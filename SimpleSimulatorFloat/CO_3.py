
#loopholes:
    #cant represent numbers less than 1, i.e., where the exponent component is negative 
    #assert is pending for length greater than 8 IEEE notation
    #

def pow(n,x):
    if x>=0:
        if x == 0:
            return 1
        else:
            return n*pow(n,x-1)
    else:
        x = -1*x
        return pow(1/n,x)

def FloatingPoint_to_Decimal(val):
    exp = val[0:3]
    mantisa = val[3:]
    # mantisa = toDecimal(2, mantisa)
    # number = 1 + (10**(-5))*int(mantisa)
    number = "1." + mantisa
    number = toDecimal(2, number)
    exponent = toDecimal(2, str(exp)) - 3
    power = 10**exponent
    number = number*(power)
    number = str(number)
    # num = toDecimal(2, number)
    return number

def Decimal_to_FloatingPoint(number):
    bin_num = str(decimalTo(2, number))
    bin_num = bin_num.split(".")
    exp = len(bin_num[0][1:])
    bin_num[0] = bin_num[0][0] + '.' + bin_num[0][1:]
    bin_num = "".join(bin_num)
    mantisa = bin_num[2:7]
    if len(mantisa)<5:
        mantisa += '0'*(5-len(mantisa))
    exp = decimalTo(2, str(exp + 3))
    if len(exp)<3:
        exp = '0'*(3-len(exp)) + exp
    IEEE_rep = exp + mantisa
    return IEEE_rep

# def binaryToDecimalF(binary):
    # decimal = 0
    # exponent = 0
    # if '.' in binary: 
        # no = (str(binary)).split('.')
        # for i in no[0][::-1]:
            # decimal += int(i) * pow(2, exponent)
            # exponent += 1
        # exponent = -1
        # for i in no[1]:
            # decimal += int(i)* pow(2,exponent)
            # exponent += -1 
        # return decimal
    # else:
        # binary = binary + ".0"
        # return binaryToDecimal(binary)

    
# def decimalToBinaryF(number):
    # if '.' in str(number):
        # number = str(number)
        # num = number.split('.')
        # num = [int(i) for i in num]
        # num[1] = float('0.' + str(num[1])) 
        # binary = ""
        # while (num[0]):
            # binary = str(num[0]%2) + binary
            # num[0] //= 2
        # binary = binary + '.'
        # count = 0
        # while (num[1] and count<10):
            # count +=1
            # num[1] = num[1]*2
            # if num[1]>=1: 
                # binary = binary + '1'
                # num[1] -= 1
            # elif num[1]<1:
                # binary = binary + '0'     
        # if binary[-1] == '.':
            # return binary[:-1]    
        # else:
            # return binary
    # else:
        # number = float(str(number) + ".0")
        # return decimalToBinary(number)

# if __name__ == "__main__":
    # Decimal_to_FloatingPoint(12.5)
    # FloatingPoint_to_Decimal("11001001")

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
