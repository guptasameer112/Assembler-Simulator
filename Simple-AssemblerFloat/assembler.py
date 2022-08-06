import sys

types = {
    "A": ["add", "sub", "mul", "xor", "or", "and", "addf", "subf"],
    "B": ["movi", "rs", "ls", "movf"],
    "C": ["movr", "div", "not", "cmp"],
    "D": ["ld", "st"],
    "E": ["jmp", "jlt", "jgt", "je"],
    "F": ["hlt"]
}

opcodes = {
    "add": "10000",
    "sub": "10001",
    "mul": "10110",
    "xor": "11010",
    "or" : "11011",
    "and": "11100",
    "rs" : "11000",
    "ls" : "11001",
    "div": "10111",
    "not": "11101",
    "cmp": "11110",
    "ld" : "10100",
    "st" : "10101",
    "jmp": "11111",
    "jlt": "01100",
    "jgt": "01101",
    "je" : "01111",
    "hlt": "01010",
    "movi": "10010",
    "movr": "10011",
    "addf": "00000",
    "subf": "00001",
    "movf": "00010",
}

regs = {"R0": "000", "R1": "001", "R2": "010", "R3": "011", "R4": "100", "R5": "101", "R6": "110"}

def throwError(message):
    sys.stdout.write(message + "\n")
    quit()

def getInstructionType(instruction):
    for t in types.keys():
        if instruction in types[t]:
            return t
    throwError("Wrong instruction on line: " + str(lineNumber))

def getOpcode(instruction):
    return opcodes[instruction]

def registerToBinary(register):
    if (register in regs.keys()):
        return regs[register]
    throwError("Wrong register name on line: " + str(lineNumber))

def immToBinary(imm):
    b = ""
    try:
        b = str(format(int(imm),'08b'))
    except:
        throwError("Illegal immediate value on line: " + str(lineNumber))
    if (int(imm) < 0 or int(imm) > 255):
        throwError("Illegal immediate value on line: " + str(lineNumber))
    return b

def writeToStdin(encodedResult):
    sys.stdout.write(encodedResult)
    sys.stdout.write("\n")

def modifyMov(instruction):
    if (instruction[0] == "mov"):
        if (instruction[2][0] == "$"):
            instruction[0] = "movi"
        else:
            instruction[0] = "movr"
    return instruction

def splitWords(instruction):
    instructionList = []
    word = ""
    for c in instruction:
        if (c.isspace()):
            if (len(word)):
                instructionList.append(word)
                word = ""
        else:
            word += c
    instructionList.append(word)

    return instructionList

variables = []
varOpcode = {}
labels = {}
lineNumber = 0


filtered = []
try:
    for line in sys.stdin:
        instruction = line.strip()
        if (instruction == ""):
            continue
        instruction = splitWords(instruction)
        if (instruction[0][-1] == ":"):
            instruction[0] = instruction[0][:-1]
            labels[instruction[0]] = immToBinary(str(lineNumber)) 
            instruction.pop(0)
            lineNumber += 1
            if (len(instruction)):
                instruction = modifyMov(instruction)
            filtered.append(instruction)
            continue

        if (instruction[0] == "var"):
            if (lineNumber):
                throwError("Var declaration between lines: " + str(lineNumber))
            if (len(instruction) != 2):
                throwError("Wrong instruction on line: " + str(lineNumber))
            variables.append(instruction[1])
            continue

        instruction = modifyMov(instruction)
        filtered.append(instruction)
        lineNumber += 1
except EOFError:
    pass

def genVarAddr(lineNumber):
    for var in variables:
        varOpcode[var] = immToBinary(lineNumber)
        lineNumber += 1

def verifyHlt():
    for line in filtered[:-1]:
        if line[0] == "hlt":
            throwError("hlt in between lines")
    if (filtered[-1][0] != "hlt"):
        throwError("Missing hlt instruction")


genVarAddr(lineNumber)
verifyHlt()

def Decimal_to_FloatingPoint(number):
    bin_num = str(decimalTo(2, number))
    bin_num = bin_num.split(".")
    exp = len(bin_num[0][1:])
    bin_num[0] = bin_num[0][0] + '.' + bin_num[0][1:]
    bin_num = "".join(bin_num)
    mantisa = bin_num[2:7]
    if len(mantisa)<5:
        mantisa += '0'*(5-len(mantisa))
    exp = decimalTo(2, str(exp))
    if len(exp)<3:
        exp = '0'*(3-len(exp)) + exp
    IEEE_rep = exp + mantisa
    IEEE_rep = 8*"0" + IEEE_rep
    return IEEE_rep

def decimalTo(base, n):
    n = n.split(".")
    integerPart = int(n[0])
    result = ""
    while (integerPart):
        rem = integerPart % base
        if (rem > 9):
            rem = chr(rem + 55)
        result = str(rem) + result
        integerPart //= base
    if (len(n) > 1):
        result += "."
        if (int(n[0]) == 0):
            result = "0."
        fracPart = "0." + n[1]
        steps = 0
        while (float(fracPart) > 0):
            if (steps > 10):
                break
            rem = float(fracPart) * base
            lst = str(rem).split(".")
            d = lst[0]
            if (int(d) > 9):
                d = chr(int(d) + 55)
            fracPart = "0." + lst[1]
            result += d
            steps += 1
    return result 
# end decimalTo

def toDecimal(base, n):
    code = {"0": "0", "1": "1", "2": "2", "3": "3", "4": "4", "5": "5", "6": "6", "7": "7", "8": "8", "9": "9", "A": "10", "B": "11", "C": "12", "D": "13", "E": "14", "F": "15", "G": "16", "H": "17", "I": "18", "J": "19", "K": "20", "L": "21", "M": "22", "N": "23", "O": "24", "P": "25", "Q": "26", "R": "27", "S": "28", "T": "29", "U": "30", "V": "31", "W": "32", "X": "33", "Y": "34", "Z": "35"}
    n = n.split(".")
    power = 0
    result = 0
    for x in n[0][::-1]:
        x = code[x]
        result += int(x)*(base**power)
        power += 1

    if (len(n) > 1):
        power = -1
        for x in n[1]:
            x = code[x]
            result += int(x)*(base**power)
            power -= 1
    return result
# end toDecimal

lineNumber = 0
binaryFile = []
for line in filtered:
    insType = getInstructionType(line[0])
    opcode = getOpcode(line[0])
    encodedResult = ""
    if (insType == "A"):
        if (len(line) != 4):
            throwError("Wrong instruction on line: " + str(lineNumber))
        r1 = registerToBinary(line[1])
        r2 = registerToBinary(line[2])
        r3 = registerToBinary(line[3])
        encodedResult = opcode + "00" + r1 + r2 + r3
    elif (insType == "B"):
        if (len(line) != 3):
            throwError("Wrong instruction on line: " + str(lineNumber))
        r1 = registerToBinary(line[1])
        if (opcode == "00010"):
            imm = Decimal_to_FloatingPoint(line[2][1:])[8:]
        else:
            imm = immToBinary(line[2][1:])
        encodedResult = opcode + r1 + imm
    elif (insType == "C"):
        if (len(line) != 3):
            throwError("Wrong instruction on line: " + str(lineNumber))
        r1 = ""
        if (line[1] == "FLAGS"):
            r1 = "111"
        else:
            r1 = registerToBinary(line[1])
        r2 = registerToBinary(line[2])
        encodedResult = opcode + "00000" + r1 + r2
    elif (insType == "D"):
        if (len(line) != 3):
            throwError("Wrong instruction on line: " + str(lineNumber))
        r1 = registerToBinary(line[1])
        try:
            mem = varOpcode[line[2]]
        except:
            throwError("Undefined variable used on line: " + str(lineNumber))
        encodedResult = opcode + r1 + mem
    elif (insType == "E"):
        if (len(line) != 2):
            throwError("Wrong instruction on line: " + str(lineNumber))
        try:
            mem = labels[line[1]]
        except:
            throwError("Undefined label used on line: " + str(lineNumber))
        encodedResult = opcode + "000" + mem
    elif (insType == "F"):
        if (len(line) != 1):
            throwError("Wrong instruction on line: " + str(lineNumber))
        encodedResult = opcode + "00000000000"
    lineNumber += 1

    binaryFile.append(encodedResult)


for line in binaryFile:
    writeToStdin(line)

