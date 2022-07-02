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
