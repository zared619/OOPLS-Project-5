'''Project 5
5-2-16
OOPLS
Zared Hollabaugh
Caelan Mayberry
Stuart Bowman

Is your Grove interpreter using a static or dynamic type system? Briefly explain what aspects of the
interpreter make it so.

    Dynamic. Types can be defined and changed at runtime, meaning that types are not rigidly set at compile time
    and can be changed. For example, the user can run \
        set X1 = 5
        and then later run
        set X1 = "hi"


'''

exec(open("grove_parse.py").read())

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