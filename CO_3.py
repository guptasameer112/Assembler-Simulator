
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

def FloatingPoint_to_Decimal(instruction):
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

def Decimal_to_FloatingPoint(number):
    bin_num = str(decimalToBinary(number))
    bin_num = bin_num.split(".")
    exp = len(bin_num[0][1:])
    bin_num[0] = bin_num[0][0] + '.' + bin_num[0][1:]
    bin_num = "".join(bin_num)
    mantisa = bin_num[2:7]
    if len(mantisa)<5:
        mantisa = '0'*(5-len(mantisa)) + mantisa
    exp = decimalToBinary(exp + 3)
    if len(exp)<3:
        exp = '0'*(3-len(exp)) + exp
    IEEE_rep = exp + mantisa
    return IEEE_rep

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

    
def decimalToBinary(number):
    if '.' in str(number):
        number = str(number)
        num = number.split('.')
        num = [int(i) for i in num]
        num[1] = float('0.' + str(num[1])) 
        binary = ""
        while (num[0]):
            binary = str(num[0]%2) + binary
            num[0] //= 2
        binary = binary + '.'
        count = 0
        while (num[1] and count<10):
            count +=1
            num[1] = num[1]*2
            if num[1]>=1: 
                binary = binary + '1'
                num[1] -= 1
            elif num[1]<1:
                binary = binary + '0'     
        if binary[-1] == '.':
            return binary[:-1]    
        else:
            return binary
    else:
        number = float(str(number) + ".0")
        return decimalToBinary(number)

if __name__ == "__main__":
    Decimal_to_FloatingPoint(12.5)
    FloatingPoint_to_Decimal("11001001")
