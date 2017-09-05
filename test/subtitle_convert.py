import os
from pathlib import Path
from shutil import copyfile

file_name = "simple.vtt"
base_path = os.path.dirname(os.getcwd())
subtitle_path = os.path.join(base_path, "simple_file")
new_file_name = os.path.join(subtitle_path, file_name.split(".")[0] + ".srt")
old_file_name = os.path.join(subtitle_path, file_name)

def process_subtitle(src_file, dst_file):
    f = open(src_file)
    lines = f.readlines()
    f.close()

    line_index = 1
    subtitle_begin = 0
    new_line = []
    new_line.append(str(line_index))
    new_line.append("\n")

    for line in lines:
        if not line[0].isdigit():
            subtitle_begin += 1
        else:
            break

    lines = lines[subtitle_begin:]
    for index in range(len(lines)):
        if lines[index] is "\n":
            line_index += 1
            new_line.append(str(line_index))
            #new_line.append("\n")
        if index % 3 == 0 and lines[index][0].isdigit() is True:
            for time_index in range(len(lines[index])):
                if lines[index][time_index].isalpha() is True:
                    line_end_index = time_index
                    #print(lines[index][0:line_end_index])
                    new_line.append(lines[index][0:line_end_index])
                    new_line.append("\n")
                    break
        if index %3 != 0 and len(lines[index]) != 0:
            line_start_index = 0
            line_end_index = 0
            line_content = ""
            bracket_pair = []
            for subtitle_index in range(len(lines[index])):
                if lines[index][subtitle_index] == "<":
                    line_start_index = subtitle_index
                if lines[index][subtitle_index] == ">":
                    line_end_index = subtitle_index
                    bracket_pair.append([line_start_index, line_end_index])
                else:
                    continue

            line_start_index = -1
            line_end_index = -1
            if lines[index][0] != "<":
                if len(bracket_pair) > 0:
                    #line_content.append(lines[index][0:bracket_pair[0][0]])
                    line_content += lines[index][0:bracket_pair[0][0]]
                else:
                    #line_content.append(lines[index][:])
                    line_content += lines[index][:]

            for item_data_index in range(len(bracket_pair)):
                if bracket_pair[item_data_index][1] == len(lines[index]) - 1:
                    break
                if item_data_index == len(bracket_pair) - 1:
                    line_end_index = len(lines[index]) - 1
                else:
                    line_end_index = bracket_pair[item_data_index + 1][0]
                line_start_index = bracket_pair[item_data_index][1] + 1
                #line_content.append(lines[index][line_start_index:line_end_index])
                line_content += lines[index][line_start_index:line_end_index]
            new_line.append(line_content)
            new_line.append("\n")
    #print(new_line)
    tmp_list = []
    for item_new_line in new_line:
        if item_new_line != '\n':
            if item_new_line.isdigit():
                #print("\n\n")
                tmp_list.append("\n")
            #print("%s"%(item_new_line))
            tmp_list.append(item_new_line)
            tmp_list.append("\n")
    #print(tmp_list)

    tmp_list = tmp_list[1:-2]
    f = open(dst_file, "w")
    f.writelines(tmp_list)
    #.close()


base_path = "/root/tmp/Python for Finance with Zipline and Quantopian"
for file_item in os.listdir(base_path):
    if file_item.split(".")[-1] == "vtt":
        #print(os.path.join(base_path, file_item))
        #print(os.path.join(base_path, file_item[:-3] + "srt"))
        process_subtitle(os.path.join(base_path, file_item), os.path.join(base_path, file_item[:-3] + "srt"))
#process_subtitle(old_file_name, new_file_name)



