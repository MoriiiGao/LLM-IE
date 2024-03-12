import urllib.request
import requests as re
import os
import sys
# from HTMLParser import HTMLParser
from html.parser import HTMLParser
# fname = r"C:\Python34\html.htm"

### 读取html
tagstack = []
html_str = ''
title_label = 0
b_label = 0
page = 1
# global title_label
# global b_label
class MyParser(HTMLParser):
    def handle_starttag(self, tag, attrs): tagstack.append(tag)
    # handle_starttag(tag, attrs)
    def handle_endtag(self, tag): tagstack.pop()
    def handle_data(self, data):
        global html_str
        global title_label
        global b_label
        global page
        if data.strip():
            tag_index = 0
            for tag in tagstack:
                if len(tagstack)>1:
                    tag_next = tag_index + 1
                    if tag=='title':
                        if 'doi' in data[:]:
                            continue
                        elif 'No Job Name' in data[:]:
                            continue
                        elif len(data[:])==0:
                            continue
                        else:
                            html_str = data[:]
                            # title_label = title_label + 1
                            break
                    elif tag=='b':
                        if title_label==0 and b_label==0:
                            if 'doi' in data[:]:
                                # html_str = html_str + '\n' +html_cl
                                continue
                            elif 'www' in data[:]:
                                # html_str = html_str + '\n' +html_cl
                                continue
                            elif data[:].isdigit():
                                # html_str = html_str + '\n' +html_cl
                                continue
                            else:
                                if len(data[:])>40:
                                    html_str = data[:]
                                    b_label = b_label + 1
                                    break
                    elif tag=='p':
                        if tag_index<len(tagstack)-1:
                            if tagstack[tag_next]=='b':
                                continue  
                tag_index = tag_index + 1                    

def title_str(html):
    my=MyParser()
    my.feed(html)
    return html_str













# import urllib.request
# import requests as re
# import os
# import sys
# from Utility import getWorkSpace

# # from HTMLParser import HTMLParser
# from html.parser import HTMLParser
# # fname = r"C:\Python34\html.htm"

# ### 读取html
# # data_dir = getWorkSpace()
# # # html存放路径
# # file_path = data_dir + "/pdf_html/"
# # # txt存放路径
# # txt_path = data_dir + "/pdf_txt2/"
# tagstack = []
# html_str = ''
# title_label = 0
# b_label = 0
# page = 1
# # global title_label
# # global b_label
# class MyParser(HTMLParser):
#     def handle_starttag(self, tag, attrs): tagstack.append(tag)
#     # handle_starttag(tag, attrs)
#     def handle_endtag(self, tag): tagstack.pop()
#     def handle_data(self, data):
#         global html_str
#         global title_label
#         global b_label
#         global page
#         if data.strip():
#             tag_index = 0
#             for tag in tagstack:
#                 if len(tagstack)>1:
#                     tag_next = tag_index + 1
#                     if tag=='title':
#                         if 'doi' in data[:]:
#                             continue
#                         elif 'No Job Name' in data[:]:
#                             continue
#                         elif len(data[:])==0:
#                             continue
#                         else:
#                             html_str = data[:]
#                             # title_label = title_label + 1
#                             break
#                     elif tag=='b':
#                         if title_label==0 and b_label==0:
#                             if 'doi' in data[:]:
#                                 # html_str = html_str + '\n' +html_cl
#                                 continue
#                             elif 'www' in data[:]:
#                                 # html_str = html_str + '\n' +html_cl
#                                 continue
#                             elif data[:].isdigit():
#                                 # html_str = html_str + '\n' +html_cl
#                                 continue
#                             else:
#                                 if len(data[:])>40:
#                                     html_str = data[:]
#                                     b_label = b_label + 1
#                                     break
#                     elif tag=='p':
#                         if tag_index<len(tagstack)-1:
#                             if tagstack[tag_next]=='b':
#                                 continue  
#                 tag_index = tag_index + 1                    

# def title_str(html):
#     my=MyParser()
#     my.feed(html)
#     return html_str