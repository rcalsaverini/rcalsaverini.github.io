---
title: Type Safe Records in Haskell
date: 2018-02-13 00:00:00 -02:00
permalink: "/posts/2018/02/type-safe-records-haskell"
category: programming
tags:
- Haskell
- Type safety
- Records
- Type-level programming
---

I've been recently trying to learn more advanced type-level constructs in Haskell and was very happy to find [this amazing talk](https://www.youtube.com/watch?v=wNa3MMbhwS4) by [Prof. Stephanie Weirich](http://www.seas.upenn.edu/~sweirich/) about Dependent Types in haskell. This talk helped me to understand deeper a few more recent concepts introduced by some of GHC's extensions and how to use them. In this post I want to focus a little bit in a simplified version of one of the data structures Prof. Weirich uses in her talk. She does a lot more than this, in the talk, but I'm going slowly to understand every bit of it.

# Type Safe Records

The *record problem* is an old problem in Haskell. Succintly, Haskell's traditional native records have lots of problems -- you couldn't reuse record names, updating record fields lead to dull boilerplate code, etc. Many of those problems [have been solved](http://www.parsonsmatt.org/overcoming-records/#/) by the idea of [lenses](https://hackage.haskell.org/package/lens). See this [talk by Simon Peyton Jones](https://skillsmatter.com/skillscasts/4251-lenses-compositional-data-access-and-manipulation) to get the basics of it.

There's one interesting problem though which is I think offers a nice opportunity to learn type level programming techniques in Haskel: how to create records whose type's are aware of the fields contained in the records and their types? That means that we'd like to have record type such that the when we try to access a non-existing field:

```haskell
> getField "nonExistentFieldName" record
```

we get an actual type error in compile time. In this way, we can use the type system to rule out certain bugs from our programs.

## First attempt: a list of named entries.

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

This compiles alright, but it's not a solution to our problem. First of all, it has no information about the entry field names in the type. The type of `Dict a` only carries information about the type of the values. Second, all fields must be of the same type. If you try to build something like:
''
```haskell
-- this raises a type error
myRecord = Cons (Entry "name" "Rafael") (Cons (Entry "age" (35::Int)) Nil)
```
You'll get an obvious type error since `Cons (Entry "age" 35::Int) Nil` is a `Dict Int` and `Entry "name" "Rafael"` is an `Entry String`, and `Cons` type signature is `Entry a -> Dict a -> Dict a`.

So, it seems that this is not a very useful record (:P).

Let's try to solve the second problem first and make the type of each entry more flexible. For that we need GADTs and existential types.

## Using GADTs and existential types
The second problem is caused by the fact the we have a explicit reference to the type of the entry in the `Dict` type constructor. We could try to make it more flexible like this:

```haskell
data Dict a = Nil | Cons (Entry a) (Dict b)
```
But of course this doesn't work because the type variable `b` is not defined in this scope. There is no way for the type checker to fix it:

```
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

If the field name is `"name"` it should return a `String`, but if the field name is `"age"` it should return an `Int`. So, the return type of `getField` is something like `(forall b . Maybe b)`?? That doesn't look very useful. I can retrieve the value but I loose all the information about its type! This doesn't seem to be working...

## Keeping track of the field types

I want to get back to "infinite regress of types" I refered above. Why couldn't we put the `b` type variable above as an argument for the type constructor? Well, let's try and see. We could create a data type `Dict a b` where `a` is the value of the head `Entry` and `b` is the type of the head of the next `Dict` down the `Cons` data constructor. So:
```haskell
data Dict a b = Nil | Cons (Entry a) (Dict b ???)
```
Oops. Damn, what about the type of the entry after the next entry? And the next? This is getting out of hand.

Let's examine closer what we want. We have two data constructors:

- `Nil` doesn't take parameters and its type don't need to keep track of value types.
- `Cons` must take two parameters: an `Entry a` and a record that keeps track of its fields values, in order. It's type must be a record that adds `a` to the *sequence* of types it's keeping track of.

This looks a hell like a list of types, doesn't it? If we had a way to create **type level lists** we could have the following GADT:

```haskell

data Dict (types :: (TypeLevelList Type)) where
    Nil :: Dict TypeLevelEmptyList
    Cons :: (Entry a) -> Dict (tail :: TypeLevelList) -> Dict (a `TypeLevelCons` tail)
```

Wait, what the hell is this? First of all, what are those type signatures in the wrong place? Those are *kind signatures*. Kind is the "type of a type constructor". For example, type constructors that have no parameters, like `Bool` or `String` have kind `Type` (or `*`). Type constructors that take a single parameter, like `Maybe` have kind `Type -> Type`. Single parameter Typeclasses like `Functor` or `Monad` have kind `Type -> Constraint`, etc. 

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
data Number = Zero | Succ Number
```

What this does is to create a type constructor called `Number`, whose kind is `Type`, and two data constructors:

- `Zero`, whose type is `Number`
- `Succ`, whose type is `Number -> Number`

When you use the `DataKinds` extension this declaration creates, besides the three objects described above, three more objects:
- a "kind constructor" `'Number` (the tick is not a typo)
- a **type constructor** `'Zero` whose **kind** is `'Number`
- a **type constructor** `'Succ` whose **kind** is `'Number -> Number`

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

So, what's happening here? First of all we have the declaration `data List a  = EmptyList | ListCons a (List a)`. This is a simple list type, but since we used the `Data.Kinds` extension, we get a new list kind for free:

- `'List :: Kind -> Kind` is a "kind constructor"
- `'EmptyList :: forall a . List a` is a type constructor
- `'ListCons :: forall a . a -> List a -> List a` is another type constructor

So, when applied to the kind `Type`, the "kind constructor" `'List` creates the kind `'List Type` which is a list of types! We can have the following types which have this kind:

```haskell
'EmptyList
'ListCons Int 'EmptyList
'ListCons String (Cons Int 'EmptyList)
```

etc. Those types are not inhabited (that is, we can't construct values that have those types), but we can used them to do them to provide compile time information that helps us to avoid bugs, because we can build things that build inhabited types out of them.

For example, we can build `Dict`! Let's check the kind of `Dict` on GHCi:

```haskell
> :k Dict
Dict :: TypeLevelList Type -> Type

-- the actual GHCi output is Dict :: TypeLevelList * -> *,
-- but Type is a nice synonym for *
```







