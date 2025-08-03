---
title: Revisiting the Python type annotation system.
description: ""
date: 2022-09-07T16:06:54.219Z
preview: true
draft: false
categories:
  - Matplotlib
  - Coordinates
format: hugo
jupyter: python3
lastmod: 2022-09-28T16:44:18.907Z
---

Years ago I [made a post]({{< ref "blog/2019-01-20-frustrations-with-mypy.md" >}}) complaining about the python type annotation system. I want to revisit it now that the system is more mature and has some new interesting features.

## The syntax is slowly improving

In my original post I complained about writing `Callable[[float, float], float]` for functions or `Union[str, int]` for sum types. That sucks a lot and it's not very transparent or easy to read. There has a couple of improvements and other are in the pipeline for approval that address those issues:

- With [PEP 585](https://peps.python.org/pep-0585/), accepted for Python 3.9, the raw python collections types (like `list`, `dict`, `tuple`) can be used in type annotations with generics without need to use the special classes from the `typing` module. So, instead of importing `Dict` and `List` from the `typing` and writing `Dict[str, List[int]]`, you can simply use the raw collection types: `dict[str, list[int]]` for annotating stuff.
- With [PEP 604](https://peps.python.org/pep-0604/), accepted for Python 3.10, union types can be written like `A | B` instead of `Union[A, B]`. Also `Optional[A]` can be written as `A | None`.

Unfortunately, my favorite change was rejected. [PEP 677](https://peps.python.org/pep-0677/), which proposes the arrow syntax `(arg1, arg2) -> res` as a synonym for `Callable[[arg1, arg2], res]` for callable objects.

## Improvements

[PEP 612](https://peps.python.org/pep-0612/) introduced parameter specifications in Python 3.10.

## Annotated Types

[PEP 593](https://peps.python.org/pep-0593/) introduced `Annotated` types.

## Type Guards

[PEP 647](https://peps.python.org/pep-0647/) introduced user defined Type Guards in Python 3.10.

## Adoption increased substantially, usability too

A lot of the libraries I use have adopted facilities for type annotations in the last three years. It's still ubiquitous as to be 100% seamless, but today it's not a pain anymore. Even numerical libraries such as `numpy` have adopted ways of providing annotations, which is super nice.

I still think that annotating arrays or dataframes with types that don't provide introspection about their dimensionality or the type they contain inside them is not super useful.

For example, this:

```python
from numpy.typing import NDArray

def my_function(x: NDArray) -> NDArray:
  return x.sum(axis=1)
```

would prevent me from mistakingly calling this function with a string or a list, but it wouldn't prevent me from calling it with a 1D array and getting a runtime error.

But there are many libraries providing better type abstractions for arrays. For example, with [`nptyping`](https://github.com/ramonhagenaars/nptyping/blob/master/USERDOCS.md) we could do:

```python
from nptyping import NDArray, Shape, Float

FloatArray2D = NDArray[Shape["N, D"], Float]
IntArray1D = NDArray[Shape["N"], Float]

def my_function(x: FloatArray2D) -> IntArray1D:
  "Should typecheck"
  return x.sum(axis=1).astype(int)

def my_function_error(x: FloatArray2D) -> IntArray1D:
  "Should NOT typecheck"
  return x.sum(axis=1)
```
