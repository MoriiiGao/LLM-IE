# 引入模型所需要的包
import os
import extract_txt
import cross
import pdf_th
from Utility import getWorkSpace
from Logger import log

data_dir = getWorkSpace()

if __name__ == "__main__":
    
    # 路径设置
    path_pdf = data_dir + '/pdf_files/'
    path_txt = data_dir + '/pdf_txt/'
    path_html = data_dir + '/pdf_html/'

    # 程序开始
    log.logger.info('--------------------------start process-------------------------------') 

    # 得到当前文件夹下面的文件
    for root, dirs, files in os.walk(path_pdf):
        for file in files:
            file_name = path_pdf + file
            pdf_file = path_html + str(file.split(".")[0]) + ".html"
            # print("————————————————————————————————————html路径——————————————————————————————————————")
            # print(pdf_file)

            log.logger.info('post file is '+ file_name)

            # 全局变量pdf_txt 用于记录pdf转成的文本的内容
            pdf_txt = ""
            log.logger.info(data_dir)
            # 修改这里的抽取函数，修改为pdfbox
            log.logger.info('-----------------文件抽取开始--------------------')
            pdf_txt = extract_txt.pdfbox_cq(data_dir,file_name, pdf_file, path_html)
            log.logger.info('-----------------文件抽取结束--------------------')

            log.logger.info('-----------------跨行处理开始--------------------')
            pdf_txt = cross.pdf_cross(data_dir+'/dictionary/',pdf_txt)
            log.logger.info('-----------------跨行处理结束--------------------')
            # log.logger.info(pdf_txt)
            log.logger.info('-----------------字符替换开始--------------------')
            # log.logger.info(pdf_txt)
            pdf_txt = pdf_th.pdf_th(data_dir+'/dictionary/',pdf_txt)
            # log.logger.info(pdf_txt)
            log.logger.info('-----------------字符替换结束--------------------')


            # 文件保存
            txt_file = str(file.split(".")[0])
            pdf_txt = str(pdf_txt)

            with open(path_txt+txt_file+".txt", "w", encoding='utf-8') as f:
                f.write(pdf_txt)
