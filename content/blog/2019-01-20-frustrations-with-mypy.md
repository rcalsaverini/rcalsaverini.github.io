---
title: A few frustrations with Python's type annotation system
date: 2019-01-20 22:00:00 -02:00
permalink: "/posts/2019/01/frustrations-with-python-types"
categories:
- programming
tags:
- Python
- Type safety
- Mypy
featured: true
---

I have on and off again tried to use [mypy] to type check my python code, but some shortcomings of Python's type annotation system really get in the way. This came now because I needed to write code involving trees that had to change the types of values stored on the nodes. This highlighted a few serious shortcomings for anyone that is accostumed to use stronger type systems.

### The ugly syntax for function types is annoying but there are worse problems

Yes, writing `Callable[[Callable[[A], B], F[A]], F[B]]` instead of `(a -> b) -> f a -> f b` as in Haskell or `(A => B, F[A]) => F[B]` (or maybe the uncurried `(A => B) => (F[A] => F[B])` version) as in Scala is really annoying.

But that's neither here nor there. One can get accostumed to it. On the other hand, it is certainly symptomatic of the philosophy chosen for the type system: passing functions around is not an idea on the forefront of this design.

### People are not using it

In general, the overwhelming majority of the python libraries I use simply don't have type annotations or stub files and don't plan to add them in the near future. Writing stub files on your own is a pain. This by itself prevents the adoption of type annotations without a lot of effort in providing stub files yourself.

### The ad hoc polymorphism mechanism chosen is annoying

The only way to do ad hoc polymorphism is with structural subtyping (using `Protocol`). This isn't so bad, since the language embraces duck typing so thoroughly. But it's somewhat annoying for two reasons:

1. First, admitedly a lesser problem, there's no clear indication in the code that a given class implements a particular `Protocol`. There's no explicit inheritance, nor explicit instancing of the `Protocol`. If you don't know the protocol exists, when you see the code of a class, you have no clue that there is a more general pattern that this class implements.

2. Second, there's no "post facto" instancing of `Protocol` like it's possible to do with Haskell's or Scala's typeclasses, or Go's interfaces. You have one chance to instanciate a class as a particular Protocol: when you write that classes code. If the class belongs to a third party library you can't change, you have to write wrappers (which are terribly annoying, because the language offers no syntax sugar for them).

### No support for lightweight parametrically polymorphic product types

Python's type annotations don't allow you to write generic named tuples. This prevents one to write very lightweight types like:

```python
class Foo(NamedTuple, Generic[A]):
    a_value: A
    a_list: List[A]
```

If you want a parametrically polymorphic type, it must be a fully fledged class by itself.

```python
### will type check
class Foo(Generic[A]):
    def __init__(self, a_value: A, a_list: List[A]):
        self.a_value = a_value
        self.a_list = a_list
```

This discourages me to use it for many applications, since Python's classes are not exactly lightweight things and I'd rather not have a class if I don't really need one. You could use a type synonym for an untagged tuple, but this would be a serious documentation hazard:

```python
Foo = Tuple[A, List[A]]
```

### No support for lightweight recursive product types

Similarly, Python's type annotations don't allow recursive types unless you're dealing with a full fledged class. Recursive `NamedTuples` are forbidden, and so are recursive `Union`s (which wouldn't be possible given the restriction on higher-kinded types anyway, see below). This further prevents fast and lightweight types like:

```python
class BinaryTree(NamedTuple):
    left: "BinaryTree"
    right: "BinaryTree"
```

and requires you to use the full (and heavy) Python classes:

```python
class BinaryTree(object):
    def __init__(self, left: "BinaryTree", right: "BinaryTree"):
            self.left = left
            self.right = right
```

### No higher kinded types

Python's type annotations have no support for [higher-kinded] types. All type variables in a class that inherit from Generic must be of kind `*`. This is kind of a catastrophe for any kind of more advanced use of the type system to improve correctness garantees. It also prevents some uses of higher kinded patterns like functors, monads, etc.

For example, you can't use the finally tagless or [tagless-final] pattern. At least not like this:

```python
class DataAccessMonad(Generic[M]):
    def get_user(self, user_id: UserId) -> M[User]
        pass
```

Also, this makes it difficult to implement "post-facto" ad hoc polymorphism using something like [Scala's typeclass instance] mechanisms to escape `Protocol`s. For this, one would need to write:

```python
class FunctorInstance(Generic[F]):

    @staticmethod
    def map(value: F[A], function: Callable[[A], B]) -> F[B]:
        pass
```

My original plan for a type class library involved creating a way to inject the instance, wrap the `F[A]` value and monkey patch it to call `value.map` when you need it. The fact that one can't use higher kinded types prevents the code above to type check.

### And so... no fixed point functors and other niceties

This means also that you can't use fixed point types like:

```python
class CoFree(NamedTuple, Generic[F, A]):
    value: A
    continuations: F["Cofree[F, A]"]
```

because this requires F to be of kind `* -> *`. Fixed point types are awfully useful for dealing with tree-like structures (see for example [this talk from Rob Norris]) and would similarly fail to type check on [mypy].

### Conclusion

There are more problems, but those are the main ones that prevented me from really using [mypy] or type annotations in Python. This haven't prevented me from writing good and useful Python code, and I still love to write Python. But it certainly increases the attrition.

[higher-kinded]: https://stackoverflow.com/questions/6246719/what-is-a-higher-kinded-type-in-scala
[mypy]: http://mypy-lang.org/
[scala's typeclass instance]: https://typelevel.org/cats/typeclasses.html
[tagless-final]: http://okmij.org/ftp/tagless-final/index.html
[this talk from rob norris]: https://www.youtube.com/watch?v=7xSfLPD6tiQ
