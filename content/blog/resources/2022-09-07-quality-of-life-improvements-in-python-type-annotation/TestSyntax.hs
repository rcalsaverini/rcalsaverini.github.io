{-# LANGUAGE FlexibleInstances #-}
{-# LANGUAGE MultiParamTypeClasses #-}
{-# LANGUAGE TypeFamilies #-}
{-# LANGUAGE UndecidableInstances #-}

module TestSyntax where

import qualified Prelude as P

class Scalable a where
  type Scale a
  (*) :: a -> Scale a -> a

class Divisible a b where
  type Ratio a b
  (/) :: a -> b -> Ratio a b
  (<*) :: b -> Ratio a b -> a
  (*>) :: Ratio a b -> b -> a
  (</) :: a -> Ratio a b -> b

instance Divisible a a => Scalable a where
  type Scale a = Ratio a a
  (*) = (<*)

instance (P.Fractional a, P.Num a) => Divisible a a where
  type Ratio a a = a
  (/) = (P./)
  (<*) = (P.*)
  (*>) = (P.*)
  (</) = (P./)

newtype Dollar = Dollar P.Float

newtype Real = Real P.Float

newtype ExchangeRate = ExchangeRate P.Float

type Money = P.Either Dollar Real

dollar :: ExchangeRate -> Money -> Dollar
dollar _ (P.Left x) = x
dollar q (P.Right x) = x <* q

real :: ExchangeRate -> Money -> Real
real _ (P.Right x) = x
real q (P.Left x) = x </ q

instance Divisible Dollar Real where
  type Ratio Dollar Real = ExchangeRate

  (Dollar d) / (Real r) = ExchangeRate (d / r)
  (Real r) <* (ExchangeRate e) = Dollar (r P.* e)
  (ExchangeRate e) *> (Real r) = Dollar (r P.* e)
  (Dollar d) </ (ExchangeRate e) = Real (d P./ e)
