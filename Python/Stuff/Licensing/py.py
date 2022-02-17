from importlib.abc import Loader, MetaPathFinder
from importlib.machinery import ModuleSpec
import sys
import base64

import sys
import inspect
from types import TracebackType

class MyLoader(Loader) : 
    def __init__(self, filename) : 
        # sys.tracebacklimit = 1
        # frame = inspect.currentframe().f_back.f_back.f_back.f_back.f_back
        # raise ModuleNotFoundError(f"No module named '{filename}'").with_traceback(TracebackType(None, frame, frame.f_lasti, frame.f_lineno))
        self.filename = filename        

    def create_module(self, spec) : return type(sys)(spec.name)

    def exec_module(self, module) : 
        
        exec("def wasd() : print('hello')", vars(module)) # base64.b64decode('aWYgX19uYW1lX18gPT0gIl9fbWFpbl9fIiA6IHByaW50KCJleGVjIikNCmVsc2UgOiBwcmludCgiaW1wIik=')

class MyMetaFinder(MetaPathFinder):
    def find_spec(self, fullname, path, target=None) : 
        return ModuleSpec(fullname, MyLoader(fullname), origin="<bytes>")

# sys.meta_path.append(MyMetaFinder())
# import mod
# mod.wasd()