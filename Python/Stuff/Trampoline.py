class Trampoline() : 
    called = False
    def __init__(self, func) : 
        self.func = func
    def __get__(self, obj, objtype) : 
        if not hasattr(self.func, '__self__') : self.func.__self__ = obj
        return self.__call__
    def __call__(self, *args, **kwargs) : 
        r = (self.func, [self.func.__self__, *args] if hasattr(self.func, '__self__') else args, kwargs)
        if not Trampoline.called : 
            try :
                Trampoline.called = True
                while isinstance(r, tuple) and callable(r[0]) and isinstance(r[1], (tuple, list)) and isinstance(r[2], dict) : 
                    (r, a, k) = r
                    if isinstance(r, Trampoline) : r = r.func
                    r = r(*a, **k)
            except Exception : raise
            finally : Trampoline.called = False
        return r
