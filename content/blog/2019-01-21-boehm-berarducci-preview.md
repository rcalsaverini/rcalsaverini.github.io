---
title: Boehm-Beraducci encoding for trees in python - a preview
date: 2019-01-21 00:00:00 -02:00
permalink: "/posts/2019/01/boehm-berarducci-preview"
categories:
- programming
tags:
- Python
- Functional programming
- Type encodings
draft: true
---

A few years ago I was very impressed for learning the [Boehm-Berarducci encoding], which is a way for encoding
[Algebraic Data Types] (ADTs) into a kind of [lambda calculus] that is well [typed] called [System F].
The first thing I asked myself was in which languages I would be able to use this encoding to represent ADTs,
with python being the most critical one for me.

I was specially motivated for going back at trying this in Python after [I became very frustrated] with my n-th attempt at
actually using [mypy] as a static type checker. Using Boehm-Berarducci encodings certainly will avoid some difficulties
with recursive types, but I don't think it will solve everything (specially my problems with higher kinded types
and generic tuples). Aditionaly, I'm not certain about how efficient this implementation would be (both in space and time complexity)
in a language without the facilities of modern and efficient functional compiler like GHC (tail-rec optimization, etc).

That said, it's a lot of fun to code this, and I plan to explore this in future posts. As an appetizer, here's a simple tree type
that typechecks correctly using [mypy] in Python, with smart constructors for leafs and branches:

```python

  from typing import NamedTuple, TypeVar, Callable

  A = TypeVar("A")
  R = TypeVar("R")
  Branch = Callable[[R, R], R]


  class BinaryTree(NamedTuple):
      constructor: Callable[[R, Branch[R]], R]

      def __call__(self, leaf: R, branch: Branch[R]):
          return self.constructor(leaf, branch)

      @classmethod
      def leaf(cls):
          def leafer(leaf: R, branch: Branch[R]) -> R:
              return leaf

          return cls(leafer)

      @classmethod
      def branch(cls, left, right):
          def brancher(leaf: R, branch: Branch[R]) -> R:
              return branch(left, right)

          return cls(brancher)
```

I'll still be checking it this is the actually usable in real code and it certainly falls short from the elegance
and terseness of a Haskell implementation. But compared with the typical Python code it's actually not that bad.

I'll be posting here any progress I have with this.

[Boehm-Berarducci encoding]: http://okmij.org/ftp/tagless-final/course/Boehm-Berarducci.html
[Algebraic Data Types]: https://en.wikipedia.org/wiki/Algebraic_data_type
[typed]: https://en.wikipedia.org/wiki/Typed_lambda_calculus
[lambda calculus]: https://en.wikipedia.org/wiki/Lambda_calculus
[System F]: https://en.wikipedia.org/wiki/System_F
[mypy]: http://mypy-lang.org/
[I became very frustrated]: {{< relref "blog/2019-01-20-frustrations-with-mypy.md" >}}

