import sys
import importlib

class GroveError(Exception):
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)

## Parse tree nodes for the Grove language

var_table = { }

class Expr:
    pass
    
class Num(Expr):
    def __init__(self, value):
        self.value = value

    def eval(self):
        return self.value
        
class NewObject(Expr):
    def __init__(self, value):
        self.value = value

    def eval(self):
        #print("EVAL: "+str(eval(self.value)) )
        return eval(self.value) 
        
class Addition(Expr):
    def __init__(self, child1, child2):
        self.child1 = child1
        self.child2 = child2
        
        if type(self.child1) != type(self.child2):
            raise GroveError("GROVE: the type " +str(type(self.child1)) + " does not match the type "+str(type(self.child2)))

        if not isinstance(self.child1, Expr):
            raise ValueError("CALC: expected expression but received " + str(type(self.child1)))
        if not isinstance(self.child2, Expr):
            raise ValueError("CALC: expected expression but received " + str(type(self.child2)))

    def eval(self):
        return self.child1.eval() + self.child2.eval()

class StringLiteral(Expr):
    def __init__(self,str):
        self.str = str

        for char in str:
            if not char.isalnum() and not char == "." and not char == "\"":
                raise GroveError("GROVE: expected string but received " + str)

    def eval(self):
        return self.str
        
class Method(Expr):
    def __init__(self, objName, methName, args):
        self.objName = objName
        self.methName = methName
        self.args = args

        if not objName in var_table:
            raise GroveError("GROVE: expected object name but received " + str(self.objName))

        if not methName in dir(self.objName):
            raise GroveError("GROVE: expected method but received " + str(self.methName))

    def eval(self):
        #print(var_table)
        obj = var_table[self.objName]
        #print(obj)
        fcn = getattr(obj, self.methName)
        #print(self.args)
        if len(self.args) == 0:
            return fcn()
        else:
            return fcn(self.args)

class Name(Expr):
    def __init__(self, name):
        self.name = name
        
        #PROJECT 5 CHANGES
        #print(self.name[:1])
        
        if not (self.name[:1].isalpha() or "_" in self.name[:1]):
            raise GroveError("GROVE: Must start with alphabetic characters or underscore")
        if len(self.name[1:]) > 0 and not (self.name[1:].isalnum() or "_" in self.name[1:]):
            raise GroveError("GROVE: Must only contain alphanumeric characters or underscore")

    def getName(self):
        return self.name

    def eval(self):
        if self.name in var_table:
            return var_table[self.name]
        else:
            raise ValueError("CALC: undefined variable " + self.name)
        
class Stmt:
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

        #print(name.eval())
        if isinstance(self.expr, NewObject):
            pass
        elif not isinstance(self.expr, Expr):
            raise ValueError("CALC: expected expression but received " + str(type(self.expr)))
        elif not isinstance(self.name, Name):
            raise ValueError("CALC expected expression but received " + str(type(self.expr)))
        #print(expr)
        
        
        #if expr[0] == "+":
        #    self.expr = Addition[1,len(expr)]
        # else:
        #     self.expr = Subtraction[1, len(expr)]

    def eval(self):
        if isinstance(self.expr,NewObject):
            var_table[self.name.getName()] = self.expr.eval()
            pass
        else:
            var_table[self.name.getName()] = self.expr.eval()

class ImportModule(Stmt):
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

    def eval(self):
        importing = importlib.import_module(self.expr.getName())
        globals().update({self.expr.getName(): importing})
        return None

class Exit(Stmt):
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

    def eval(self):
        sys.exit()

class New(Stmt):
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

    def eval(self):
        sys.exit()