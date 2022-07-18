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

program_counter = 0
memory = []
registers = {}

def init_memory():
    # take input from stdin
    try:
        for line in sys.stdin:
            memory.append(line)
    except EOFError:
        pass

    # initialise remaining indices with "0"
    while (len(memory) < 256):
        memory.append(16 * "0")


def init_registers():
    for i in range(7):
        registers["R" + str(i)] = 16 * "0"

    registers["FLAGS"] = 16 * "0"

def read_register(reg):
    return registers[reg]

def write_register(reg, value):
    registers[reg] = value

def fetch_instruction():
    return memory[program_counter]

def executioner(instruction, instruction_type, arguments):
    if (instruction_type == "A"):
        pass
    elif (instruction_type == "B"):
        pass
    elif (instruction_type == "C"):
        pass
    elif (instruction_type == "D"):
        pass
    elif (instruction_type == "E"):
        pass
    elif (instruction_type == "F"):
        return -1
