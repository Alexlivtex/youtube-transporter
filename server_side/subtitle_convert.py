import os

def process_subtitle(src_file, dst_file):
    subtitle_content = dict()
    if not os.path.exists(src_file):
        print("{} not exists".format(src_file))
        return

    f_src = open(src_file, "r")
    lines = f_src.readlines()
    f_src.close()

    subtitle_begin = 0
    for line in lines:
        if not line[0].isdigit():
            subtitle_begin += 1
        else:
            break

    if subtitle_begin == 4 and len(lines[subtitle_begin].split(":")) == 5:
        f = open(dst_file, "w")
        f.writelines(lines[subtitle_begin:])
        f.close()
        return

    original_sub_content = lines[subtitle_begin:]

    #print(original_sub_content)
    sub_title_index = 1

    for line_num in range(len(original_sub_content)):
        if original_sub_content[line_num][0].isdigit() and line_num % 3 == 0:
            if line_num < len(original_sub_content) - 3 and original_sub_content[line_num + 3][0].isdigit():
                time_track_1st = original_sub_content[line_num].strip()[:-26].split(" --> ")[0]
                time_track_2nd = original_sub_content[line_num + 3].strip()[:-26].split(" --> ")[0]
                time_track = " --> ".join([time_track_1st, time_track_2nd])
            else:
                time_track = original_sub_content[line_num][:-26].strip()

            while True:
                if line_num < len(original_sub_content) - 1:
                    left_braket = original_sub_content[line_num + 1].find('<')
                    right_braket = original_sub_content[line_num + 1].find('>')
                    if left_braket == -1 and right_braket == -1:
                        break

                    original_sub_content[line_num + 1] = original_sub_content[line_num+1][0:left_braket] + original_sub_content[line_num+1][right_braket + 1:]

            subtitle_content[sub_title_index] = [time_track, original_sub_content[line_num+1]]
            sub_title_index+=1

    total_dst_list = list()
    for index in subtitle_content:
        total_dst_list.append(str(index) + "\n")
        total_dst_list.append(subtitle_content[index][0] +"\n")
        total_dst_list.append(subtitle_content[index][1] + "\n")

    f_dst = open(dst_file, "w")
    f_dst.writelines(total_dst_list)
    f_dst.close()
