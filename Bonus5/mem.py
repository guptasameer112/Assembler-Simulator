import math

def getSpaceBits(space):
    units = {"K": 1000, "Ki": 1024, "M": 1000000, "Mi": 1048576, "G": 1000000000, "Gi": 1073741824}
    space = space.split(" ")
    bits = int(space[0])
    if (len(space[1]) > 1):
        bits *= units[space[1][:-1]]
    if (space[-1] == "B"):
        bits *= 8
    return bits

def calAddrBits(space, n):
    numAddr = math.ceil(math.log2(space / n))
    return numAddr

space = input("Enter memory space: ")
space = getSpaceBits(space)
memTypeArray = [1, 4, 8, 16]
print("Enter type of memory based on the following menu:\n1. Bit\n2. Nibble\n3. Byte\n4. Word\n")
memType = int(input()) - 1
while True:
    question = int(input("Enter the question type, 1 or 2 (0 for exit): "))
    if (question == 0):
        break
    if (question == 1):
        instructionLen = int(input("Enter the length of one instruction (in bits): "))
        registerLen = int(input("Enter the length register (in bits): "))
        addrBits = calAddrBits(space, memTypeArray[memType])
        opcodeBits = instructionLen - registerLen - addrBits
        fillerBits = instructionLen - opcodeBits - 2*registerLen
        maxInstructions = 2**opcodeBits
        maxRegisters = 2**registerLen

        print("Minimum bits needed to represent an address in this architecture: " + str(addrBits))
        print("Number of bits needed by opcode: " + str(opcodeBits))
        print("Number of filler bits in Instruction type 2: " + str(fillerBits))
        print("Maximum numbers of instructions this ISA can support: " + str(maxInstructions))
        print("Maximum number of registers this ISA can support: " + str(maxRegisters))

    else:
        question2Type = int(input("Enter type of query, 1 or 2: "))
        if (question2Type == 1):
            cpuBits = int(input("Enter how many bits the CPU is: "))
            memTypeArray[3] = cpuBits
            print("Enter type of memory based on the following menu:\n1. Bit\n2. Nibble\n3. Byte\n4. Word\n")
            desiredMemType = int(input()) - 1
            addrBits = calAddrBits(space, memTypeArray[memType])
            newAddrBits = calAddrBits(space, memTypeArray[desiredMemType])
            print("Pins: " + str(newAddrBits - addrBits))
        else:
            cpuBits = int(input("Enter how many bits the CPU is: "))
            addrPins = int(input("Enter number of address pins: "))
            print("Enter type of memory based on the following menu:\n1. Bit\n2. Nibble\n3. Byte\n4. Word\n")
            memTypeArray[3] = cpuBits
            memType = int(input()) - 1
            maxMemory = memTypeArray[memType] * (2**(addrPins - 3))
            print(str(maxMemory) + " Bytes")
