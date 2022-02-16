from __future__ import annotations
from abc import ABC, abstractmethod


class Point() : 
    Inf = O = None
    def __init__(self, x:int=None, y:int=None, Curve:EllipticCurve=None) : (self.x, self.y, self.Curve) = (x, y, Curve)
    def __eq__(self, other:object) -> bool : return (isinstance(other, Point) and self.x==other.x and self.y==other.y)
    def __repr__(self) -> str : return f"{self.__class__.__name__}({', '.join([f'{k}={v}' for (k,v) in vars(self).items()])})"
Point.Inf = Point.O = Point()


class EllipticCurve(ABC) : 
    def __init__(self, Prime:int, A:int, B:int, G:Point=None, Order:int=None, Cofactor:int=None) : 
        self.Prime = Prime # Modulus
        self.A = A
        self.B = B
        self.G = G
        self.Order = Order # N
        self.Cofactor = Cofactor # N/R(Subgroups); esp TwistedEdwards(?) = 4(?)

        self.G.Curve = self
    def __repr__(self) -> str : return self.__class__.__name__

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
    def HasPoint(self, P:Point) -> bool : raise NotImplementedError

    @abstractmethod
    def Dot(self, P:Point=Point.O, Q:Point=Point.O) -> Point : raise NotImplementedError

    @abstractmethod
    def CompressPoint(self, D:Point) :  raise NotImplementedError
    @abstractmethod
    def DecompressPoint(self, C:Point) -> Point : raise NotImplementedError


class Weierstrass(EllipticCurve) :
    """ (y**2) % Prime = (x**3 + A*x + B) % Prime """
    def HasPoint(self, P:Point) -> bool : return (P==Point.O or ((P.y**2) % self.Prime == (P.x**3 + self.A*P.x + self.B) % self.Prime))
    def Dot(self, P:Point=Point.O, Q:Point=Point.O) -> Point : 
        if P==Point.O and Q==Point.O : return Point.Inf
        elif P==Point.O : return Q
        elif Q==Point.O : return P

        if P==Q : l = ((3 * P.x**2 + self.A) * pow(2 * P.y, -1, self.Prime)) % self.Prime
        else : 
            try : l = ((Q.y - P.y) * pow(Q.x - P.x, -1, self.Prime)) % self.Prime
            except ValueError : return Point.Inf

        R = Point(Curve=self)
        R.x = (l**2 - P.x - Q.x) % self.Prime
        R.y = (l * (P.x - R.x) - P.y) % self.Prime
        return R

    def CompressPoint(self, D:Point) : return Point(x=D.x, y=(D.y & 1))
    def DecompressPoint(self, C:Point) : 
        D = Point(x=C.x,  y=self._SqrtMod(pow(C.x, 3, self.Prime) + self.A * C.x + self.B, self.Prime))
        if bool(C.y) != bool(D.y & 1) : D.y = self.Prime - D.y
        return D

class Montgomery(EllipticCurve) : 
    """ (B*y**2) % Prime = (x**3 + A*x**2 + x) % Prime """
    def Dot(self, P:Point=Point.O, Q:Point=Point.O) -> Point : 
        if P==Point.O and Q==Point.O : return Point.Inf
        elif P==Point.O : return Q
        elif Q==Point.O : return P

        if P==Q : l = ((3 * P.x**2 + 2 * self.A + 1) * pow(2 * P.y, -1, self.Prime)) % self.Prime
        else : l = ((Q.y - P.y) * pow(Q.x - P.x, -1, self.Prime)) % self.Prime

        R = Point(Curve=self)
        R.x = (self.B * l**2 - self.A - P.x - Q.x) % self.Prime
        R.y = ((2 * P.x + Q.x + self.A) * l - self.B * l**3 - P.y) % self.Prime
        return R

class TwistedEdwards(EllipticCurve) : 
    """ (A*x**2 + y**2) % Prime = (1 + B*x**2*y**2) % Prime """
    def Dot(self, P:Point=Point.O, Q:Point=Point.O) -> Point : 
        R = Point(Curve=self)
        d = pow(1 - self.B * P.x * Q.x * P.y * Q.y, -1, self.Prime)
        R.x = ((P.x * Q.y + P.y * Q.x) * d) % self.Prime
        R.y = ((P.y * Q.y - self.A * P.x * Q.x) * d) % self.Prime
        return R


class ECC() : 
    def __init__(self, Curve:EllipticCurve, D:int, Q:Point=None) : 
        self.Curve = Curve
        self.D = D
        self.Q = Q
    def __del__(self) : del self.__dict__
    def __enter__(self) : return self
    def __exit__(self, type, value, tb) : self.__del__()

    def EnCrypt(self, p) : return self.Crypt(m=p, key=self.Exponent)
    def DeCrypt(self, c) : return self.Crypt(m=c, key=self.D)
    def Crypt(self, m, key) : pass 


if __name__ == "__main__" : 
    prime = 17
    p = Point(15, 13)
    curve = Weierstrass(prime, 0, 7, G=p)
    for _ in range(prime + 1) : 
        p = curve.Dot(curve.G, p)
        print(f"{p}, {curve.HasPoint(p)}")
    # p = Point(10, 15)
    # p = curve.CompressPoint(p)
    # print(f"Compressed: {p}")
    # p = curve.DecompressPoint(p)
    # print(f"Decompressed: {p}")
    pass
