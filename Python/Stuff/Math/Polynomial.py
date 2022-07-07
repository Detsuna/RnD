from collections import defaultdict
from numbers import Number


class Polynomial(Number, defaultdict['Polynomial.VariablesExponents', int]) : 
    " e.g. 5x³y⁴ -2x -6 = Polynomial({Polynomial.VariablesExponents({'x': 3, 'y': 4}): 5, Polynomial.VariablesExponents({'x': 1}): -2, Polynomial.VariablesExponents({'': 1}): -6}) "

    class VariablesExponents(defaultdict[str, int]) : 

        def __init__(self, values={}) : 
            defaultdict.__init__(self, int)
            values = { k.strip():v for k, v in values.items()}
            for k in sorted(values) : 
                if len(k)>1 : raise ValueError(f"Variable(s) should only consist of at most 1 character : len('{k}')={len(k)}")
                if k!="" and (1*values[k])!=0 : self[k] = values[k]
            if ("" in values) : self[""] = values[""] ** 0

        def __repr__(self) : return f"""{self.__class__.__qualname__}({dict.__repr__(self)})"""
        @staticmethod
        def __SuperScript(text) : return str.translate(text, str.maketrans("0123456789.-()", "⁰¹²³⁴⁵⁶⁷⁸⁹·⁻⁽⁾"))
        def __str__(self) :
            segments = ["".join([
                k,
                (self.__SuperScript(str(self[k])) if k and self[k]!=1 else "")
            ]) for k in self]
            return "".join(segments)

        def __hash__(self) : return hash(str(self))
        def __eq__(self, other) : return (str(self)==str(other))
        def __lt__(self, other) : 
            keys = sorted([(k if k else chr(0x110000 - 1)) for k in dict(self) | dict(other)])
            s = [(self[k] if k in self else 0) for k in keys]
            o = [(other[k] if k in other else 0) for k in keys]
            for i in range(min(len(s), len(o))) : 
                if s[i]!=o[i] : return s[i]<o[i]
                if s[i]==o[i] and len(s)!=len(o) : return len(s)>len(o)
            return False
        def __le__(self, other) : return self.__eq__(other) | self.__lt__(other)


        def __add__(self, other) :
            result = dict(self) | dict(other)
            for k in result : result[k] = (Polynomial.VariablesExponents(self)[k] + Polynomial.VariablesExponents(other)[k])
            return Polynomial.VariablesExponents(result)

        def __sub__(self, other) :
            result = dict(self) | dict(other)
            for k in result : result[k] = (Polynomial.VariablesExponents(self)[k] - Polynomial.VariablesExponents(other)[k])
            return Polynomial.VariablesExponents(result)

    def __init__(self, values={}) : 
        defaultdict.__init__(self, int)
        for k in values : 
            if (1*values[k])!=0 : self[k] = values[k]

    def __repr__(self) : return f"""{self.__class__.__qualname__}({dict.__repr__(self)})"""
    def __str__(self) -> str : 
        segments = sorted([k for k in self], reverse=True)
        segments = ["".join([
            (" -" if self[k]<0 else " +"),
            str(abs(self[k])) if (abs(self[k])!=1 or not str(k)) else "",
            str(k)
        ]) for k in segments]
        return ("".join(segments)).lstrip(" ").lstrip("+") if segments else "0"
    def Eval(self, vars={}) : 
        result = Polynomial(self)
        const = Polynomial.VariablesExponents({"":0})
        for v in vars : 
            for ve in list(result) : 
                if v in ve : 
                    r = Polynomial.VariablesExponents(ve)
                    del r[v]
                    result[r] += result[ve] * vars[v]**ve[v]
                    del result[ve]
        result = Polynomial(result)
        if len(result)==1 and const in result : return result[const]
        else : return result

    
    def __add__(self, other) : 
        result = Polynomial(self)
        for k in other : result[k] = (result[k] + other[k])
        return Polynomial(result)
    def __radd__(self, other) : return self.__add__(other)
    def __iadd__(self, other) : return self.__add__(other)

    def __sub__(self, other) : 
        result = Polynomial(self)
        for k in other : result[k] = (result[k] - other[k])
        return Polynomial(result)
    def __rsub__(self, other) : return self.__sub__(other)
    def __isub__(self, other) : return self.__sub__(other)

    def __mul__(self, other) :
        result = Polynomial()
        for s in list(self) : 
            for o in list(other) : 
                result[s+o] = (result[s+o] + (self[s] * other[o]))
        return Polynomial(result)
    def __rmul__(self, other) : return self.__mul__(other)
    def __imul__(self, other) : return self.__mul__(other)

    def __truediv__(self, other) : 
        quotient, remainder, divisorMaxKey = Polynomial(), Polynomial(self), sorted(other, reverse=True)[0]

        maxRemainderKey = sorted(remainder, reverse=True)[0]
        coefficientQ, coefficientR = divmod(remainder[maxRemainderKey], other[divisorMaxKey])
        while divisorMaxKey<=maxRemainderKey and coefficientR==0: 
            partQuotient = Polynomial({ maxRemainderKey-divisorMaxKey : coefficientQ  })
            subtractable = other * partQuotient

            quotient += partQuotient
            remainder -= subtractable

            if not len(remainder) : break
            maxRemainderKey = sorted(remainder, reverse=True)[0]
            coefficientQ, coefficientR = divmod(remainder[maxRemainderKey], other[divisorMaxKey])
        return quotient, remainder


if __name__ == "__main__" : 
    a = Polynomial({
        Polynomial.VariablesExponents({ "x":1 }):1,
        Polynomial.VariablesExponents({ "y":1 }):1,
    })
    b = Polynomial({
        Polynomial.VariablesExponents({ "x":1 }):1,
        Polynomial.VariablesExponents({ "y":1 }):-1,
    })
    print(f"a=[{a}], b=[{b}]")
    print(f"================================")
    print(f"Addition        : [{a+b}]")
    print(f"Subtraction     : [{a-b}]")
    print(f"Multiplication  : [{a*b}]")

    a = Polynomial({
        Polynomial.VariablesExponents({ "x":3 }):2,
        Polynomial.VariablesExponents({ "x":2, "y":1 }):12,
        Polynomial.VariablesExponents({ "x":1, "y":2 }):15,
        Polynomial.VariablesExponents({ "y":3 }):-9,
    })
    b = Polynomial({
        Polynomial.VariablesExponents({ "x":1 }):1,
        Polynomial.VariablesExponents({ "y":1 }):3,
    })
    q, r = a/b
    print(f"a=[{a}], b=[{b}], a/b=[{q}, {r}]")

    
    a = Polynomial({
        Polynomial.VariablesExponents({ "x":2 }):1,
        Polynomial.VariablesExponents({ "y":2 }):-1,
    })
    b = Polynomial({
        Polynomial.VariablesExponents({ "x":1 }):1,
    })
    c = Polynomial({
        Polynomial.VariablesExponents({ "y":1 }):1,
    })
    qb, rb, qc, rc = (*(a/b) , *(a/c))
    print(f"a/b=[{qb}, {rb}], a/c=[{qc}, {rc}]")


    e = {"x":2, "y":1}
    print(f"a.Eval(e)=[{a.Eval(e)}]")