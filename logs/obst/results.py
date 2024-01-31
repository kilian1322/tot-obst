import os
import json

def get_info_from_file(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
        info = []
        final_ys = None
        # Retrieve the information you need from the JSON data
        if '0-shot' in file_path:
            info.append('0-shot')
        elif 'naive_cot' in file_path:
            info.append('cot')
        elif 'naive_standard' in file_path:
            info.append('standard')
        elif 'gpt-3.5-turbo-1106' in file_path:
            info.append("tot")
            final_ys = data[0]['ys']

        else: 
            return (None, None)
        
        info.append(data[0]['idx'])
        info.append(data[0]['usage_so_far']['completion_tokens'])
        info.append(data[0]['usage_so_far']['prompt_tokens'])
        info.append(data[0]['usage_so_far']['cost'])
        
        infos = data[0]['infos'] 
        has_one = any(info['r'] == 1 for info in infos)
        

        if has_one:
            info.append(1)
        else:
            info.append(0)
            
        
    return (info, final_ys)

directory = '.\logs\obst'
info_list = []
final_yses = []

for filename in os.listdir(directory):
    if filename.endswith('.json'):
        file_path = os.path.join(directory, filename)
        info, final_ys = get_info_from_file(file_path)
        if info is not None:
            info_list.append(info)
        if final_ys is not None:
            final_yses.append(final_ys)

for i in info_list:
    print(i, "\n")
    
print("-----------------------------------------------------------------------------")
    
for i in final_yses:
    print(i, "\n")
    
    
# Group the info_list by the first element of each sublist
grouped_info = {}
for info in info_list:
    key = info[0]
    if key not in grouped_info:
        grouped_info[key] = []
    grouped_info[key].append(info[-1])

# Sum the values in each group and store them in a list
summed_values = []
for key, values in grouped_info.items():
    summed_values.append(sum(values))

print(summed_values)

cost = [0] * 16
for i in info_list:
    if i[0] == '0-shot':
        if i[1] < 5:
            tmp = 0
        elif i[1] < 10:
            tmp = 1
        elif i[1] < 15:
            tmp = 2
        else:
            tmp = 3
    elif i[0] == 'standard':
        if i[1] < 5:
            tmp = 4
        elif i[1] < 10:
            tmp = 5
        elif i[1] < 15:
            tmp = 6   
        else:
            tmp = 7
    elif i[0] == 'cot':
        if i[1] < 5:
            tmp = 8
        elif i[1] < 10:
            tmp = 9
        elif i[1] < 15:
            tmp = 10 
        else:
            tmp = 11
    elif i[0] == 'tot':
        if i[1] < 5:
            tmp = 12
        elif i[1] < 10:
            tmp = 13
        elif i[1] < 15:
            tmp = 14
        else:
            tmp = 15

    cost[tmp] += i[2] + i[3]
    
print(cost)


          

# Divide every value in cost by 5
for i in range(len(cost)):
    cost[i] /= 5

print(cost)
