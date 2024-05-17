
import pandas as pd
import os
import subprocess


tech_result = None
def float_to_exponential(num):
    return format(num, "e")

# read the unit header but don't add the column label to it 
def parse(file, first, last):
    chunk = file.iloc[first:last]
    chunk= chunk['parameters'].str.split(expand = True)
    chunk = chunk.reset_index(drop=True)
    chunk.loc[len(chunk)] = None
    return chunk

def partition(tech_param, tech_result):
    tech_param = pd.read_csv(tech_param, names = ['parameters'])
    tech_result = None
    part = None

    for x in range(11):
        if x==1:
            part = parse(tech_param, 0, 13)
            tech_result = part
            # print(tech_part)
        elif x==2:
            part = parse(tech_param, 13, 36)
            # tech_part.columns =['parameters', '(unit)', 'temp', 'hp','lstp','lop','lp-dram ','comm-dram']
            # print(part)
        elif x==3:
            part = parse(tech_param, 36, 44)
            # tech_part.columns =['parameters', '(unit)', 'hp', 'lstp', 'lop', 'lp-dram', 'comm-dram']
            # print(tech_part)
        elif x==4:
            part = parse(tech_param, 44, 51)
            # tech_part.columns =['parameters', '(unit)', 'cell_type', 'hp', 'lstp', 'lop','lp-dram','comm-dram']
            # print(tech_part)
        elif x==5:
            part = parse(tech_param, 51, 58)
            # tech_part.columns =['parameters', '(unit)', 'cell_type', 'hp', 'lstp', 'lop','lp-dram','comm-dram']
            # print(tech_part)
        elif x==6:
            part = parse(tech_param, 58, 66)
            # tech_part.columns =['parameters', '(unit)','cell_type', 'hp', 'lstp', 'lop','lp-dram','comm-dram']
            # print(tech_part)
        elif x==7:
            part = parse(tech_param, 66, 71)
            # tech_part.columns =['parameters', '(unit)', 'hp',  'lstp',   'lop',  'lp-dram',   'comm-dram' ]
            # print(tech_part)
        elif x==8:
            part = parse(tech_param, 71, 78)
            # print(tech_part)
        elif x==9:
            part = parse(tech_param, 78, 90)
            # tech_part.columns =['parameters','(units)', '0/0', '0/1', '0/2', '0/3', '1/0', '1/1', '1/2', '1/3' ]
            # print(tech_part)
        elif x==10:
            part = parse(tech_param, 90, None)
            # tech_part.columns =['parameters','(units)', '0/0', '0/1', '0/2', '1/0', '1/1', '1/2' ]
            # print(tech_part)

        # print(tech_part)
        if x>1:
            tech_result=pd.concat([tech_result, part], ignore_index=True)
    return tech_result




data = partition("real/90nm.dat", tech_result)
control = partition("real/90nm.dat", tech_result)


data.to_csv('tech_params/90nm.dat', index=False, header=False, sep=' ')

# make sure to allow targeting for each cell by header
for y in range (len(data)):
    for x in range (len(data.columns)):
        cell = data.iloc[y,x]
        if cell == "parameters":
            break
        if not(pd.isnull(cell)) and cell[0].isdigit():
            data.iloc[y,x] = float_to_exponential(float(data.iloc[y,x])*1000)
            # data.to_csv('tech_params/90nm.dat', index=False, header=True, sep=' ')

            # print (data)
            data = partition("real/90nm.dat", tech_result)
            # os.system("./cacti -infile cache.cfg > output.txt")
            # os.system("diff control.txt output.txt >> cool/" + control.iloc[y+1,0] + ".txt")
            # file = open(control.iloc[y+1,0]+".txt")
            # lines = fp.readlines()
            # for line in lines:
            #     # check if string present on a current line
            #     if line.find(word) != -1:
            #         print(word, 'string exists in file')
            #         print('Line Number:', lines.index(line))
            # #         print('Line:', line)
            # data = partition("real/90nm.dat", tech_result)
        
'''
readL: outputs dataframesss

process: change the values, write to data, call cacti
output to a different file and process that one instead 

write: input dataframes
'''


# process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# output, error = process.communicate()

# # Decode output and error from bytes to string
# output_str = output.decode('utf-8')
# error_str = error.decode('utf-8')

# # Print output and error
# print("Output:", output_str)


# for y in range (5):
#     for x in range (7):
#         if not(pd.isnull(data.iloc[y+1,x+2])) :
#             data = partition("idk/cacti/tech_params/90nm.dat", tech_result)
#             data.iloc[y+1,x+2] = float_to_exponential(float(data.iloc[y+1,x+2])*10)
#     # print(data)




# print (partition("idk/cacti/tech_params/90nm.dat", tech_result))
