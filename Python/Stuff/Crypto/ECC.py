from __future__ import annotations
from abc import ABC, abstractmethod


class Point() : 
    Inf = O = None
    def __init__(self, x:int=None, y:int=None, Curve:EllipticCurve=None) : (self.x, self.y, self.Curve) = (x, y, Curve)
    def __repr__(self) -> str : return f"Point(x={self.x}, y={self.y})"

    def __eq__(self, other:object) -> bool : return (isinstance(other, Point) and self.x==other.x and self.y==other.y)
    def __hash__(self) -> int : return (self.x, self.y).__hash__()

    def __add__(self, other) -> Point : return self.__iadd__(other)
    def __radd__(self, other) -> Point : return self.__iadd__(other)
    def __iadd__(self, other) -> Point : 
        if not isinstance(other, Point) : return NotImplemented
        if self==Point.O and other==Point.O : return Point.Inf
        return (self.Curve | other.Curve).CheckHasPoint(self).CheckHasPoint(other).Dot(self, other)

    def __mul__(self, other) -> Point : return self.__imul__(other)
    def __rmul__(self, other) -> Point : return self.__imul__(other)
    def __imul__(self, other) -> Point : 
        if not isinstance(other, int) : return NotImplemented
        return self.Curve.CheckHasPoint(self).Ladder(other, self)
Point.Inf = Point.O = Point()


class EllipticCurve(ABC) : 
    def __init__(self, Prime:int, A:int, B:int, G:Point=None, Order:int=None, Cofactor:int=None) : 
        self.Prime = Prime # Modulus
        self.A = A
        self.B = B
        self.G = G
        self.Order = Order # N
        self.Cofactor = Cofactor # N/R(Subgroups); esp TwistedEdwards(?) = 4(?)
        
        if self.G is not None : self.G.Curve = self
    def __repr__(self) -> str : return f"{self.__class__.__name__}({', '.join([f'{k}={v}' for (k,v) in vars(self).items()])})"

    def __del__(self) : del self.__dict__
    def __enter__(self) : return self
    def __exit__(self, type, value, tb) : self.__del__()

    def __or__(self, other) : return self.__ror__(other)
    def __ror__(self, other) : return self

    def _SqrtMod(self, n, p) : 
        """ https://en.wikipedia.org/wiki/Tonelli%E2%80%93Shanks_algorithm#The_algorithm """
        def __Legendre(a, p) : 
            l = pow(a, (p - 1) // 2, p)
            return (-1 if l == p - 1 else l)

        if __Legendre(n, p) < 0 : raise ValueError("not a square (mod p)")
        elif (p & 3)==3 : return pow(n, (p + 1) // 4, p) # (p % 4)==3

        Q = p - 1
        S = 0
        while Q & 1 == 0 : 
            Q = Q>>1
            S = S + 1

        z = 2
        while __Legendre(z, p) != -1 : z = z + 1

        M = S
        c = pow(z, Q, p)
        t = pow(n, Q, p)
        R = pow(n, (Q + 1) // 2, p)

        while True : 
            if t==0 : return 0
            elif t==1 : return R

            t2 = t
            for i in range(1, M) : 
                t2 = pow(t2, 2, p)
                if t2 == 1 : break

            b = pow(c, 2 ** (M - i - 1), p)
            M = i
            c = (b * b) % p
            t = (t * c) % p
            R = (R * b) % p

    @abstractmethod
    def CheckHasPoint(self, P:Point) -> EllipticCurve : raise NotImplementedError
    def GeneratePoints(self) -> list[Point] : 
        points = set([Point.O, Point.Inf])
        for x in range(self.Prime) : 
            for y in range(self.Prime) : 
                point = Point(x, y, self)
                try : 
                    self.CheckHasPoint(point)
                    points.add(point)
                except : pass
        return list(points)

    @abstractmethod
    def Dot(self, P:Point=Point.O, Q:Point=Point.O) -> Point : raise NotImplementedError
    def Ladder(self, x:int, P:Point) -> Point : 
        if x==0 : return Point.Inf

        R0 = Point.Inf
        R1 = P
        for byt in [int(i, 2) for i in f"{x:b}"] : 
            if byt==0 : (R0, R1) = (self.Dot(R0, R0), self.Dot(R0, R1))
            else : (R0, R1) = (self.Dot(R0, R1), self.Dot(R1, R1))
        return R0

    def CompressPoint(self, D:Point) -> Point : return Point(x=D.x, y=(D.y & 1))
    @abstractmethod
    def DecompressPoint(self, C:Point) -> Point : raise NotImplementedError


class Weierstrass(EllipticCurve) :
    """ (y**2) % Prime = (x**3 + A*x + B) % Prime """
    def CheckHasPoint(self, P:Point) -> EllipticCurve : 
        if (P==Point.O or P==self.G or ((P.y**2) % self.Prime == (P.x**3 + self.A*P.x + self.B) % self.Prime)) : return self
        else : raise ValueError("point not on curve")
    def Dot(self, P:Point=Point.O, Q:Point=Point.O) -> Point : 
        if P==Point.O and Q==Point.O : return Point.Inf
        elif P==Point.O : return Q
        elif Q==Point.O : return P

        if P==Q and P.y!=0 : l = ((3 * P.x**2 + self.A) * pow(2 * P.y, -1, self.Prime)) % self.Prime 
        elif P!=Q and P.x!=Q.x : l = ((Q.y - P.y) * pow(Q.x - P.x, -1, self.Prime)) % self.Prime
        else : return Point.Inf

        R = Point(Curve=self)
        R.x = (l**2 - P.x - Q.x) % self.Prime
        R.y = (l * (P.x - R.x) - P.y) % self.Prime
        return R
    def DecompressPoint(self, C:Point) -> Point : 
        D = Point(x=C.x,  y=self._SqrtMod(C.x**3 + self.A * C.x + self.B, self.Prime), Curve=self)
        if bool(C.y) != bool(D.y & 1) : D.y = self.Prime - D.y
        return D

class Montgomery(EllipticCurve) : 
    """ (B*y**2) % Prime = (x**3 + A*x**2 + x) % Prime """
    def CheckHasPoint(self, P:Point) -> EllipticCurve : 
        if (P==Point.O or P==self.G or ((self.B*P.y**2) % self.Prime == (P.x**3 + self.A*P.x**2 + P.x) % self.Prime)) : return self
        else : raise ValueError("point not on curve")
    def Dot(self, P:Point=Point.O, Q:Point=Point.O) -> Point : 
        if P==Point.O and Q==Point.O : return Point.Inf
        elif P==Point.O : return Q
        elif Q==Point.O : return P

        if P==Q and P.y!=0 : l = ((3 * P.x**2 + 2 * self.A * P.x + 1) * pow(2 * self.B * P.y, -1, self.Prime)) % self.Prime
        elif P!=Q and P.x!=Q.x : l = ((Q.y - P.y) * pow(Q.x - P.x, -1, self.Prime)) % self.Prime
        else : return Point.Inf

        R = Point(Curve=self)
        R.x = (self.B * l**2 - self.A - P.x - Q.x) % self.Prime
        R.y = ((2 * P.x + Q.x + self.A) * l - self.B * l**3 - P.y) % self.Prime
        return R
    def DecompressPoint(self, C:Point) -> Point : 
        D = Point(x=C.x,  y=self._SqrtMod((C.x**3 + self.A * C.x**2 + C.x) * pow(self.B, -1, self.Prime), self.Prime), Curve=self)
        if bool(C.y) != bool(D.y & 1) : D.y = self.Prime - D.y
        return D

class TwistedEdwards(EllipticCurve) : 
    """ (A*x**2 + y**2) % Prime = (1 + B*x**2*y**2) % Prime """
    def CheckHasPoint(self, P:Point) -> EllipticCurve : 
        if (P==Point.O or P==self.G or (self.A*P.x**2 + P.y**2) % self.Prime == (1 + self.B*P.x**2*P.y**2) % self.Prime) : return self
        else : raise ValueError("point not on curve")
    def Dot(self, P:Point=Point.O, Q:Point=Point.O) -> Point : 
        if P==Point.O and Q==Point.O : return Point.Inf
        elif P==Point.O : return Q
        elif Q==Point.O : return P

        R = Point(Curve=self)
        R.x = ((P.x * Q.y + P.y * Q.x) * pow(1 + self.B * P.x * Q.x * P.y * Q.y, -1, self.Prime)) % self.Prime
        R.y = ((P.y * Q.y - self.A * P.x * Q.x) * pow(1 - self.B * P.x * Q.x * P.y * Q.y, -1, self.Prime)) % self.Prime
        return R
    def DecompressPoint(self, C:Point) -> Point : 
        D = Point(x=C.x,  y=self._SqrtMod((self.A*C.x**2 - 1)* pow(self.B*C.x**2 - 1, -1, self.Prime), self.Prime), Curve=self)
        if bool(C.y) != bool(D.y & 1) : D.y = self.Prime - D.y
        return D


if __name__ == "__main__" : 
    with Weierstrass(17, 0, 7, Point(15, 13), Order=18) as curve : 
        """ https://cryptobook.nakov.com/asymmetric-key-ciphers/elliptic-curve-cryptography-ecc """
        actual = curve.G
        for _ in range(100 - 1) : actual += curve.G
        print(f"[{curve}] => expected:{curve.G*100}, actual:{actual}, compression:{curve.DecompressPoint(curve.CompressPoint(curve.G))}")

    with Montgomery(11, 5, 7) as curve : 
        points = curve.GeneratePoints()
        curve.Order = len(points)

        n = 0
        for point in points : 
            if point==Point.O : continue
            m = len(set([i*point for i in range(curve.Order)]))
            if m>n : 
                n = m
                curve.G = point
            if curve.Order==m : break

        actual = curve.G
        for _ in range(100 - 1) : actual += curve.G
        print(f"[{curve}] => expected:{curve.G*100}, actual:{actual}, compression:{curve.DecompressPoint(curve.CompressPoint(curve.G))}")   

    with TwistedEdwards(13, 10, 6) as curve :
        points = curve.GeneratePoints()
        curve.Order = len(points)

        n = 0
        for point in points : 
            if point==Point.O : continue
            m = len(set([i*point for i in range(curve.Order)]))
            if m>n : 
                n = m
                curve.G = point
            if curve.Order==m : break

        actual = curve.G
        for _ in range(100 - 1) : actual += curve.G
        print(f"[{curve}] => expected:{curve.G*100}, actual:{actual}, compression:{curve.DecompressPoint(curve.CompressPoint(curve.G))}")    
