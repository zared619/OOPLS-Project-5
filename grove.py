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
        choice = input("Grove>>")
        root = parse(choice)
        evaluation = root.eval()
        if isinstance(evaluation, Expr):
            print(evaluation)