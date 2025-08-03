---
title: Type safe records as an excuse to learn type level programming in Haskell
date: 2018-02-12 22:00:00 -02:00
permalink: "/posts/2018/02/type-level-excuse"
categories:
- programming
tags:
- Haskell
- Type safety
- Records
- Type-level programming
featured: true 
---

I've been recently trying to learn more advanced type-level constructs in Haskell and was very happy to find [this amazing talk](https://www.youtube.com/watch?v=wNa3MMbhwS4) by [Prof. Stephanie Weirich](http://www.seas.upenn.edu/~sweirich/) about Dependent Types in haskell. This talk helped me to understand deeper a few more recent concepts introduced by some of GHC's extensions and how to use them. In this post I want to focus a little bit in a simplified version of one of the data structures Prof. Weirich uses in her talk. She does a lot more than this, in the talk, but I'm going slowly to understand every bit of it.

### Type Safe Records

The _record problem_ is an old problem in Haskell. Succintly, Haskell's traditional native records have lots of problems -- you couldn't reuse record names, updating record fields lead to dull boilerplate code, etc. Many of those problems [are attacked](http://www.parsonsmatt.org/overcoming-records/#/) by the idea of [lenses](https://hackage.haskell.org/package/lens) (see this [talk by Simon Peyton Jones](https://skillsmatter.com/skillscasts/4251-lenses-compositional-data-access-and-manipulation) to get the basics of it) and many [other libraries](http://hackage.haskell.org/packages/#cat:Records) as well as the [OverloadedRecordFields](https://hackage.haskell.org/package/base-4.10.1.0/docs/GHC-Records.html) extension.

Though there are many solutions attacking parts of the record problem, there's one particular aspect of it which offers a nice opportunity to learn type level programming techniques in Haskel and are worth working out from scratch: how to create records whose type's are aware of the fields contained in the records and their types?

That means, how to create a record type such that the when we try to access a non-existing field:

```haskell
> getField "nonExistentFieldName" record
```

we get an actual type error in compile time. This allows us to completely rule out a whole class of bugs from our programs: we don't need to worry about users acessing unexisting fields type of errors because this code wouldn't even compile.

### First attempt: a list of named entries

Our first attempt will be to model our records as lists of named-entries:

```haskell
data Entry a = Entry String a
data Dict a = Nil | Cons (Entry a) (Dict a)

getField :: String -> Dict a -> Maybe a
getField _ Nil = Nothing
getField name (Cons (Entry name' x) dict') =  case (name == name') of
    True  -> Just x
    False -> getField name dict'
```

This compiles alright, but it's not a solution to our problem. First of all, it has no information about the entry field names in the type. The type of `Dict a` only carries information about the type of the values. Second, all fields must be of the same type. If you try to build something like: ''

```haskell
-- this raises a type error
myRecord = Cons (Entry "name" "Rafael") (Cons (Entry "age" (35::Int)) Nil)
```

You'll get an obvious type error since `Cons (Entry "age" 35::Int) Nil` is a `Dict Int` and `Entry "name" "Rafael"` is an `Entry String`, and `Cons` type signature is `Entry a -> Dict a -> Dict a`.

So, it seems that this is not a very useful record (:P).

Let's try to solve the second problem first and make the type of each entry more flexible. For that we need GADTs and existential types.

### Using GADTs and existential types

The second problem is caused by the fact the we have a explicit reference to the type of the entry in the `Dict` type constructor. We could try to make it more flexible like this:

```haskell
data Dict a = Nil | Cons (Entry a) (Dict b)
```

But of course this doesn't work because the type variable `b` is not defined in this scope. There is no way for the type checker to fix it:

```ghci
/.../Post.hs:5:42: error:
    Not in scope: type variable ‘b’
  |
5 | data Dict a = Nil | Cons (Entry a) (Dict b)
```

For this to work, we need to put `b` in scope, without adding it as argument to the type constructor or else we'd get an infinite regress of types (I'll get back to this later). For that we need two GHC extensions: `GADTs` and `Rank2Types` (or `RankNTypes`, or other extension providing the `forall` keyword).

`GADTs` is an extension that allows us to give more generic types to the data constructors of an algebraic data type. It also allows a nicer syntax for data constructors with a long type signature. With `GADTs` and `RankNTypes` enabled we can do this:

```haskell
{-# LANGUAGE GADTs, RankNTypes  #-}

data Entry a = Entry String a
data Dict a = Nil | forall b . Cons (Entry a) (Dict b)
```

This compiles correctly and we can try to use it! Now our previous record is well typed:

```haskell
myRecord :: Dict String
myRecord = Cons (Entry "name" "Rafael") (Cons (Entry "age" (35::Int)) Nil)
```

But look what happened. The information that there's an `Int` somewhere inside the structure of the record is gone! Yep. We enclosed it in a `forall` and all the information `Cons` have now is that its second argument is some kind of `Dict b`, whatever `b` is. This doesn't look like a good sign.

Let's try to write a `getField` function. We still didn't solve the problem of letting the type know what fields are possible, so we still need to guard ourselves against the possibility that the user will try to fetch the data from a field that doesn't exist. So the signature of `getField` still is `String -> Dict a -> Maybe`... wait a minute! What's the return type?

In the record above, if the field name is `"name"` it should return a `String`, but if the field name is `"age"` it should return an `Int`. But the compiler wouldn't know that because there's no information in the type of the record about the value of the fields in is tail. We only have information about the type of the head entry.

So, the return type of `getField` is something like `(forall b . Maybe b)`? That doesn't look very useful. I can retrieve the value but I loose all the information about its type! This doesn't seem to be working...

### Keeping track of the field types

I want to get back to "infinite regress of types" I refered above. Why couldn't we put the `b` type variable above as an argument for the type constructor? Well, let's try and see. We could create a data type `Dict a b` where `a` is the value of the head `Entry` and `b` is the type of the head of the next `Dict` down the `Cons` data constructor. So:

```haskell
data Dict a b = Nil | Cons (Entry a) (Dict b ???)
```

Oops. Damn, what about the type of the entry after the next entry? Well... Let's put it in the constructor too:

```haskell
data Dict a b c = Nil | Cons (Entry a) (Dict b c ???)
```

You get it, right? There's always a new type to keep track of. The type of the record must know not only the type of the head entry, but also all the types of all entries in its tail. This looks a hell like a linked list of types, doesn't it? If we had a way to create **a type level list** we could have the following GADT:

```haskell
data Dict (types :: (TypeLevelList Type)) where
    Nil :: Dict TypeLevelEmptyList
    Cons :: (Entry a) -> Dict (tail :: TypeLevelList) -> Dict (a `TypeLevelCons` tail)
```

Wait, what the hell is this? First of all, what are those type signatures in the wrong place? Those are _kind signatures_. Kind is the "type of a type constructor". For example, type constructors that have no parameters, like `Bool` or `String` have kind `Type` (or `*`). Type constructors that take a single parameter, like `Maybe` have kind `Type -> Type`. Single parameter Typeclasses like `Functor` or `Monad` have kind `Type -> Constraint`, etc.

Here I'm supposing that there exists a kind called `TypeLevelList`, and that there exists two type constructors:

- `TypeLevelEmptyList` with kind `TypeLevelList`,
- `TypeLevelCons` with kind `Type -> TypeLevelList -> TypeLevelList`.

When I write `data Dict (types :: TypeLevelList)` I'm declaring a type constructor `Dict`with kind `TypeLevelList -> Type`. This type has two data constructors:

- `Nil` which is just an empty record with type `Dict TypeLevelEmptyList`
- `Cons` which takes an `Entry a` and a `Dict TypeLevelList` and return another `Dict TypeLevelList` putting `a` on the head of that `TypeLevelList` it received.

In practice we'd have something like this:

```haskell
emptyRecord :: Dict TypeLevelEmptyList
emptyRecord = Nil

agedRecord :: Dict (Int `TypeLevelCons` TypeLevelEmptyList)
agedRecord = Cons (Entry "age" 35) emptyRecord

recordWithAStringAndAnInt :: Dict (String `TypeLevelCons` Int `TypeLevelCons` TypeLevelEmptyList)
namedAndAgedRecord = Cons (Entry "name" "Rafael") agedRecord
```

This is sweet! We can keep track to the types of all fields! But how do we create those type level lists? :O
### Type Level Lists

To create those type level lists we have to use a GHC extension called `DataKinds`. To understand what `DataKinds` do lets consider this simple type declaration:

```haskell
data Nat = Zero | Succ Nat
```

What this does is to create a type constructor called `Nat`, whose kind is `Type`, and two data constructors:

- `Zero`, whose type is `Nat`
- `Succ`, whose type is `Nat -> Nat`

When you use the `DataKinds` extension this declaration creates, besides the three objects described above, three more objects:

- a **"kind constructor"** `'Nat` (the tick is not a typo)
- a **type constructor** `'Zero` whose **kind** is `'Nat`
- a **type constructor** `'Succ` whose **kind** is `'Nat -> 'Nat`

Those types constructed with those type constructors are not inhabited by values, but they are very useful for **type computation**. So, how do we create the "kind constructor" `TypeLevelList` with type constructor `TypeLevelEmptyList` and `TypeLevelCons`? Exactly with the same code that we would use to create a type constructor `List` with data constructor `EmptyList` and `Cons`, but we use the `DataKinds` extension to lift those objects from the `value :: type` world to the `type :: kind` world. We can do:

```haskell
{-# LANGUAGE  GADTs, RankNTypes, DataKinds, KindSignatures #-}

module Post where

import Data.Kind (Type)

data Entry a = Entry String a

data List a  = EmptyList | ListCons a (List a)

data Dict (a :: (List Type)) where
    Nil :: Dict 'EmptyList
    Cons :: Entry a -> Dict t -> Dict ('ListCons a t)
```

So, what's happening here? First of all we have the declaration `data List a = EmptyList | ListCons a (List a)`. This is a simple _list type_, but since we used the `Data.Kinds` extension, we get a new **list kind** for free:

- `'List` is a "kind constructor" which takes a kind and return another kind (`* -> *`)
- `'EmptyList :: forall a . List a` is a type constructor
- `'ListCons :: forall a . a -> List a -> List a` is another type constructor

So, when applied to the kind `Type`, the "kind constructor" `'List` creates the kind `'List Type` which is a list of types! We can have the following types which have this kind:

```haskell
'EmptyList
'ListCons Int 'EmptyList
'ListCons String (Cons Int 'EmptyList)
```

etc. All those types have kind `'List Type`. Those types are not inhabited (that is, we can't construct values that have those types), but we can used them to provide compile time information that helps us to avoid bugs, because we can build type constructors that build inhabited types out of them! For example, we can build `Dict`. Let's check the kind of `Dict` on GHCi:

```haskell
> :k Dict
Dict :: List Type -> Type
-- the actual GHCi output is Dict :: List * -> *, but Type is a nice synonym for *
```

This is what's happening with the declaration `data Dict (a :: (List Type))`. We used the extension `KindSignatures` to inform the compiler that the `Dict` type constructor has a kind which takes an argument of kind `List Type` and returns a regular `Type`.

Now to the data constructors - which are the things that allows us to actually build values of type `Dict a`. The simples one is `Nil` which builds a value of type `Dict 'EmptyList`. This is an empty record, with no values stored and thus no types stored in the type level list.

Also we have `Cons`, which takes a parameter of type `Entry a` and a parameter of type `Dict t` (remember, here `t` is a type of kind `'List Type`) and builds a value of type `Dict ('ListCons a t)`. So, `Cons` does two things:

- it concatenates a new entry with an existing record,
- it also concatenates the _type_ of the value stored in this entry into an _existing list of types_ that describes the types of the entries in the existing record.

Wow. If that's too much to grasp, let's see this in action:

```haskell
namedRecord ::Dict ('ListCons String 'EmptyList)
namedRecord = (Entry "name" "Rafael") Nil

namedAndAgedRecord :: Dict ('ListCons Int ('ListCons String 'EmptyList))
namedAndAgedRecord = Cons (Entry "age" (35::Int)) namedRecord
```

See how the types of the fields we're creating are concatenated in the type of the record? This allows us to know precisely the types of all the fields in a record!
### Making it prettier

We didn't have to code our own list type, Haskell already provides one for us and fortunately `Data.Kinds` works with the built-in types too. So we could have written simply:

```haskell
{-# LANGUAGE  GADTs, RankNTypes, DataKinds, KindSignatures, TypeInType, TypeOperators #-}

module Post where

import Data.Kind (Type)

infixr 6 :>

data Entry a = Entry String a

data Dict (a :: [Type]) where
    Nil :: Dict '[]
    (:>) :: Entry a -> Dict t -> Dict (a:t)
```

We made a few changes to make the types nicer:

- We are now using Haskel's built-in lists:

  ```haskell
  > :k Dict
  Dict :: [Type] -> Type
  ```

  This is completely equivalent to the previous signature `List Type -> Type` the only difference is that we're using the built-in type instead of our custom list type.

- We're using the `TypeInType` extension to allow for the syntax `[Type]`

- We're using the `TypeOperators` extension to allow for two things:

  1. using the promoted type constructor `(:) :: a -> [a] -> [a]` which concatenates a type on the head of a type level list;
  2. renaming the ugly `Cons` data constructor to a nicer `(:>)` infix type operator so that the expressions are nicer looking.

With this modifications, instead of this ugly monster:

```haskell
myRecord :: Dict ('ListCons String ('ListCons Int 'EmptyList))
myRecord = Cons (Entry "name" "Rafael") (Cons (Entry "age" 35) Nil)
```

we can write this:

```haskell
myRecord :: Dict '[String, Int]
myRecord = Entry "name" "Rafael" :> Entry "age" 35 :> Nil
```

Much better, right?
### This is already too long and you didn't get to the point you promised

Well, yep. This post is already big and we still don't know:

- how to write `getField`
- how to enhance the type `Dict` to allow for information about field names to be statically checked by the compiler.

So it looks like a perfect point to stop and start planning to write Part 2!
