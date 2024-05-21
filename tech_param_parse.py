
import pandas as pd
import os
import subprocess

names = ["architecture", "current", "semiconductor", "SRAM_data", "CAM_data", "DRAM_data", "DRAM_cell", "chip_data_dict", "wire", "TSV_data"]

def float_to_exponential(num):
    return format(num, "e")

# read the unit header but don't add the column label to it 
def parse(file, first, last):
    chunk = file.iloc[first:last]
    chunk= chunk['parameters'].str.split(expand = True)
    chunk = chunk.reset_index(drop=True)
    chunk.loc[len(chunk)] = None
    return chunk

def partition(tech_param):
    tech_param = pd.read_csv(tech_param, names = ['parameters'])

    architecture = parse(tech_param, 1, 13)
    architecture.columns =['parameters', '(unit)', 'hp','lstp','lop','lp-dram ','comm-dram']

    current = parse(tech_param, 14, 36)
    current.columns =['parameters', '(unit)', 'temp', 'hp','lstp','lop','lp-dram ','comm-dram']

    semiconductor = parse(tech_param, 37, 44)
    semiconductor.columns =['parameters', '(unit)', 'hp', 'lstp', 'lop', 'lp-dram', 'comm-dram']

    SRAM_data = parse(tech_param, 46, 51)
    SRAM_data.columns =['parameters', '(unit)', 'cell_type', 'hp', 'lstp', 'lop','lp-dram','comm-dram']

    CAM_data = parse(tech_param, 53, 58)
    CAM_data.columns =['parameters', '(unit)', 'cell_type', 'hp', 'lstp', 'lop','lp-dram','comm-dram']

    DRAM_data = parse(tech_param, 60, 66)
    DRAM_data.columns =['parameters', '(unit)','cell_type', 'hp', 'lstp', 'lop','lp-dram','comm-dram']

    DRAM_cell= parse(tech_param, 67, 71)
    DRAM_cell.columns =['parameters', '(unit)', 'hp',  'lstp',   'lop',  'lp-dram',   'comm-dram' ]

    chip_data = parse(tech_param, 71, 78)
    chip_data.columns =[" ", "  ", "    "]
    # chip_data_dict = {chip_data[0][0]: chip_data[1][0]}
    # for x in range(8):
    #     chip_data_dict.update ({chip_data[0][x]: chip_data[1][x]})

    wire = parse(tech_param, 79, 90)
    wire.columns =['parameters','(units)', '0/0', '0/1', '0/2', '0/3', '1/0', '1/1', '1/2', '1/3' ]

    TSV_data = parse(tech_param, 91, None)
    TSV_data.columns =['parameters','(units)', '0/0', '0/1', '0/2', '0/3', '1/0', '1/1', '1/2', '1/3']

    return architecture, current, semiconductor, SRAM_data, CAM_data, DRAM_data, DRAM_cell, chip_data, wire, TSV_data




data = partition("tech_params/90nm.dat")
tech_param_dict = {names[0]:data[0]}
initialize = {"none" : []}
initialize = pd.DataFrame(data=initialize)
for x in range(10):
    tech_param_dict.update({names[x]:data[x]})

print (tech_param_dict)

initialize.to_csv('tech_params/90nmtest.dat', index=False, header=False, sep=' ')

for key in tech_param_dict:
    tech_param_dict[key].to_csv('tech_params/90nmtest.dat', mode='a', index=False, header=True, sep=' ')

# # make sure to allow targeting for each cell by header
# for y in range (len(data)):
#     for x in range (len(data.columns)):
#         cell = data.iloc[y,x]
#         if cell == "parameters":
#             break
#         if not(pd.isnull(cell)) and cell[0].isdigit():
#             data.iloc[y,x] = float_to_exponential(float(data.iloc[y,x])*1000)
#             # data.to_csv('tech_params/90nm.dat', index=False, header=True, sep=' ')

#             # print (data)
#             data = partition("tech_params/90nm.dat", tech_result)
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
