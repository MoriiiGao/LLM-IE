import re
from Logger import log
import pandas as pd

def pdf_th(path_cross,pdf_txt):
    pdf_txt_new = ''
    json_lines = pdf_txt.split('\n')
    json_lines = [json_line +'\n' for json_line in json_lines]
    with open(path_cross+'th.txt','r') as f:
        cross_lines = f.readline()
    for cross_line in cross_lines:
        if cross_line in pdf_txt:
            pdf_txt_new = pdf_txt.replace(cross_line,' ') 
    # pdf_txt_new = pdf_txt_new.   
    return pdf_txt_new

def Germanic_str_replace(path_cross,pdf_txt):
    df1 = pd.read_excel(path_cross+'th.xlsx',sheet_name = 'Sheet1')
    for replce_index in range(df1.iloc[:,0].size):
        # log.logger.info('-----------------------------------------')
        # log.logger.info(df1.loc[replce_index,'origon'])
        if df1.loc[replce_index,'origon'] in pdf_txt:
            log.logger.info('-----------------替换----------------')
            pdf_txt = pdf_txt.replace(df1.loc[replce_index,'origon'],df1.loc[replce_index,'new'])
    # print(df1.loc[0,'origon'])
    # print(type(df1.loc[0,'origon']))
    if 'u\u0308' in pdf_txt:
        log.logger.info('-----------------替换1----------------')
        pdf_txt = pdf_txt.replace('u\u0308','u')
    return pdf_txt