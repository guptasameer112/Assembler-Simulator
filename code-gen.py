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
