import os
from pathlib import Path
from shutil import copyfile

file_name = "simple.vtt"
base_path = os.path.dirname(os.getcwd())
subtitle_path = os.path.join(base_path, "simple_file")
new_file_name = os.path.join(subtitle_path, file_name.split(".")[0] + ".srt")
old_file_name = os.path.join(subtitle_path, file_name)

def process_subtitle(src_file, dst_file):
    print(src_file)
    f = open(src_file)
    lines = f.readlines()
    f.close()

    line_index = 1
    subtitle_begin = 0
    new_line = []
    total_end_time = []
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
        if index %3 == 1 and len(lines[index]) != 0:
            line_start_index = 0
            line_end_index = 0
            line_content = ""
            bracket_pair = []
            end_time_point = []
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
                if len(lines[index][bracket_pair[item_data_index][0] + 1:bracket_pair[item_data_index][1]].split(":")) == 3:
                    #print(lines[index][bracket_pair[item_data_index][0] + 1:bracket_pair[item_data_index][1]])
                    end_time_point.append(lines[index][bracket_pair[item_data_index][0] + 1:bracket_pair[item_data_index][1]])
                if item_data_index == len(bracket_pair) - 1:
                    line_end_index = len(lines[index]) - 1
                else:
                    line_end_index = bracket_pair[item_data_index + 1][0]
                line_start_index = bracket_pair[item_data_index][1] + 1
                #line_content.append(lines[index][line_start_index:line_end_index])
                line_content += lines[index][line_start_index:line_end_index]
            new_line.append(line_content)
            new_line.append("\n")
            if len(end_time_point) > 0:
                #print(end_time_point[-1])
                total_end_time.append(end_time_point[-1])
            else:
                total_end_time.append("")
                #print("Empty")
    #print(new_line)
    tmp_list = []
    #print(total_end_time)
    end_point_index = 0
    for item_new_line in new_line:
        if item_new_line != '\n':
            if item_new_line.isdigit():
                #print("\n\n")
                tmp_list.append("\n")
            if item_new_line[0].isdigit() and len(item_new_line.split(":")) == 5:
                if total_end_time[end_point_index] != "":
                    tmp_list.append(item_new_line.split("-->")[0] + "-->" + total_end_time[end_point_index])
                else:
                    tmp_list.append(item_new_line)
                #print(item_new_line.split("-->")[0] + "-->" + total_end_time[end_point_index])
                print(tmp_list[-1])
                end_point_index+=1
                tmp_list.append("\n")
                continue
            #print("%s"%(item_new_line))
            tmp_list.append(item_new_line)
            tmp_list.append("\n")
    #print(tmp_list)

    tmp_list = tmp_list[1:-2]
    #print(len(tmp_list))
    #print(total_end_time)

    f = open(dst_file, "w")
    f.writelines(tmp_list)
    f.close()


base_path = "E:/BaiduNetdiskDownload"
abs_path = ""
for folder_item in os.listdir(base_path):
    if Path(os.path.join(base_path, folder_item)).is_dir():
        abs_path = base_path + "/" + folder_item
        for file_item in os.listdir(abs_path):
            if file_item.split(".")[-1] == "vtt":
            #print(os.path.join(base_path, file_item))
            #print(os.path.join(base_path, file_item[:-3] + "srt"))
            #print(os.path.join(base_path, file_item[:-3] + "srt"))
                try:
                   process_subtitle(os.path.join(abs_path, file_item), os.path.join(abs_path, file_item[:-3] + "srt"))
                except:
                    print("===================%s has error================="%(os.path.join(abs_path, file_item)))
                    continue
#process_subtitle(old_file_name, new_file_name)


