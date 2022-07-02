import sys

types = {
    "A": ["add", "sub", "mul", "xor", "or", "and"],
    "B": ["movi", "rs", "ls"],
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
