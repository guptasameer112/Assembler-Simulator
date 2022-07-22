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
        # l = [op_type, ins, registers[reg1], registers[reg2], registers[reg3]]
        l = [op_type, ins, registers[reg3], registers[reg3], registers[reg1]]

    elif op_type == "B":
        reg1 = instruction[5:8]
        imm = instruction[8:]
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
