from SimpleSimulator.SimpleSimulator import read_register, write_register


def decimalToBinary(number):
    binary = ""
    while (number):
        binary = str(number % 2) + binary
        number /= 2

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

    if (ra + rb >= pow(2, 16)):
        pass
    else:
        s = ra + rb
        binary_sum = decimalToBinary(s)
        write_register(rc, binary_sum)

def subtract(ra, rb, rc):
    ra = read_register(ra)
    rb = read_register(rb)

    ra = binaryToDecimal(ra)
    rb = binaryToDecimal(rb)

    if (ra - rb < 0):
        pass
    else:
        d = ra - rb
        binary_diff = decimalToBinary(d)
        write_register(rc, binary_diff)

def multiply(ra, rb, rc):
    ra = read_register(ra)
    rb = read_register(rb)

    ra = binaryToDecimal(ra)
    rb = binaryToDecimal(rb)

    if (ra * rb >= pow(2, 16)):
        pass
    else:
        m = ra * rb
        binary_mul = decimalToBinary(m)
        write_register(rc, binary_mul)

def divide(ra, rb):
    ra = read_register(ra)
    rb = read_register(rb)

    ra = binaryToDecimal(ra)
    rb = binaryToDecimal(rb)

    quotient = ra // rb
    remainder = ra % rb

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
    ra = read_register(ra)
    ra = binaryToDecimal(ra)

    result = ~ra
    result = decimalToBinary(result)
    write_register(rb, result)

def compare(ra, rb):
    ra = read_register(ra)
    rb = read_register(rb)

    ra = binaryToDecimal(ra)
    rb = binaryToDecimal(rb)

    if (ra < rb):
        pass
    elif (ra == rb):
        pass
    else:
        pass
