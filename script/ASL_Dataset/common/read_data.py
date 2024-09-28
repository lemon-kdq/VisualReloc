import os

def read_data(file,s = ',',skip_first_line = True):
    data = []
    with open(file, 'r') as file:
    # 跳过第一行
        cur_line = 0
        for line in file:
            cur_line = cur_line + 1
            if skip_first_line == True:
                if cur_line > 1:
                    data.append(line.strip().split(s))
            else:
                data.append(line.strip().split(s))
    return data


def list_files_in_directory(directory):
    file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            absolute_path = os.path.join(root, file)
            file_list.append((file, absolute_path))
    file_list.sort(key=lambda x: x[0])
    return file_list
