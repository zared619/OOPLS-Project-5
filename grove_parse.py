exec(open("grove_lang.py").read())

# Utility methods for handling parse errors
def check(condition, message = "Unexpected end of expression"):
    """ Checks if condition is true, raising a ValueError otherwise """
    if not condition:
        raise GroveError("GROVE: " + message)
        
def expect(token, expected):
    """ Checks that token matches expected
        If not, throws a ValueError with explanatory message """
    if token != expected:
        check(False, "Expected '" + expected + "' but found '" + token + "'")
def is_expr(x):
    if not isinstance(x, Expr):
        check(False, "Expected expression but found " + str(type(x)))        
# Checking for integer        
def is_int(s):
    """ Takes a string and returns True if in can be converted to an integer """
    try:
        int(s)
        return True
    except ValueError:
        return False
       
def parse(s):
    """ Return an object representing a parsed command
        Throws ValueError for improper syntax """
    # TODO
    (root, remainingTokens) = parse_tokens(s.split())
    #print(str(type(root)))
    #print("Remaining Tokens: "+remainingTokens)
    #The parse call should have used all the tokens
    check(len(remainingTokens) == 0, "Expected end of command but found '"+ " ".join(remainingTokens)+ "'")

    return root

def parse_tokens(tokens):
    """ Returns a tuple:
        (an object representing the next part of the expression,
         the remaining tokens)
    """
    
    check(len(tokens) > 0)
        
    start = tokens[0]
    # TODO: parse the next part of the expression
    if is_int(start):
        return  ( Num(int(start)),tokens[1:])
    elif start in ["+"]:
        expect(tokens[1], "(")
        (child1, tokens) = parse_tokens(tokens[2:])
        check(len(tokens) > 1)
        expect(tokens[0], ")")
        expect(tokens[1], "(")
        (child2, tokens) = parse_tokens(tokens[2:])
        check(len(tokens) >0)
        expect(tokens[0], ")")

        if start == "+":
            return (Addition(child1, child2), tokens[1:])
        # else:
        #     return (Subtraction(child1, child2), tokens[1:])

    elif "\"" in start[0]:
        varname = tokens[0]
        check(varname.count("\"") == 2,"Should contain exactly two quotation marks")
        varname = varname.replace("\"","")
        
        return (StringLiteral(varname),tokens[1:])

    elif start == "set":
        (varname, tokens) = parse_tokens(tokens[1:])
        #print(tokens)
        expect(tokens[0], "=")
        (child, tokens) = parse_tokens(tokens[1:])
        return (Stmt(varname, child), tokens)
    elif start == "import":
        (varname, tokens) = parse_tokens(tokens[1:])
        expect(len(tokens),0)#tokens should be empty now
        return ImportModule(varname, varname), tokens[1:]

    elif start == "call":
        expect(tokens[1], "(")
        child = tokens[2]
        if not child in var_table:
            raise GroveError("GROVE: variable does not exist. Received " + str(child))
        method = tokens[3]
        args = []
        iter = 4
        #print(tokens)
        while(len(tokens[iter:]) > 1):
            myToken = tokens[iter]
            if isinstance(myToken, str):
                myToken = myToken.replace("\"","")
            args.append(myToken)
            iter += 1

        if "call" in args:
            args = parse_tokens(args)

        argIter = 0
        argList = list(args)
        for arg in args:
            if isinstance(arg,Method):
                argList[argIter] = arg.eval()
            if arg == list():
                argList.remove(list())
            argIter += 1

        expect(tokens[iter], ")")
        check(len(tokens) > 1)
        return (Method(child, method, args),tokens[iter+1:])
    elif start == "new":
        #print(str(tokens))
        
        splitTokens = tokens[1].split(".")
        (varname, splitTokens) = parse_tokens(splitTokens)
        
        if len(splitTokens) > 0:
            #print(splitTokens)
            (child, splitTokens) = parse_tokens(splitTokens)
            #print(splitTokens)
            return (NewObject(varname.getName()+"."+child.getName()), splitTokens[1:])
        else:
            return (NewObject(varname.getName()), splitTokens[1:])
        
       # 
        #return (NewObject(varname.getName()), tokens[1:])
    elif start == "exit" or start == "quit":
        return Exit(start, start), tokens[1:]
    else:
        #print(start)
        #check(start[:1].isalpha(), "Variable names must be alphabetic.")
        #Name checks itself for isalpha/isnumeric
        return (Name(start), tokens[1:])

        

# Testing code
# if __name__ == "__main__":
#     # First try some things that should work
#     cmds = [" + ( 3 ) ( 12 ) ",
#             " - ( 5 ) ( 2 )",
#             " + ( 15 ) ( - ( 3 ) ( 8 ) ) ",
#             "set foo = 38",
#             "foo",
#             "set bar = + ( 22 ) ( foo )",
#             "bar"]
            
#     answers = [ 15,
#                 3,
#                 10,
#                 None,
#                 38,
#                 None,
#                 60 ]
    
#     for i in range(0, len(cmds)):
#         root = parse(cmds[i])
#         result = root.eval()
#         check(result == answers[i], "TEST FAILED for cmd " + cmds[i] + 
#             ";  result was " + str(result) + " instead of " + str(answers[i]))
    
#     # Testing for all errors is beyond our scope,
#     # but we check a few
#     bad_cmds = [ " ",
#                  "not-alpha",
#                  " + ( nope ) ( 3 ) ",
#                  " 3 + 3 ",
#                  " + ( 5 ) ( 4 ) foo ",
#                  " + ( set x = 6 ) ( 7 )" ]
        
#     for c in bad_cmds:
#         try:
#             root = parse(c)
#             result = root.eval()
#             check(False, "Did not catch an error that we should have caught")
#         except ValueError:
#             pass

# if __name__ == "__main__":
#     while True:
#         #print(globals())
#         #print(var_table)
#         #print()
#         choice = input("Grove>>")
#         try:
#             root = parse(choice)
#             evaluation = root.eval()
#             #print(evaluation)
#             if evaluation != None:
#                 print(evaluation)
#         except GroveError as e:
#             print(e)
#         except ValueError as e:
#             print(e)
#         except NameError as e:
#             print(e)

if __name__ == "__main__":
    while True:
        #print(globals())
        #print(var_table)
        #print()
        choice = input("Grove>>")
        try:
            root = parse(choice)
            evaluation = root.eval()
            #print(evaluation)
            if evaluation != None:
                print(evaluation)
        except GroveError as e:
            print(e)
        except ValueError as e:
            print(e)
        except NameError as e:
            print(e)