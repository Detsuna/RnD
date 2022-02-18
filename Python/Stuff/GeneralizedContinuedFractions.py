from time import time
from math import gcd
from warnings import simplefilter, warn


class GeneralizedContinuedFractionValueWarning(UserWarning) : pass
simplefilter('always', GeneralizedContinuedFractionValueWarning)


class GeneralizedContinuedFractionIterator() : 
    def __init__(self, *_, a, b, radix=10, nNext=(lambda n : (n + 1)), timeout=1.0) : 
        self.timeout = timeout

        self.n = 0
        self.nNext = nNext
        self.radix = radix

        self.b = b
        self.a = a
        self.Aprev = 1
        self.Bprev = 0
        self.A = self.b(self.n)
        self.B = 1
    def __iter__(self) : return self
    def __next__(self) : 
        start = time()
        while True : 
            if time()-start>self.timeout : raise TimeoutError("Convergence too slow")
            self.n = self.nNext(self.n)
            (self.Aprev, self.Bprev, self.A, self.B) = (
                self.A,
                self.B,
                (self.b(self.n) * self.A + self.a(self.n) * self.Aprev),
                (self.b(self.n) * self.B + self.a(self.n) * self.Bprev)
            )
            # (premature(?)) optimization : shrink continuants ("reduce space required" to store the "super big" numbers)
            D = gcd(self.Aprev, self.Bprev, self.A, self.B)                
            if D>1 : 
                warn(f"shrinking continuants with gcd:[{D}]...", GeneralizedContinuedFractionValueWarning)
                (self.Aprev, self.Bprev, self.A, self.B) = (self.Aprev//D, self.Bprev//D, self.A//D, self.B//D)

            (Qprev, Rprev), (Q, R) = divmod(self.Aprev, self.Bprev), divmod(self.A, self.B)
            if Qprev==Q : 
                (self.Aprev, self.A) = (self.radix * Rprev, self.radix * R)
                if Q>=self.radix : warn(f"emitting value:[{Q}] equal or larger than base:[{self.radix}]", GeneralizedContinuedFractionValueWarning)
                return Q

class Stringify(GeneralizedContinuedFractionIterator) : 
    def __Process(self) : 
        c = 0 
        while len(self.digits)<3 or self.digits[-1]>=(self.radix**(len(self.digits)-1)) :
            self.digits.append(super().__next__())
            c += 1
        i = 0
        while i<len(self.digits) : 
            i += 1
            if not isinstance(self.digits[-i], int) : continue
            (q, r) = divmod(self.digits[-i], self.radix)
            if q>0 : 
                try : (self.digits[-i-1], self.digits[-i]) = (self.digits[-i-1] + q, r)
                except IndexError : (self.digits, self.digits[-i]) = ([q] + self.digits, r)            
        return c

    def __init__(self, *_, Format=(lambda i : i if isinstance(i, str) else hex(i)[2:].upper()), floatPointChar=None, **k) : 
        super().__init__(**k)
        self.Format = Format
        self.digits = []
        c = self.__Process()
        if floatPointChar is not None : self.digits.insert((len(self.digits) - c + 1), floatPointChar) # decimal pt
    def __next__(self) : 
        self.__Process()
        (result, self.digits) = (self.digits[0], self.digits[1:])
        return self.Format(result)


class GoldenRatioDigitGenerator(Stringify) : 
    def __init__(self, *_, **k) : 
        f = (lambda k : 1)
        super().__init__(a=f, b=f, nNext=f, **k)

class PiDigitGenerator(Stringify) : 
    def __init__(self, *_, **k) : 
        a = (lambda k : 4 if k==1 else ((k - 1)**2))
        b = (lambda k : 0 if k==0 else (k + k - 1))
        super().__init__(a=a, b=b, **k)


class ExponentialDigitGenerator(Stringify) : 
    def __init__(self, *_, z=1, **k) : 
        (x, y) = z if isinstance(z, (tuple, list)) else (z, 1)
        a = (lambda k : (2 * x) if k==1 else (x**2))
        b = (lambda k : 1 if k==0 else (2 * y - x) if k==1 else ((k * 4 - 2) * y))
        super().__init__(a=a, b=b, **k)

class NaturalLogDigitGenerator(Stringify) : 
    def __init__(self, *_, z=1, **k) : 
        neg = False
        if isinstance(z, (tuple, list)) : 
            neg = True if z[1]>z[0] else False
            (x, y) = z if neg is False else reversed(z)
            x = x - y
        else : (x, y) = (z - 1, 1)
        a = (lambda k : (2 * x) if k==1 else -(((k - 1) * x)**2))
        b = (lambda k : 0 if k==0 else ((k + k - 1) * (2 * y + x)))
        super().__init__(a=a, b=b, **k)
        if neg : self.digits.insert(0, "-")


class NthRootDigitGenerator(Stringify) : 
    def __init__(self, *_, z=1, n=1,**k) : 
        y = z - 1
        a = (lambda k : (2 * y) if k==1 else -(((k - 1)**2 * n**2 - 1) * y**2))
        b = (lambda k : 1 if k==0 else (n * (2 + y) - y) if k==1 else ((k + k - 1) * n * (2 + y)))
        super().__init__(a=a, b=b, **k)


if __name__ == "__main__" : 
    simplefilter('ignore', GeneralizedContinuedFractionValueWarning)

    for cls in [PiDigitGenerator, GoldenRatioDigitGenerator, ExponentialDigitGenerator] : 
        example = {
            "generators" : {
                "base02": cls(radix=2, floatPointChar="."),
                "base10": cls(radix=10, floatPointChar="."),
                "base16": cls(radix=16, floatPointChar=".")
            }, "results" : {
                "base02": "",
                "base10": "",
                "base16": ""
            }
        }
        for i in range(100) : 
            for key in ["base02", "base10", "base16"] : 
                example["results"][key] += next(example["generators"][key])
        print(f"{cls.__name__}\n================")
        for (k,v) in example["results"].items() : 
            print(f"{k}: {v}")
        print()

    print(f"\neˣ\n================")
    for i in [1, 5, 99] : 
        print(f"x = {i:3d}: ", end="")
        g = ExponentialDigitGenerator(z=i, floatPointChar=".")
        for _ in range(100): print(next(g), end="")
        print()

    print(f"\nln(x/y)\n================")
    print(f" ln(1) : ", end="")
    g = NaturalLogDigitGenerator(floatPointChar=".")
    for _ in range(100): print(next(g), end="")
    print()
    for i in [2, 3] : 
        print(f"ln({i}/1): ", end="")
        g = NaturalLogDigitGenerator(z=i, floatPointChar=".")
        for _ in range(100): print(next(g), end="")
        print()
        print(f"ln(1/{i}): ", end="")
        g = NaturalLogDigitGenerator(z=(1,i), floatPointChar=".")
        for _ in range(100): print(next(g), end="")
        print()

    print(f"\nⁿ√z\n================")
    for i in range(1 ,6) : 
        print(f"{i}√{i}: ", end="")
        g = NthRootDigitGenerator(z=i,n=i, floatPointChar=".")
        for _ in range(47) : print(next(g), end="")
        j=i**i
        print(f", {f'{i}√{j}':>6}: ", end="")        
        g = NthRootDigitGenerator(z=j,n=i, floatPointChar=".")
        for _ in range(47) : print(next(g), end="")
        print()
