def pow(n,x):
    if x>=0:
        if x == 0:
            return 1
        else:
            return n*pow(n,x-1)
    else:
        x = -1*x
        return pow(1/n,x)

def floating_point(instruction):
    val = instruction[-8:]
    exp = val[0:3]
    mantisa = val[3:]
    number = 1 + (10**(-5))*int(mantisa)
    exponent = binaryToDecimal(exp)-3
    power = 10**exponent
    number = number*(power)
    number = str(number)
    num = binaryToDecimal(number)
    return num

def binaryToDecimal(binary):
    decimal = 0
    exponent = 0
    if '.' in binary: 
        no = (str(binary)).split('.')
        for i in no[0][::-1]:
            decimal += int(i) * pow(2, exponent)
            exponent += 1
        exponent = -1
        for i in no[1]:
            decimal += int(i)* pow(2,exponent)
            exponent += -1 
        return decimal
    else:
        binary = binary + ".0"
        return binaryToDecimal(binary)

if __name__ == "__main__":
    print(floating_point("11111110"))
