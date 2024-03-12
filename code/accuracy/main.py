import os
import shutil
import json
import re
from Utility import getWorkSpace
from LLM_API import chatgpt_API, ERNIE_Bot_API, qwen72_API, AndesGPT_API, ChatGLM_API, LLaMa2_API, Mixtral_API
from accuracy.LLM_API import LLaMa2_api

json_path = 'D:/college/li/准确率测试/6.5（数据更新）/test/'
zong_path = 'D:/college/li/准确率测试/6.5（数据更新）/'

# 准确率测试
def test_accuracy():
    for dirpath, dirnames, filenames in os.walk(json_path):
        continue
    data_list = []
    for file in filenames:
        json_new = {"tokens":'',"entities":[],"relations":[]}
        # print(json_path+file)
        with open(json_path+file,'r', encoding='utf8') as fp:
            json_data = json.load(fp) 
        json_data_list = []
        contentlist =  re.split(r'[\s,“”\xa0\n^:";>/()\]\[]',json_data['content'])
        # json_data_list.append(json_data['content']) 
        # json_data_list.append(contentlist)  
        # json_new['tokens']=json_data_list
        # 去除空值
        while "" in contentlist:# 判断是否有空值在列表中
            contentlist.remove("")
        json_new['tokens']=contentlist
        tokens = []
        for token in contentlist:
            if token != '' :
                tokens.append(token)
        entity_detail = {}
        end_index = 0
        for i, each in enumerate(tokens):
            tempdic = {}
            # print(end_index)
            #找的是匹配的第一个
            start_index = json_data["content"].find(each, end_index)
            end_index = start_index + len(each)
            tempdic["start"] = start_index
            tempdic["end"] = end_index
            tempdic["phrase"] = each
            entity_detail[i] = tempdic
        # print(entity_detail)
        entities = []
        #newid
        num = 0
        for item in json_data["labels"]:
            start = 0
            end = 0
            #从字符到单词的映射
            for each in entity_detail:
                if entity_detail[each]["start"] == item["startIndex"] :
                    start = each
                #在start附近+-2
                elif item["startIndex"] in range(entity_detail[each]["start"] - 2 ,entity_detail[each]["start"] + 2 ):
                    start = each
                #在start与end 之间
                elif item["startIndex"] in range(entity_detail[each]["start"],entity_detail[each]["end"]):
                    start = each

                if entity_detail[each]["end"] == item["endIndex"] :
                    end = each
                elif item["endIndex"] in range(entity_detail[each]["end"] - 2 ,entity_detail[each]["end"] + 2 ):
                    end = each
                elif item["endIndex"] in range(entity_detail[each]["start"],entity_detail[each]["end"]):
                    end = each
            #这是从文中取的，不一定与真实值一致
            # item["entity"] = temp["content"][item["startIndex"]:item["endIndex"]]
            true_phrase = ""
            for i in range(start,end+1):
                true_phrase = true_phrase + entity_detail[i]["phrase"] + " "
            # if true_phrase=="":
            #     print(json_path+file)
            json_new['entities'].append({
                "id": 0,
                "entity":true_phrase,
                "start": start,
                "end": end +1,
                "type":item["text"]
            })

        data_list.append(json_new)
        # print(len(data_list))
        
    with open(zong_path+'testhg.json', 'w', encoding='utf8') as json_file:
        listallarr2=json.dumps(data_list,ensure_ascii=False)
        json_file.write(listallarr2)
        
    #     file_count = file_count + 1
    # file_count = file_count + 1
    # file_name_list=os.listdir(new_json_path+dir_name+'/')
        

# 大模型抽取结果
def LLM_prompt(file_path, prompt, model_name='gpt2', length=100, temperature=0.7, num_return_sequences=1):
    
    with open(file_path, "r", encoding='utf8') as file:
        input_text = file.read()

    prompt = """
        Please extract field information from the above paper content, requiring:
        1. If there is no relevant information about the field in the text, fill in/for that field;
        2. If relevant information about a field appears in the text, you don't need to summarize it. You can simply extract the four sentences above and below the text where the field is located;
        3. Require to display in a table format, with two columns, one for the field and the other for the original content;
        4. The extracted information is the original content rather than the summary;
        5. The fields to be extracted include:

        Title
        Author
        Unit
        DOI
        Published Time
        Zeolite
        Magazine
        Gel Composition
        Silicon Source
        Aluminum Source
        Alkali Source
        Cations
        Fluorine Source
        Crystallization Conditions temperature
        Crystallization Conditions time
        Crystallization Conditions rotational speed
        Germanium Source
        Phosphorus Source
        Template Agent
        Molecular Sieve Structure Information
    """

    tokenizer = GPT2Tokenizer.from_pretrained(model_name)
    model = GPT2LMHeadModel.from_pretrained(model_name)

    # Encode context the generation is conditioned on
    input_ids = tokenizer.encode(prompt, return_tensors='pt')

    # Generate text
    output = model.generate(input_ids, 
                            max_length=length, 
                            num_return_sequences=num_return_sequences, 
                            temperature=temperature, 
                            top_k=50, 
                            top_p=0.95, 
                            eos_token_id=tokenizer.eos_token_id)
    
    # Decode and print the output text
    decoded_output = [tokenizer.decode(output[i], skip_special_tokens=True) for i in range(num_return_sequences)]
    print(decoded_output[text])
    

    
if __name__=="__main__":
    
    data_dir = getWorkSpace()
    path_pdf = data_dir + "/pdf_txt/"
    result = ""
    for root, dirs, files in os.walk(path_pdf):
        for file in files:
            file_name = path_pdf + file
            result = str(result) + "\n\n\n"+ str(LLM_prompt(file_name))


    with open(data_dir+"/result_qwen.txt", "w", encoding='utf8') as f:
        f.write(result)
        