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

class LogYofbaseXDigitGenerator(Stringify) : 
    def __init__(self, *_, z=1, **k) : 
        a = (lambda k : (2 * (z - 1)) if k==1 else -(((k - 1) * (z - 1))**2))
        b = (lambda k : 0 if k==0 else ((k + k - 1) * (2 + z - 1)))
        super().__init__(a=a, b=b, **k)


if __name__ == "__main__" : 
    simplefilter('ignore', GeneralizedContinuedFractionValueWarning)

    g = GoldenRatioDigitGenerator(radix=2)
    for i in range(8097): print(next(g), end="")




# from Stuff.GeneralizedContinuedFractions import PiDigitGenerator

# example = {
#     "generators" : {
#         "base02": PiDigitGenerator(base=2),
#         "base10": PiDigitGenerator(),
#         "base16": PiDigitGenerator(base=16)
#     }, "results" : {
#         "base02": "",
#         "base10": "",
#         "base16": ""
#     }
# }
# for i in range(100):
#     for key in ["base02", "base10", "base16"] : 
#         example["results"][key] += next(example["generators"][key])
# for (k,v) in example["results"].items() : 
#     print(f"{k}: [{v}]")


# π in base 2, 8, 10, 16
# 11.00100 10000 11111 10110 10101 00010 00100 00101 10100 01100 00100 01101 00110 00100 11000 11001 10001 01000 10111 00000
# 3.11037 55242 10264 30215 14230 63050 56006 70163 21122 01116 02105 14763 07200 20273 72461 66116 33104 50512 02074 61615
# 3.14159 26535 89793 23846 26433 83279 50288 41971 69399 37510 58209 74944 59230 78164 06286 20899 86280 34825 34211 70679
# 3.243F6 A8885 A308D 31319 8A2E0 37073 44A40 93822 299F3 1D008 2EFA9 8EC4E 6C894 52821 E638D 01377 BE546 6CF34 E90C6 CC0AC

# Φ
# 1.618033988749894848204586834365638117720309179805762862135448622705260462818

# e, e^5, e^99
# 2.7182818284590452353602874713526624977572470936999595749669676277240766303535475945713821785251664274
# 148.41315910257660342111558004055227962348766759387898904675284511091206482095857607968840945989902
# 9889030319346946770560030967138037101405082.60719933517340199715371109444700740600600675067295103719703
# 

# ln(10)
# 2.30258509299404568401799145468436420760110148862877297603332790096757260967735248023599720508959829834
# -0.693147180559945309417232121458176568075500134360255254120680009493393621969694715605863326996418687542
#  0.693147180559945309417232121458176568075500134360255254120680009493393621969694715605863326996418687542
# -1.09861228866810969139524523692252570464749055782274945173469433363749429321860896687361575481373208879