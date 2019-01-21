---
title: Boehm-Beraducci encoding for trees in python: a preview
date: 2019-01-21
permalink: /posts/2019/01/boehm-berarducci-preview
category: programming
tags:
  - Python
  - Functional programming
  - Type encodings
---

A few years ago I was very impressed for learning the [Boehm-Berarducci encoding], which is a way for encoding 
[Algebraic Data Types] (ADTs) into a kind of [typed] [lambda calculus] called [System F] and the first thing I asked myself was in 
which languages I would be able to use this encoding to represent ADTs, with python being the most critical one for me. 
I don't know anything about how efficient this implementation would be (both in memory use and actual complexity) in a 
language without the facilities of modern and efficient functional compiler like GHC (tail-rec optimization, etc), but 
it's a fun exercise anyway.

So here's a simple tree type that typechecks correctly using [mypy] in Python:

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

I'll still be analysing the actuall usability of this in real code, but I think that, while it falls short from the elegance
and terseness of a Haskell implementation, it's actually not that bad compared with the typical Python code. I'll be posting
here any progress I have with this.


[Boehm-Berarducci encoding]: http://okmij.org/ftp/tagless-final/course/Boehm-Berarducci.html
[Algebraic Data Types]: https://en.wikipedia.org/wiki/Algebraic_data_type
[lambda calculus]: https://en.wikipedia.org/wiki/Lambda_calculus
[typed]: https://en.wikipedia.org/wiki/Typed_lambda_calculus
[System F]: https://en.wikipedia.org/wiki/System_F
