# 首先调用jar包得到html文件
# 而后从html中抽取<title></title>以及<p></p>中的数据
# 最后将之返回
# import os
# import subprocess
# import urllib.request
# import os
# import sys
# from Logger import log
# from html.parser import HTMLParser
# from unittest import result
# from bs4 import BeautifulSoup
# import title
# import requests

# def pdfbox_cq(file_path,param, pdf_file):
#     log.logger.info('-----------------start method pdfbox_cq--------------------')
#     jar_path = file_path+'/pdfbox-app-3.0.0-alpha2.jar'
#     # execute = "java -jar {} export:text -html=true --input=\"{}\"".format(jar_path, param)
#     execute = "java -Djava.awt.headless=true -jar {} export:text -html=true --input=\"{}\" --output=\"{}\"".format(jar_path, param, pdf_file)
#     output = subprocess.Popen(execute, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
#     print("-------------------------------------------------Output----------------------------------------------------")
#     print(output)
#     res = output.stdout.readlines()
#     # title_str = ''
#     # result,title_str = html2txt(pdf_file)
#     result= html2txt(pdf_file)
#     # if '\n' in title_str:
#     #     new_title_str = title_str.split('\n')[0]
#     # else:
#     #     new_title_str = title_str
#     # new_title = 'Title: '+ new_title_str
#     # result = result.replace(new_title_str,new_title)
#     return result

# def html2txt(pdf_file):
#     with open(pdf_file, "r", encoding='utf-8') as f:
#         html = f.read()
#     # soup = BeautifulSoup(requests.get(url).content, 'html.parser')
#         soup = BeautifulSoup(html, 'html.parser')
#         text = soup.get_text()

#     return text

#     # # head, tail = os.path.split(param)
#     # # path_html = head+'/'+tail.strip('.pdf')+'.html'
#     # # print('-------------------------------HTML路径-------------------------------------')
#     # # print(path_html)
#     # f = open(pdf_file, "r", encoding='utf-8')
#     # html = f.read()
#     # title_str = title.title_str(html)
#     # soup = BeautifulSoup(html,'html.parser')
#     # txt = soup.get_text()
#     # lines = txt.split('\n')
#     # result = []
#     # paragraph = []
#     # for line in lines: 
#     #     current_line = line.strip()
#     #     if current_line == '' :
#     #         paragraph_txt = ' '.join(paragraph).strip()
#     #         if paragraph_txt != '' :
#     #             result.append(paragraph_txt)
#     #             result.append('\n')
#     #             paragraph = []
#     #     paragraph.append(current_line)
#     # return '\n'.join(result).strip(), title_str


import os
import subprocess
import urllib.request
import requests as re
import os
import sys
from Logger import log
from html.parser import HTMLParser
from unittest import result
from bs4 import BeautifulSoup
import title



def pdfbox_cq(file_path,param, pdf_file,path_html):
    log.logger.info('-----------------start method pdfbox_cq--------------------')
    jar_path = file_path+'/pdfbox-app-3.0.0-alpha2.jar'
    # execute = "java -jar {} export:text -html=true --input=\"{}\"".format(jar_path, param)
    execute = "java -Djava.awt.headless=true -jar {} export:text -html=true --input=\"{}\" --output=\"{}\"".format(jar_path, param, pdf_file)
    output = subprocess.Popen(execute, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print("-------------------------------------------------Output----------------------------------------------------")
    print(output)
    res = output.stdout.readlines()
    title_str = ''
    result,title_str = html2txt(param,path_html)
    if '\n' in title_str:
        new_title_str = title_str.split('\n')[0]
    else:
        new_title_str = title_str
    new_title = 'Title: '+ new_title_str
    result = result.replace(new_title_str,new_title)
    return result

# def pdfbox_cq(file_path,param):
#     log.logger.info('-----------------start method pdfbox_cq--------------------')
#     jar_path = file_path+'/pdfbox-app-3.0.0-alpha2.jar'
#     # execute = "java -jar {} export:text -html=true --input=\"{}\"".format(jar_path, param)
#     execute = "java -Djava.awt.headless=true -jar {} export:text -html=true --input=\"{}\"".format(jar_path, param)
#     output = subprocess.Popen(execute, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
#     res = output.stdout.readlines()
#     title_str = ''
#     result,title_str = html2txt(param)
#     if '\n' in title_str:
#         new_title_str = title_str.split('\n')[0]
#     else:
#         new_title_str = title_str
#     new_title = 'Title: '+ new_title_str
#     result = result.replace(new_title_str,new_title)
    # return result

def html2txt(param, path_html):
    head, tail = os.path.split(param)
    path_full = path_html+'/'+tail.strip('.pdf')+'.html'
    f = open(path_full, "r", encoding='utf-8')
    html = f.read()
    title_str = title.title_str(html)
    soup = BeautifulSoup(html,'html.parser')
    txt = soup.get_text()
    lines = txt.split('\n')
    result = []
    paragraph = []
    for line in lines: 
        current_line = line.strip()
        if current_line == '' :
            paragraph_txt = ' '.join(paragraph).strip()
            if paragraph_txt != '' :
                result.append(paragraph_txt)
                result.append('\n')
                paragraph = []
        paragraph.append(current_line)
    return '\n'.join(result).strip(), title_str
