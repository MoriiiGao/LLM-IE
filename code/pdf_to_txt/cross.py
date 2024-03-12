import re
from Logger import log

def pdf_cross(path_cross,pdf_txt):
    pdf_txt_new = ''
    json_lines = pdf_txt.split('\n')
    json_lines = [json_line +'\n' for json_line in json_lines]
    with open(path_cross+'cross.txt','r') as f:
        cross_lines = f.readline()
    json_line_index = 0
    # for json_line in json_lines:
    while True:
        temp_str = ''
        temp_num = 0
        # 保证不会产生溢出
        if json_line_index<len(json_lines)-1:
            # 确定此行最后一个字符为数字
            if len(json_lines[json_line_index])>=6:
                json_line_temp = json_lines[json_line_index].replace('\n','')
                if json_line_temp[-1].isdigit():
                    for cross_line in cross_lines:
                        cross_line = cross_line.replace('\n', '')
                        if len(json_lines[json_line_index+1])>=2:
                            if cross_line in json_lines[json_line_index+1][0:2]:
                                temp_str = json_lines[json_line_index].replace('\n', '')
                                temp_str = temp_str.replace('\r', '')
                                # log.logger.info(temp_str)
                                temp_num = temp_num + 1
                                break
                        elif len(json_lines[json_line_index+1].replace('\n',''))==0:
                            if cross_line in json_lines[json_line_index+2][0:2]:
                                temp_str = json_lines[json_line_index].replace('\n', '')
                                temp_str = temp_str.replace('\r', '')
                                # log.logger.info(temp_str)
                                temp_num = temp_num+2
                                break
                        # else:
                        #     pdf_txt_new=pdf_txt_new+json_lines[json_line_index]
                elif json_line_temp[-2].isdigit():
                    for cross_line in cross_lines:
                        cross_line = cross_line.replace('\n', '')
                        if len(json_lines[json_line_index+1])>=2:
                            if cross_line in json_lines[json_line_index+1][0]:
                                temp_str = json_lines[json_line_index].replace('\n', '')
                                temp_str = temp_str.replace('\r', '')
                                # log.logger.info(temp_str)
                                temp_num = temp_num + 1
                                break
                        elif len(json_lines[json_line_index+1].replace('\n',''))==0:
                            if cross_line in json_lines[json_line_index+2][0:2]:
                                temp_str = json_lines[json_line_index].replace('\n', '')
                                temp_str = temp_str.replace('\r', '')
                                # log.logger.info(temp_str)
                                temp_num = temp_num+2
                                break
                elif 'gel:' in json_line_temp[-4:]:
                    if json_lines[json_line_index+1][0]==' ' or json_lines[json_line_index+1][0].isdigit():
                        temp_str = json_lines[json_line_index].replace('\n', '')
                        temp_str = temp_str.replace('\r', '')
                        # log.logger.info(temp_str)
                        temp_num = temp_num+2
                        break
                elif 'gel :' in json_line_temp[-5:]:
                    if json_lines[json_line_index+1][0]==' ' or json_lines[json_line_index+1][0].isdigit():
                        temp_str = json_lines[json_line_index].replace('\n', '')
                        temp_str = temp_str.replace('\r', '')
                        # log.logger.info(temp_str)
                        temp_num = temp_num+2
                        break
        if len(temp_str)==0:
            temp_str = json_lines[json_line_index]
        if temp_num==1:
            pdf_txt_new = pdf_txt_new + temp_str
            json_line_index = json_line_index + temp_num
        elif temp_num==2:
            pdf_txt_new = pdf_txt_new + temp_str + ' '
            json_line_index = json_line_index + temp_num
        elif temp_num==0:
            pdf_txt_new = pdf_txt_new + temp_str
            json_line_index = json_line_index + 1
        
        # log.logger.info(json_line_index)
        if json_line_index>=len(json_lines)-1:
            break
    # log.logger.info(pdf_txt_new[44450:44455])
    # with open(path_cross+'test.txt','w',encoding='utf8') as f:
    #     f.write(pdf_txt_new)
    return pdf_txt_new