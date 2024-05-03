from os import system as sys
from os import path as p
import re

if p.exists('./main.pspy'):
    codefile = open("main.pspy", "r").read()
elif p.exists('./main.pseudopy'):
    codefile = open("main.pseudopy", "r").read()
else:
    print("No [main.pspy] or [main.pseudopy] file found.")
    exit()

code = [i.strip() for i in codefile.splitlines() if i.strip() != ""]

def parse(code):
    final = ""
    indent = 0
    for line in range(0,len(code)):
        arrA = [["([A-Za-z0-9]+) = ([A-Za-z0-9]+) to ([A-Za-z0-9]+)", "\\1 in range(\\2, \\3)"], ["function ([A-Za-z0-9]+)", "def \\1"], ["([A-Za-z0-9 ]+)MOD([A-Za-z0-9 ]+)", "\\1%\\2"], ["([A-Za-z0-9 ]+)DIV([A-Za-z0-9 ]+)", "\\1//\\2"]]
        for a in range(0,len(arrA)):
            code[line] = re.sub(arrA[a][0], arrA[a][1], code[line])
        arrB = [["function$", "function"], ["MOD$", "MOD"], ["DIV$", "DIV"]]
        for b in range(0,len(arrB)):
            code[line] = code[line].replace(arrB[b][0], arrB[b][1])
    for j, k in enumerate(code):
        for i, v in enumerate(k.splitlines()):
            v = v.strip()
            if (v == "endfunction") or (v == "endif") or (v == "endwhile"):
                indent -= 1
                v = ""
                continue
            elif re.search("next ([A-Za-z0-9]+)",v):
                if v[0] == "n":
                    indent -= 1
                    v = ""
                    continue
            if v.split()[0] in ["if", "elif", "else", "for", "while", "def", "class", "try", "except", "finally"]:
                v = "    " * indent + v
                indent += 1
            else: v = "    " * indent + v
            final += v + "\n"

    return "\n".join([i for i in final.splitlines() if i != ""])

exec(parse(code), {"pspy_ver": 1.4})
