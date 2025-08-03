# new syntax for collections in the standard library
import re
from typing import Annotated, Generic, TypeVar, TypedDict, Union


def find(haystack: dict[str, list[int]]):
    pass


# new syntax for optionals and unions
maybe_int: int | None = 4
int_or_str: int | str = "alo"

# Annotated


class Dollar(float):
    pass


class Real(float):
    pass


A = TypeVar("A", bound=float)
B = TypeVar("B", bound=float)


class Ratio(Generic[A, B]):
    value: float

    def __mul__(self, other: B) -> A:
        return other * self.value  # type: ignore

    def __rmul__(self, other: B) -> A:
        return other * self.value  # type: ignore

    def __rdiv__(self, other: A) -> B:
        return other / self.value  # type: ignore


class Money:
    _dollar: Dollar | None
    _real: Real | None

    def __init__(self, ammount: Dollar | Real, exchange_rate: Ratio[Dollar, Real]):
        self._exchange_rate: Ratio[Dollar, Real] = exchange_rate
        if isinstance(ammount, Dollar):
            self._dollar = ammount
            self._real = None
        elif isinstance(ammount, Real):
            self._real = ammount
            self._dollar = None
        else:
            return ValueError("Variable `ammount` needs to be a Dollar or Real value.")

    @property
    def dollar(self) -> Dollar:
        if self._dollar is not None:
            return self._dollar
        elif self._real is not None:
            return self._real * self._exchange_rate
        else:
            raise NotImplementedError()

    @property
    def real(self) -> Real:
        if self._real is not None:
            return self._real
        elif self._dollar is not None:
            return Real(self._dollar / self._exchange_rate)
        else:
            raise NotImplementedError()


class InterestRate(float):
    pass


def applyInterest(money: Money, rate: InterestRate) -> Money:
    return Money(money * (1 + rate))


applyInterest(Money(10), InterestRate(0.05))
