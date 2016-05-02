exec(open("calc_parse.py").read())

while True:
    ln = input("Calc>>")
    root = parse(ln)
    res = root.eval()
    if not res is None:
        print(res)