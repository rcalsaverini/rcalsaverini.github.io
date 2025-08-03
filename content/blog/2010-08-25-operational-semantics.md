---
title: Operational Semantics for Monads
date: 2010-08-25 21:00:00 -03:00
permalink: "/posts/2010/08/operational-semantics-for-monads"
categories:
- programming
tags:
- Haskell
- Monads
- Operational Monads
- Free Monads
- Free Vector Space
- Category Theory
author: Rafael S. Calsaverini
---

**Disclaimer: this is an old blog post from a very old wordpress blog and may contain inacuracies. I reproduced it as is for sentimental reasons. I may revisit this theme later.**

While randomly browsing around on [Planet Haskell](http://planet.haskell.org/) I've found [a post](http://apfelmus.nfshost.com/articles/operational-monad.html#concatenation-and-thoughts-on-the-interface) on [Heinrich Apfelmus' blog](http://apfelmus.nfshost.com/) about something called "operational semantics" for monads. Found it very iluminating. Basically it's a form to implement monads focusing not on defining the bind and return operators, but on what the monad is really supposed to do. It's a view where a monad define a Domain Specific Language, that must be interpreted in order to cause it's effects. It seems to me it's exactly what is implemented in the [monadprompt (Control.Monad.Prompt)](http://hackage.haskell.org/packages/archive/MonadPrompt/1.0.0.2/doc/html/Control-Monad-Prompt.html) package, although I'm not sure.

# The Operational Monad

```haskell
{-# LANGUAGE GADTs #-}
import Control.Monad
import Data.Map (Map, fromList, unionWith)
```

The definition of a monad on this approach starts with a common interface given by the following data type and a singleton function:

```haskell
data Program m a where
    Then :: m a -> (a -> Program m b) -> Program m b
    Return :: a -> Program m a

singleton :: m a -> Program m a
singleton i = i `Then` Return
```

Note that the types of the data constructors Then and Return are very similar (but not equal...) to the types of the monadic operations (>>=) and return. This identification of class functions with data constructors is recurring throughout this post. This data type is instanciated as a traditional monad as follows:

```haskell
instance Monad (Program m) where
    return = Return
    (Return a)    >>= f  = f a
    (i `Then` is) >>= f  = i `Then` (\ x -> is x >>= f)
```

This is all we need! As an example let's describe the implementation of the State Monad within this approach. This is exactly the first example given by Apfelmus on his post, disguised as a stack machine.

# Example: implementing the State Monad

The operational approach to monads begins with recognizing what operations you want your monad to perform. A State Monad have a state, a return value and two function: one that allows us to retrieve the state as the return value, and one that allows us to insert a new state. Let's represent this in the following GADT:

```haskell
data StateOp st retVal where
    Get :: StateOp st st  -- retrieve current state as a returned value
    Put :: st -> StateOp st ()  -- insert a new state
```

This are the operations needed on the `State` Monad, but the monad itself is a sequence of compositions of such operations:

```haskell
type State st retVal = Program (StateOp st) retVal
```

Note that the type synonym State st is a monad already and satisfy all the monad laws by construction. We don't need to worry about implementing return and `(>>=)` correctly: they are already defined.

So far, so good but... how do we use this monad in practice? This types define a kind of Domain Specific Language: we have operations represented by Get and Put and we can compose them in little programs by using Then and Return. Now we need to write an interpreter for this language. I find this is greatly simplified if you notice that the construct

```haskell
do x <- singleton foo
   bar x
```

can be translated as _foo `Then` bar_ in this context. Thus, to define how you'll interpret the later, just think what's the effect you want to have when you write the former.

Our interpreter will take a `State st retVal` and a state st as input and return a pair: the next state and the returned value `(st, retVal)`:

```haskell
interpret :: State st retVal -> st -> (st, retVal)
```

First of all, how should we interpret the program `Return val` ? This program just takes any state input and return it unaltered, with val as it's returned value:

```haskell
interpret (Return val) st = (st, val)
```

The next step is to interpret the program _foo `Then` bar_. Looking at the type of things always helps: Then, in this context, have type `StateOp st a -> (a -> State st b) -> State st b`. So, in the expression _foo `Then` bar_, foo is of type `StateOp st a`, that is, it's a stateful computation with state of type `st` and returned value of type `a`. The rest of the expression, `bar`, is of type `a -> State st b`, that is, it expects to receive something of the type of the returned value of foo and return the next computation to be executed. We have two options for `foo`: `Get` and `Put x`.

When executing _Get `Then` bar_, we want this program to return the current state as the returned value. But we also want it to call the execution of `bar val`, the rest of the code. And if `val` is the value returned by the last computation, `Get`, it must be the current state:

```haskell
interpret (Get `Then` bar) st = interpret (bar st) st
```

The program _Put x `Then` bar_ is suposed to just insert `x` as the new state and call `bar val`. But if you look at the type of `Put x`, it's returned value is empty: `()`. So we must call `bar ()`. The current state is then discarded and substituted by `x`.

```haskell
interpret (Put x `Then` bar) _  = interpret (bar ()) x
```

We have our interpreter (which, you guessed right, is just the function `runState` from `Control.Monad.State) and now it's time to write programs in this language. Let's then define some helper functions:

```haskell
get :: State st st
get = singleton Get

put :: st -> State st ()
put = singleton . Put
```

and write some code to be interpreted:

```haskell
example :: Num a => State a a
example = do x <- get
          put (x + 1)
          return x

test1 = interpret example 0
test2 = interpret (replicateM 10 example) 0
```

This can be run in ghci to give exactly what you would expect from the state monad:

```haskell
*Main> test1
(1,0)

*Main> test2
(10,[0,1,2,3,4,5,6,7,8,9])
```

# Vector Spaces

The approach seems very convenient from the point of view of developing applications, as it's focused on what are actions the code must implement and how the code should be executed. But it seems to me that the focus on the operations the monad will implement is also very convenient to think about mathematical structures. To give an example, I'd like to implement a monad for Vector Spaces, in the spirit of Dan Piponi (Sigfpe)'s ideas [here](http://blog.sigfpe.com/2007/02/monads-for-vector-spaces-probability.html), [here](http://blog.sigfpe.com/2007/03/monads-vector-spaces-and-quantum.html) and [here](http://blog.sigfpe.com/2009/05/trace-diagrams-with-monads.html).

A vector space $\mathbb{V_F}$ is a set of elements $\mathbf{x}\in\mathbb{V_F}$ that can be summed ($\mathbf{x} + \mathbf{y} \in\mathbb{V_F}$ if $\mathbf{x},\mathbf{y} \in \mathbb{V_F}$) and multiplied elements of a field ($\alpha\mathbf{x}$ if $\alpha\in \mathcal{F}$ and $\mathbf{x}\in\mathbb{V_F}$). If we want this to be implemented as a monad then, we should, in analogy with what we did for the State Monad, write a GADT with data constructors that implement the sum and product by a scalar:

```haskell
data VectorOp field label where

    Sum :: Vector field label
        -> Vector field label
        -> VectorOp field label

    Mul :: field
        -> Vector field label
        -> VectorOp field label

type Vector field label = Program (VectorOp field) label
```

and then we must implement a interpreter:

```haskell
runVector :: (Num field, Ord label) => Vector field label -> Map label field
runVector (Return a) = fromList [(a, 1)]
runVector (Sum u v `Then` foo) = let uVec = (runVector (u >>= foo))
                                     vVec = (runVector (v >>= foo))
                                 in unionWith (+) uVec vVec
runVector (Mul x u `Then` foo) = fmap (x*) (runVector (u >>= foo))
```

The interpreter `runVector` takes a vector and returns it's representation as a `Map`. As an example, we could do the following:

```haskell
infixr 3 <*>
infixr 2 <+>

u <+> v = singleton $ Sum u v
x <*> u = singleton $ Mul x u

data Base = X | Y | Z deriving(Ord, Eq, Show)

x, y, z :: Vector Double Base
x = return X
y = return Y
z = return Z

reflectXY :: Vector Double Base -> Vector Double Base
reflectXY vecU = do cp <- vecU
                    return (transf cp)
                        where transf X = Y
                              transf Y = X
                              transf Z = Z
```

and test this on ghci:

```ghci
*Main> runVector $ x <+> y
fromList [(X,1.0),(Y,1.0)]

*Main> runVector $ reflectXY $ x <+> z
fromList [(Y,1.0),(Z,1.0)]
```

As Dan Piponi points out in his talk, any function acting on the base `f :: Base -> Base` is lifted to a linear map on the vector space Space field Base by doing (because this is the Free Vector Space over `Base`):

```haskell
linearTrans f u = do vec <- u
                  return (f vec)
```

More on this later. :)
