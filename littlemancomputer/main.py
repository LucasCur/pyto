import os
import re
import json
os.system("clear")

f = open("main.lmc", "r")
x = enumerate(f)
line = []
mneu = [
        ["([A-Za-z0-9 ]+) LDA ([A-Za-z0-9 ]+)", "def \\1():|$|  accumulator = \\2"],
        ["LDA ([A-Za-z0-9 ]+)", "accumulator = \\1"],
        ["([A-Za-z0-9 ]+) STA ([A-Za-z0-9 ]+)", "def \\1():|$|  \\2 = accumulator"],
        ["STA ([A-Za-z0-9 ]+)", "\\1 = accumulator"],
        ["([A-Za-z0-9 ]+) ADD ([A-Za-z0-9 ]+)", "def \\1():|$|  accumulator += \\2"],
        ["ADD ([A-Za-z0-9 ]+)", "accumulator += \\1"],
        ["([A-Za-z0-9 ]+) SUB ([A-Za-z0-9 ]+)", "def \\1():|$|  accumulator -= \\2"],
        ["SUB ([A-Za-z0-9 ]+)", "accumulator -= \\1"],
        ["([A-Za-z0-9 ]+) INP", "def \\1():|$|  accumulator = int(input(\"Input: \"))"],
        ["INP", "accumulator = int(input(\"Input: \"))"],
        ["([A-Za-z0-9 ]+) OUT", "def \\1():|$|print(accumulator)"],
        ["OUT", "print(accumulator)"],
        ["([A-Za-z0-9 ]+) HLT", "def \\1():|$|exit()"],
        ["HLT", "exit()"],
        ["BRZ ([A-Za-z0-9 ]+)", "if accumulator == 0:|$|\\1()"],
        ["BRP ([A-Za-z0-9 ]+)", "if accumulator >= 0:|$|\\1()"],
        ["BRA ([A-Za-z0-9 ]+)", "\\1()"],
        ["([A-Za-z0-9 ]+) DAT ([A-Za-z0-9 ]+)", "\\1 = \\2"],
        ["([A-Za-z0-9 ]+) DAT", "\\1 = 0"]
       ]

torun = ""

def filelen(file):
  count = 0 
  with open(file) as f:
    for k in f:
      count += 1
  return count

modifier = 0

print("  ┏ LMC CODE\n  ┃")
counter = 0
with open("main.lmc") as f:
  for k in f:
    line.append("")
    counter += 1
    if counter == filelen("main.lmc"):
      print(str(counter) + " ┗",k.strip())
    elif k == "":
      print(str(counter) + " ┃",k.strip())
    else:
      print(str(counter) + " ┣",k.strip())
print("\n\n  ┏ CONVERTED PYTHON\n  ┃")
wrapped = False
for i, j in x:
  displayi = int(i + int(modifier))
  line[i] = str(j).strip()
  for a in range(0, len(mneu)):
    if len(j) > 0:
      line[i] = re.sub(mneu[a][0], mneu[a][1], line[i])
      if "|$|" in line[i]:
        wrapped = True
  if wrapped == True:
    wrapped = False
    _temp = line[i].split("|$|")
    if i == len(line)-1:
      print(str(displayi+1) + " ┣",_temp[0])
      print(str(displayi+2) + " ┗  ",_temp[1])
      modifier += 1
    else:
      print(str(displayi+1) + " ┣",_temp[0])
      print(str(displayi+2) + " ┣  ",_temp[1])
      modifier += 1
  else:  
    if i == len(line)-1:
      print(str(displayi+1) + " ┗",line[i])
    elif line[i] == "":
      print(str(displayi+1) + " ┃",line[i])
    else:
      print(str(displayi+1) + " ┣",line[i])
  if "|$|" in line[i]:
    _temp = line[i].split("|$|")
    torun = torun + _temp[0] + "\n"
    torun = torun + "  " + _temp[1] + "\n"
  else:
    torun = torun + line[i] + "\n"
  f = open("temp.dat", "a")
  if "|$|" in line[i]:
    _temp = line[i].split("|$|")
    f.write(_temp[0] + "\n")
    f.write("  " + _temp[1] + "\n")
  else:
    f.write(line[i] + "\n")
  f.close()

run = input("\n┓\n┃ Would you like to run this code? y/n: ")
print("┛")
if run.lower() == "y":
  print("")
  exec(torun.replace("exit()","#exit()"))

save = input("\n┓\n┃ Would you like to save this code? y/n: ")
if save.lower() == "y":    
  os.remove("converted.py")
  with open('temp.dat','r') as firstfile, open('converted.py','w') as secondfile:
    for line in firstfile:
      secondfile.write(line)
  print("┃ Saved to 'converted.py'\n┛")
else:
  print("┛")
os.remove("temp.dat")
