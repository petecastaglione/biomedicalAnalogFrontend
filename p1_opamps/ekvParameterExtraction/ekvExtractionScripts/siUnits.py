import math

#TODO make SI class

siPrefixes = {'y': 1e-24,  # yocto
              'z': 1e-21,  # zepto
              'a': 1e-18,  # atto
              'f': 1e-15,  # femto
              'p': 1e-12,  # pico
              'n': 1e-9,   # nano
              'u': 1e-6,   # micro
              'm': 1e-3,   # mili
            #   'c': 1e-2,   # centi
            #   'd': 1e-1,   # deci
              'k': 1e3,    # kilo
              'M': 1e6,    # mega
              'G': 1e9,    # giga
              'T': 1e12,   # tera
              'P': 1e15,   # peta
              'E': 1e18,   # exa
              'Z': 1e21,   # zetta
              }

def inputSiUnits(message):
    inputString = input(message)
    res = inputString
    for key in siPrefixes:
        if key in inputString:
            inputString = inputString.split(key)            
            res = float(inputString[0]) * siPrefixes[key]       # or *siPrefixes[inputString[1]]
    return res

def siString2Num(str):
    res = str
    for key in siPrefixes:
        if key in str:
            str = str.split(key)            
            res = float(str[0]) * siPrefixes[key]       # or *siPrefixes[inputString[1]]
    try:
        if res == str:
            print('No SI Unit Prefix found in inputString ')
            raise KeyError('Invalid input String')
    except KeyError:        
        print("inputString=" + str)
        raise
    finally:
        pass
    
    return res



# getting dict key from value with filter function & lambda is slower?
#ex:
# my_dict = {"Java": 100, "Python": 112, "C": 11}
 
# # Get the key corresponding to value 100
# key = list(filter(lambda x: my_dict[x] == 100, my_dict))[0]
def num2SiString(outputNumber):        
    outputNumber = float(outputNumber)
    for value in siPrefixes.values():        
        if outputNumber < value:     
            # if outputNumber < siPrefixes['p'] and outputNumber > siPrefixes['p']/100:         #if i want it to still show value in pico if the value is between 0.01p and 1p
            #     outputNumber = outputNumber/siPrefixes['p']
            #     siPrefix = 'p'
            if outputNumber < siPrefixes['k'] and outputNumber > 1:
                siPrefix = ''
            else:
                key = list(siPrefixes.keys())[list(siPrefixes.values()).index(previousValue)]      #finds the corresponging key(si prefix) given the dictionary value(power of 10)
                # make a list out of all SI prefixes
                # use the last SI prefix (that is smaller than the current number) to find the index of said SI prefix in the dictionary
                # use the resulting index to append the corresponding SI prefix to the number, divided by the found SI prefix/value
                
                outputNumber = outputNumber/previousValue
                siPrefix = key
            break
        else:
            previousValue = value

    # if outputNumber >= siPrefixes['k']:        
    #     outputNumber = outputNumber/siPrefixes['k']
    #     siPrefix = 'k'
    
    outputString = str(outputNumber) + siPrefix
    return outputString


def num2SiStringRounded(outputNumber):        
    outputNumber = float(outputNumber)
    firstIteration = True
    for value in siPrefixes.values():      
        if firstIteration:
            previousValue = value
            firstIteration = False  
        if outputNumber < value:                 
            # if outputNumber < siPrefixes['p'] and outputNumber > siPrefixes['p']/100:         #if i want it to still show value in pico if the value is between 0.01p and 1p
            #     outputNumber = outputNumber/siPrefixes['p']
            #     siPrefix = 'p'
            if outputNumber < siPrefixes['k'] and outputNumber > 1:
                siPrefix = ''
            else:
                key = list(siPrefixes.keys())[list(siPrefixes.values()).index(previousValue)]      #finds the corresponging key(si prefix) given the dictionary value(power of 10)
                # make a list out of all SI prefixes
                # use the last SI prefix (that is smaller than the current number) to find the index of said SI prefix in the dictionary
                # use the resulting index to append the corresponding SI prefix to the number, divided by the found SI prefix/value
                
                outputNumber = outputNumber/previousValue
                siPrefix = key
            break
        else:
            previousValue = value

    # if outputNumber >= siPrefixes['k']:        
    #     outputNumber = outputNumber/siPrefixes['k']
    #     siPrefix = 'k'
    
    outputString = str(round(outputNumber, 3)) + siPrefix
    return outputString

#define si function that can receive either an SI string to convert to a number or a float number to convert to SI string
def si(input):
    if isinstance(input, str):
        return siString2Num(input)
    elif isinstance(input, (int, float)):
        print("isfloat")
        return num2SiStringRounded(input)
    else:
        return "Unsupported input type. Please provide a string or a number."