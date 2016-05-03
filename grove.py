'''Project 5
5-2-16
OOPLS
Zared Hollabaugh
Caelan Mayberry
Stuart Bowman
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