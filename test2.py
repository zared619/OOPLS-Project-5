
exec(open("grove_parse.py").read())

root = parse('set x1 = "hi"')
evaluation = root.eval()
root = parse('+ ( x1 ) ( "bye" )')
evaluation = root.eval()
print(evaluation)
