import sys
# weewooweewoo

# Memory (global list): 256 lines long list
# Init memory: initialise memory with instructions
# Fetch: fetches instruction from memory
# Decoder: parses the instruction to return type, name and operands
# Executioner: takes in the type and operands to execute the instruction. Call ALU, ld, st, branch etc
# Program Counter (global)
# Register file (binary dictionary): reads or writes to the registers
# Arithmetic Logic Unit (ALU)

memory = []
registers = {}

def FloatingPoint_to_Decimal(val):
    exp = val[0:3]
    mantisa = val[3:]
    number = "1" + mantisa
    exponent = toDecimal(2, str(exp))
    if (exponent < 0):
        number = "0." + (abs(exponent) - 1)*"0" + number
    elif (exponent > 0):
        number = number[:(abs(exponent) + 1)] + "." + number[(abs(exponent) + 1):]
    else:
        number = number[0] + "." + number[1:]
    number = toDecimal(2, number)
    number = str(number)
    return number

def Decimal_to_FloatingPoint(number):
    bin_num = str(decimalTo(2, number))
    bin_num = bin_num.split(".")
    exp = 0
    exp = len(bin_num[0][1:])
    bin_num[0] = bin_num[0][0] + "." + bin_num[0][1:]
    bin_num = "".join(bin_num)
    mantisa = bin_num[2:7]
    if len(mantisa)<5:
        mantisa += "0"*(5-len(mantisa))
    exp = decimalTo(2, str(exp))
    if len(exp)<3:
        exp = "0"*(3-len(exp)) + exp
    IEEE_rep = exp + mantisa
    IEEE_rep = 8*"0" + IEEE_rep
    return IEEE_rep

def decimalTo(base, n):
    n = str(n).split(".")
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
def decoder(instruction):
    registers = {
        "000": "R0",
        "001": "R1",
        "010": "R2",
        "011": "R3",
        "100": "R4",
        "101": "R5",
        "110": "R6",
        "111": "FLAGS",
    }
    opcodes = {
        "10000": ["add" , "A"],
        "10001": ["sub", "A"],
        "10110": ["mul", "A"],
        "11010": ["xor", "A"],
        "11011": ["or", "A"],
        "11100": ["and", "A"],
        "11000": ["rs", "B"],
        "11001": ["ls", "B"],
        "10111": ["div", "C"],
        "11101": ["not", "C"],
        "11110": ["cmp", "C"],
        "10100": ["ld", "D"],
        "10101": ["st", "D"],
        "11111": ["jmp", "E"],
        "01100": ["jlt", "E"],
        "01101": ["jgt", "E"],
        "01111": ["je", "E"],
        "01010": ["hlt", "F"],
        "10010": ["movi", "B"],
        "10011": ["movr", "C"],
        "00000": ["addf", "A"],
        "00001": ["subf", "A"],
        "00010": ["movf", "B"],
    }

    opcode = instruction[0:5]
    op_type = opcodes[opcode][1]
    ins = opcodes[opcode][0]
    l = []
    if op_type == "A":
        unused = instruction[5:7]
        reg1 = instruction[7:10]
        reg2 = instruction[10:13]
        reg3 = instruction[13:]
        l = [op_type, ins, registers[reg1], registers[reg2], registers[reg3]]

    elif op_type == "B":
        reg1 = instruction[5:8]
        imm = instruction[8:]
        if (ins == "movf"):
            imm = FloatingPoint_to_Decimal(imm)
        else:
            imm = binaryToDecimal(imm)
        l = [op_type, ins, registers[reg1], imm]
    
    elif op_type == "C":
        unused = instruction[5:10]
        reg1 = instruction[10:13]
        reg2 = instruction[13:]
        l = [op_type, ins, registers[reg1], registers[reg2]]

    elif op_type == "D":
        reg1 = instruction[5:8]
        mem_addr = instruction[8:]
        mem_addr = binaryToDecimal(mem_addr)
        l = [op_type, ins, registers[reg1], mem_addr]

    elif op_type == "E":
        unused = instruction[5:8]
        mem_addr = instruction[8:]
        mem_addr = binaryToDecimal(mem_addr)
        l = [op_type, ins, mem_addr]
    
    elif op_type == "F":
        l = [op_type, ins]

    return l

def decimalToBinary(number):
    binary = ""
    number = int(number)
    while (number):
        binary = str(number % 2) + binary
        number //= 2

    binary = ((16 - len(binary)) * "0") + binary
    return binary

def binaryToDecimal(binary):
    decimal = 0
    exponent = 0
    for i in binary[::-1]:
        decimal += int(i) * pow(2, exponent)
        exponent += 1
    return decimal

def add(ra, rb, rc):
    ra = read_register(ra)
    rb = read_register(rb)

    ra = binaryToDecimal(ra)
    rb = binaryToDecimal(rb)

    reset_flags()
    if (ra + rb >= pow(2, 16)):
        write_register(rc, decimalToBinary((ra + rb) % pow(2, 16)))
        flags = read_register("FLAGS")
        flags = list(flags)
        flags[12] = "1"
        flags = "".join(flags)
        write_register("FLAGS", flags)
    else:
        s = ra + rb
        binary_sum = decimalToBinary(s)
        write_register(rc, binary_sum)
        reset_flags()

def addf(ra, rb, rc):
    ra = read_register(ra)
    rb = read_register(rb)

    ra = float(FloatingPoint_to_Decimal(ra[8:]))
    rb = float(FloatingPoint_to_Decimal(rb[8:]))

    reset_flags()
    if (ra + rb >= pow(2, 16)):
        write_register(rc, 8*"0" + 8*"1")
        flags = read_register("FLAGS")
        flags = list(flags)
        flags[12] = "1"
        flags = "".join(flags)
        write_register("FLAGS", flags)
    else:
        s = ra + rb
        binary_sum = Decimal_to_FloatingPoint(s)
        write_register(rc, binary_sum)
        reset_flags()
 
def subtract(ra, rb, rc):
    ra = read_register(ra)
    rb = read_register(rb)

    ra = binaryToDecimal(ra)
    rb = binaryToDecimal(rb)

    reset_flags()
    if (ra - rb < 0):
        write_register(rc, decimalToBinary(0))
        flags = read_register("FLAGS")
        flags = list(flags) 
        flags[12] = "1"
        flags = "".join(flags)
        write_register("FLAGS", flags)
    else:
        d = ra - rb
        binary_diff = decimalToBinary(d)
        write_register(rc, binary_diff)
        reset_flags()

def subtractf(ra, rb, rc):
    ra = read_register(ra)
    rb = read_register(rb)

    ra = float(FloatingPoint_to_Decimal(ra[8:]))
    rb = float(FloatingPoint_to_Decimal(rb[8:]))

    reset_flags()
    if (ra - rb < 0):
        write_register(rc, decimalToBinary(0))
        flags = read_register("FLAGS")
        flags = list(flags) 
        flags[12] = "1"
        flags = "".join(flags)
        write_register("FLAGS", flags)
    else:
        d = ra - rb
        binary_diff = Decimal_to_FloatingPoint(d)
        write_register(rc, binary_diff)
        reset_flags()


def multiply(ra, rb, rc):
    ra = read_register(ra)
    rb = read_register(rb)

    ra = binaryToDecimal(ra)
    rb = binaryToDecimal(rb)

    reset_flags()
    if (ra * rb >= pow(2, 16)):
        write_register(rc, decimalToBinary((ra * rb) % pow(2, 16)))
        flags = read_register("FLAGS")
        flags = list(flags) 
        flags[12] = "1"
        flags = "".join(flags)
        write_register("FLAGS", flags)
    else:
        m = ra * rb
        binary_mul = decimalToBinary(m)
        write_register(rc, binary_mul)
        reset_flags()

def divide(ra, rb):
    ra = read_register(ra)
    rb = read_register(rb)

    ra = binaryToDecimal(ra)
    rb = binaryToDecimal(rb)

    quotient = ra // rb
    remainder = ra % rb

    quotient = decimalToBinary(quotient)
    remainder = decimalToBinary(remainder)

    write_register("R0", quotient)
    write_register("R1", remainder)

def right_shift(reg, imm):
    r = read_register(reg)
    r = binaryToDecimal(r)

    r = r >> imm # right shift

    r = decimalToBinary(r)
    write_register(reg, r)

def left_shift(reg, imm):
    r = read_register(reg)
    r = binaryToDecimal(r)

    r = r << imm # right shift

    r = decimalToBinary(r)
    write_register(reg, r)

def bitwise_xor(ra, rb, rc):
    ra = read_register(ra)
    rb = read_register(rb)

    ra = binaryToDecimal(ra)
    rb = binaryToDecimal(rb)

    result = ra ^ rb

    result = decimalToBinary(result)
    write_register(rc, result)

def bitwise_or(ra, rb, rc):
    ra = read_register(ra)
    rb = read_register(rb)

    ra = binaryToDecimal(ra)
    rb = binaryToDecimal(rb)

    result = ra | rb

    result = decimalToBinary(result)
    write_register(rc, result)

def bitwise_and(ra, rb, rc):
    ra = read_register(ra)
    rb = read_register(rb)

    ra = binaryToDecimal(ra)
    rb = binaryToDecimal(rb)

    result = ra & rb

    result = decimalToBinary(result)
    write_register(rc, result)

def bitwise_not(ra, rb):
    # ra = read_register(ra)
    rb = read_register(rb)
    # ra = binaryToDecimal(ra)

    result = ""
    for i in rb:
        if (i == "1"):
            result += "0"
        else:
            result += "1"
    write_register(ra, result)

def compare(ra, rb):
    ra = read_register(ra)
    rb = read_register(rb)

    ra = binaryToDecimal(ra)
    rb = binaryToDecimal(rb)

    reset_flags()
    if (ra < rb):
        flags = read_register("FLAGS")
        flags = list(flags)
        flags[13] = "1"
        flags = "".join(flags)
        write_register("FLAGS", flags)
    elif (ra == rb):
        flags = read_register("FLAGS")
        flags = list(flags)
        flags[15] = "1"
        flags = "".join(flags)
        write_register("FLAGS", flags)
    else:
        flags = read_register("FLAGS")
        flags = list(flags)
        flags[14] = "1"
        flags = "".join(flags)
        write_register("FLAGS", flags)

def init_memory():
    # take input from stdin
    try:
        for line in sys.stdin:
            line = line.strip()
            memory.append(line)
    except EOFError:
        pass

    # initialise remaining indices with "0"
    while (len(memory) < 256):
        memory.append(16 * "0")

def reset_flags():
    registers["FLAGS"] = 16 * "0"

def init_registers():
    for i in range(7):
        registers["R" + str(i)] = 16 * "0"
    reset_flags()

def read_register(reg):
    return registers[reg]

def write_register(reg, value):
    registers[reg] = value

def fetch_instruction(program_counter):
    return memory[program_counter]

def ld(reg, mem_addr):
    data = memory[mem_addr]
    write_register(reg, data)

def st(reg, mem_addr):
    data = read_register(reg)
    memory[mem_addr] = data

def jlt(mem_addr, program_counter):
    flags = read_register("FLAGS") 
    if (flags[13] == "1"):
        reset_flags()
        return mem_addr
    reset_flags()

    return 1 + program_counter

def jgt(mem_addr, program_counter):
    flags = read_register("FLAGS") 
    if (flags[14] == "1"):
        reset_flags()
        return mem_addr
    reset_flags()

    return 1 + program_counter

def je(mem_addr, program_counter):
    flags = read_register("FLAGS") 
    if (flags[15] == "1"):
        reset_flags()
        return mem_addr
    reset_flags()

    return 1 + program_counter

def executioner(instruction, instruction_type, arguments, program_counter):
    if (instruction_type == "A"):
        if (instruction == "add"):
            add(arguments[0], arguments[1], arguments[2])
        elif (instruction == "sub"):
            subtract(arguments[0], arguments[1], arguments[2])
        elif (instruction == "mul"):
            multiply(arguments[0], arguments[1], arguments[2])
        elif (instruction == "xor"):
            bitwise_xor(arguments[0], arguments[1], arguments[2])
        elif (instruction == "or"):
            bitwise_or(arguments[0], arguments[1], arguments[2])
        elif (instruction == "and"):
            bitwise_and(arguments[0], arguments[1], arguments[2])
        elif (instruction == "addf"):
            addf(arguments[0], arguments[1], arguments[2])
        elif (instruction == "subf"):
            subtractf(arguments[0], arguments[1], arguments[2])
    elif (instruction_type == "B"):
        if (instruction == "rs"):
            right_shift(arguments[0], arguments[1])
        elif (instruction == "ls"):
            left_shift(arguments[0], arguments[1])
        elif (instruction == "movi"):
            imm = decimalToBinary(arguments[1])
            write_register(arguments[0], imm)
        elif (instruction == "movf"):
            imm = Decimal_to_FloatingPoint(arguments[1])
            write_register(arguments[0], imm)
    elif (instruction_type == "C"):
        if (instruction == "div"):
            divide(arguments[0], arguments[1])
        elif (instruction == "not"):
            bitwise_not(arguments[0], arguments[1])
        elif (instruction == "cmp"):
            compare(arguments[0], arguments[1])
        elif (instruction == "movr"):
            r2 = read_register(arguments[1])
            write_register(arguments[0], r2)
    elif (instruction_type == "D"):
        if (instruction == "ld"):
            ld(arguments[0], arguments[1])
        elif (instruction == "st"):
            st(arguments[0], arguments[1])
    elif (instruction_type == "E"):
        if (instruction == "jmp"):
            return arguments[0]
        elif (instruction == "jlt"):
            return jlt(arguments[0], program_counter)
        elif (instruction == "jgt"):
            return jgt(arguments[0], program_counter)
        elif (instruction == "je"):
            return je(arguments[0], program_counter)
    elif (instruction_type == "F"):
        return -1

    return program_counter + 1

def memory_dump():
    for line in memory:
        print(line)

def data_dump(program_counter):
    program_counter = decimalToBinary(program_counter)[8:]
    line = program_counter + " "
    for reg in ["R0", "R1", "R2", "R3", "R4", "R5", "R6", "FLAGS"]:
        line += registers[reg] + " "
    print(line[:-1])

def loop():
    program_counter = 0
    init_memory()
    init_registers()
    while True:
        instruction = fetch_instruction(program_counter)
        decoded_ins = decoder(instruction)
        new_program_counter = executioner(decoded_ins[1], decoded_ins[0], decoded_ins[2:], program_counter)
        if (decoded_ins[1] != "add" and decoded_ins[1] != "sub" and decoded_ins[1] != "mul" and decoded_ins[1] != "cmp"):
            reset_flags()
        data_dump(program_counter)
        if (new_program_counter == -1): 
                break
        program_counter = new_program_counter
    #end while

    memory_dump()

loop()


