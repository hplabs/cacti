import pandas as pd
import os


def clean(string):
    tmp = string.replace(" ", "")
    tmp = tmp.replace(";", "")
    tmp = tmp.replace("\n", "")
    return tmp

def removeTab(string):
    return string.replace("\t", "")

def removeDecimal(string):
    return string.replace(".", "")

def check(line):
    if "LPDDR2" in line:
        return "LPDDR2"
    if "WideIO" in line:
        return "WideIO"
    if "DDR3" in line:
        return "DDR3"
    if "Serial" in line:
        return "Serial"
    else:
        return None


file = open("extio_technology.cc")
lines = file.readlines()

varList = []
outputs = ["IO Area", "IO Dynamic Power", "IO Termination and Bias Power"]

if not os.path.isdir("iocc_results"):
    os.mkdir("iocc_results")

function = '1'
functionType = "LPDDR2"
for x in range(len(lines)):
    var = None
    val = None

    if check(lines[x]) != None:
        functionType = check(lines[x])

    if "  frequency = freq;" in lines[x]:
        function = '2'

    if "=" in lines[x]:
        text = lines[x].split(" = ")
        if len(text) > 1:
            var = clean(text[0])
            val = clean(text[1])
            # print (removeDecimal(val).isnumeric())
            if removeDecimal(val).isnumeric():
                # print(val)
                controlLine = var + " = " + str(val) + ";" + "\n"
                varSpec = var + "_" + function + "_" + functionType
                varList.append(removeTab(varSpec))
                if val == "0":
                    val = 1
                elif "." in val:
                    val = float(val)*1000
                else:
                    val = int(val)*1000

                # print (val)
                print (var + " = " + str(val))
                lines[x] = var + " = " + str(val) + ";" +"\n"
                
                with open("extio_technology.cc", 'w') as file:
                    file.writelines(lines) 

                os.system("make")
                os.system("./cacti -infile cache.cfg > output.txt")
                os.system("diff control.txt output.txt > " + "iocc_results/" + varSpec + ".txt")

                lines[x] = controlLine

                with open("extio_technology.cc", 'w') as file:
                    file.writelines(lines) 
result = pd.DataFrame(index=varList, columns= outputs)
print (result)

                
