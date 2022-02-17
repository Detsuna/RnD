from time import time
from .Units import ReadableSize

class TimeIt() : 
    instances = []
    def __new__(cls, *a, **k) : 
        instance = object.__new__(cls)
        cls.instances.append(instance)
        return instance
    def __init__(self, func) : 
        self.func = func
        self.total = 0
        self.count = 0
    def __get__(self, obj, objtype) : 
        if not hasattr(self.func, '__self__') : self.func.__self__ = obj
        return self.__call__
    def __call__(self, *a, **k) : 
        start = time()
        result = self.func(*[self.func.__self__, *a] if hasattr(self.func, '__self__') else a, **k)
        end = time()
        (self.total, self.count) = ((self.total + (end-start)), (self.count + 1))
        return result

    @classmethod
    def Summary(cls) : 
        for i in cls.instances : 
            if i.count>0 : 
                print(f"name:[{i.func.__name__}], avg:[{ReadableSize(i.total/i.count)}secs], iterations:[{i.count}], total time:[{ReadableSize(i.total)}secs]")
