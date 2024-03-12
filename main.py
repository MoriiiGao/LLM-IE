import os
import json
import requests
import dashscope
import json
from Logger import log
from Utility import getWorkSpace
from transformers import AutoModelForCausalLM, AutoTokenizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from progress.bar import Bar
#可以通过fill设置进度条填充符号，默认“#”
#可以通过suffix设置成百分比显示
bar = Bar("Loading", fill='#', max = 100, suffix = '%(percent)d%%')

# json_path = 'D:/college/li/准确率测试/6.5（数据更新）/test/'
# zong_path = 'D:/college/li/准确率测试/6.5（数据更新）/'

# 准确率测试
def test_accuracy(file_dir, prompt, modle_name):

    # 定义正确的数量
    right_count= 0
    # 定义总数
    sum_count = 0
    json_path = file_dir + "/test_data/"
    # 首先，获得当前文件夹下面的文件名称
    for dirpath, dirnames, filenames in os.walk(json_path):
        continue
    # 而后开始循环获得每一个json文件中的数据
    for file in bar.iter(filenames):
        # 总数加一
        sum_count = sum_count + 1

        # 打开json文件取出json数据
        with open(json_path + file, "r", encoding = "utf-8") as f:
            json_data = json.load(f)
        # # 正则项分割
        # contentlist =  re.split(r'[\s,“”\xa0\n^:";>/()\]\[]',json_data['content'])

        # 取出content
        content_text = json_data['content']

        # 正确答案
        # start_index = json_data['labels'][0]['id']['startIndex']
        # end_index = json_data['labels'][0]['id']['endIndex']
        # lable = json_data['labels'][0]['id']['text']
        start_index = json_data['labels'][0]['startIndex']
        end_index = json_data['labels'][0]['endIndex']
        lable = json_data['labels'][0]['text']
        right_answer = json_data['content'][start_index:end_index]

        # 修改后的prompt
        prompt = prompt + str(lable)

        # 调用模型
        if modle_name == "GPT4":
            model_answer = GPT4_ACC(content_text,prompt)
        elif modle_name == "ERNIE Bot":
            model_answer = ERNIE_ACC(content_text,prompt)
        elif modle_name == "Qwen72B":
            model_answer = Qwen72B_ACC(content_text,prompt)
        elif modle_name == "AndesGPT":
            model_answer = AndesGPT_ACC(content_text,prompt)
        elif modle_name == "ChatGLM":
            model_answer = ChatGLM_ACC(content_text,prompt)
        elif modle_name == "LLaMa2":
            model_answer = LLaMa2_ACC(content_text,prompt)
        elif modle_name == "Mixtral8*7":
            model_answer = Mixtral_ACC(content_text,prompt)
        else:
            log.logger.info("-------------------------------------------未发现模型--------------------------------------------")
        
        # 测试两个字段的相似度
        ## 将文本转换为向量
        vectorizer = CountVectorizer().fit_transform([right_answer, model_answer])
        vectors = vectorizer.toarray()

        ## 计算余弦相似度
        cos_sim = cosine_similarity([vectors[0]], [vectors[1]])[0][0]

        if cos_sim >= 0.85:
            right_count = right_count + 1

    # 计算准确率
    accurcy_rate = right_count/sum_count
    F1_rate = 2 * accurcy_rate/(accurcy_rate+1) 

    return accurcy_rate, F1_rate
       

# def GPT4_ACC(content_text,prompt):

def get_access_token():
    """
    使用 API Key，Secret Key 获取access_token，替换下列示例中的应用API Key、应用Secret Key
    """
        
    # url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=HWQtdD2jwy5GasBrGaknML7i&client_secret=H0hvizpZEGiNE058uW7X8yFoqgUVhywp"
    
    # payload = json.dumps("")
    # headers = {
    #     'Content-Type': 'application/json',
    #     'Accept': 'application/json'
    # }
    
    # response = requests.request("POST", url, headers=headers, data=payload)
    # return response.json().get("access_token"
    API_KEY = "HWQtdD2jwy5GasBrGaknML7i"
    SECRET_KEY = "H0hvizpZEGiNE058uW7X8yFoqgUVhywp"
    # if model == "ERNIE ROT":
    #     url = "https://aip.baidubce.com/oauth/2.0/token"
    # elif model =="LLaMa":
    url = "https://aip.baidubce.com/oauth/2.0/token"

    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))


# ERNIE ROT模型 ernie-2.0-large-en  https://huggingface.co/nghuyong/ernie-2.0-large-en
def ERNIE_ACC( content_text, prompt,model_name="nghuyong/ernie-2.0-large-en", max_length=1000):
    # # 加载预训练模型和分词器
    # tokenizer = AutoTokenizer.from_pretrained(model_name)
    # model = AutoModelForCausalLM.from_pretrained(model_name)

    # # 编码输入文本，添加必要的特殊标记（比如开始、结束标记）
    # input_text = str(content_text) + str(prompt)
    # input_ids = tokenizer.encode(input_text, return_tensors="pt")

    # # 生成回答
    # output = model.generate(input_ids, max_length=max_length, num_return_sequences=1)

    # # 解码模型输出，去掉特殊标记得到文本输出
    # generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie_bot_8k?access_token=" + get_access_token()
    
    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    })

    # payload = json.dumps({
    #     "messages": [
    #         {
    #             'role': 'system', 
    #             'content': 'You are an academic expert in petrochemicals.'},
    #         {
    #             "role": "user",
    #             "content": prompt
    #         }
    #     ]
    # })
    headers = {
        'Content-Type': 'application/json'
    }

    
    response = requests.request("POST", url, headers=headers, data=payload)
    
    # print(response.text)
    generated_text = response.text

    return generated_text
    
#  https://huggingface.co/Qwen/Qwen-72B-Chat
def Qwen72B_ACC(content_text, prompt):
    dashscope.api_key="sk-8cdbec7b7486475aaa52bb8d8b37d22c"

    # tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen-72B-Chat", trust_remote_code=True)

    # model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen-72B-Chat", device_map="auto", trust_remote_code=True).eval()
    # input_text = str(content_text) + str(prompt)
    # response = model.chat(tokenizer, input_text)
    # print("---------------------------------------------------模型开始运行-----------------------------------------------------")

    messages = [{'role': 'system', 'content': 'You are an academic expert in petrochemicals.'},
                {'role': 'user', 'content': prompt}]

    response = dashscope.Generation.call(
        dashscope.Generation.Models.qwen_turbo,
        messages=messages,
        result_format='message',  # set the result to be "message" format.
    )
    # if response.status_code == HTTPStatus.OK:
    #     print(response)
    # else:
    #     print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
    #         response.request_id, response.status_code,
    #         response.code, response.message
    #     ))
    print("---------------------------------------------------模型结束运行-----------------------------------------------------")
    # print(response.output)

    return response.output

    # return response

# def AndesGPT_ACC(data_dir, prompt):
#     test_accuracy()

# ChatGLM3-6B https://huggingface.co/THUDM/chatglm3-6b
# https://console.bce.baidu.com/tools/?u=qfdc#/api?product=AI&project=%E5%8D%83%E5%B8%86%E5%A4%A7%E6%A8%A1%E5%9E%8B%E5%B9%B3%E5%8F%B0&parent=ChatGLM2-6B-32K&api=rpc%2F2.0%2Fai_custom%2Fv1%2Fwenxinworkshop%2Fchat%2Fchatglm2_6b_32k&method=post
# chatglm-6b-32k
def ChatGLM_ACC(content_text, prompt):

    # input_text = str(content_text) + str(prompt)
    # tokenizer = AutoTokenizer.from_pretrained("THUDM/chatglm3-6b", trust_remote_code=True)
    # model = AutoModel.from_pretrained("THUDM/chatglm3-6b", trust_remote_code=True).half().cuda()
    # model = model.eval()
    # response, history = model.chat(tokenizer, input_text, history=[])
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/chatglm2_6b_32k?access_token=" + get_access_token()
    
    
    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    })
    # payload = json.dumps({
    #     "messages": [
    #         {
    #             'role': 'system', 
    #             'content': 'You are an academic expert in petrochemicals.'},
    #         {
    #             "role": "user",
    #             "content": prompt
    #         }
    #     ]
    # })
    headers = {
        'Content-Type': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    
    # print(response.text)
    response = response.text
    return response

# https://huggingface.co/meta-llama/Llama-2-70b-chat
# https://github.com/huggingface/blog/blob/main/zh/llama2.md
# https://console.bce.baidu.com/tools/?u=qfdc#/api?product=AI&project=%E5%8D%83%E5%B8%86%E5%A4%A7%E6%A8%A1%E5%9E%8B%E5%B9%B3%E5%8F%B0&parent=Llama-2&api=rpc%2F2.0%2Fai_custom%2Fv1%2Fwenxinworkshop%2Fchat%2Fllama_2_7b&method=post
# llama2-70b
def LLaMa2_ACC(content_text, prompt):

    # input_text = str(content_text) + str(prompt)
    # model = "meta-llama/Llama-2-7b-chat-hf"

    # tokenizer = AutoTokenizer.from_pretrained(model)
    # pipeline = transformers.pipeline(
    #     "text-generation",
    #     model=model,
    #     torch_dtype=torch.float16,
    #     device_map="auto",
    # )

    # generated_text = pipeline(
    #     input_text,
    #     do_sample=True,
    #     top_k=1,
    #     num_return_sequences=1,
    #     eos_token_id=tokenizer.eos_token_id,
    #     max_length=200,
    # )
    # # for seq in sequences:
    # #     log.logger.info(f"Result: {seq['generated_text']}")
    # url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/llama_2_7b?access_token=" + get_access_token()
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/llama_2_70b?access_token=" + get_access_token()
    
    
    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    })
    # payload = json.dumps({
    #     "messages": [
    #         {
    #             'role': 'system', 
    #             'content': 'You are an academic expert in petrochemicals.'},
    #         {
    #             "role": "user",
    #             "content": prompt
    #         }
    #     ]
    # })
    headers = {
        'Content-Type': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    
    # print(response.text)
    generated_text = response.text

    return generated_text


# mistralai/Mixtral-8x7B-Instruct-v0.1 https://huggingface.co/mistralai/Mixtral-8x7B-Instruct-v0.1
# https://console.bce.baidu.com/tools/?u=qfdc#/api?product=AI&project=%E5%8D%83%E5%B8%86%E5%A4%A7%E6%A8%A1%E5%9E%8B%E5%B9%B3%E5%8F%B0&parent=Mixtral-8x7B-Instruct&api=rpc%2F2.0%2Fai_custom%2Fv1%2Fwenxinworkshop%2Fchat%2Fmixtral_8x7b_instruct&method=post
def Mixtral_ACC(content_text, prompt):

    # input_text = str(content_text) + str(prompt)
    # model_id = "mistralai/Mixtral-8x7B-Instruct-v0.1"
    # tokenizer = AutoTokenizer.from_pretrained(model_id)

    # model = AutoModelForCausalLM.from_pretrained(model_id)

    # inputs = tokenizer(input_text, return_tensors="pt")

    # outputs = model.generate(**inputs, max_new_tokens=20)
    
    # generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/mixtral_8x7b_instruct?access_token=" + get_access_token()
    
    # payload = json.dumps("")
        
    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    })
    # payload = json.dumps({
    #     "messages": [
    #         {
    #             'role': 'system', 
    #             'content': 'You are an academic expert in petrochemicals.'},
    #         {
    #             "role": "user",
    #             "content": prompt
    #         }
    #     ]
    # })
    headers = {
        'Content-Type': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    
    # print(response.text)
    generated_text = response.text

    return generated_text


    
if __name__=="__main__":
    
    data_dir = getWorkSpace()
    # prompt
    prompt = """
        Please extract field information from the above paper content, requiring:
        1. If there is no relevant information about the field in the text, fill in/for that field;
        2. If relevant information about a field appears in the text, you don't need to summarize it. You can simply extract the four sentences above and below the text where the field is located;
        3. Require to display in a table format, with two columns, one for the field and the other for the original content;
        4. The extracted information is the original content rather than the summary;
        5. The fields to be extracted include:
    """
    
    log.logger.info("-------------------------------------------准确率测试开始--------------------------------------------")

    # # GPT4
    # log.logger.info("-------------------------------------------GPT4 结果--------------------------------------------")
    # accurcy_rate, F1_rate = test_accuracy(data_dir, prompt, modle_name  = "GPT4")
    # log.logger.info("GPT4的抽取准确率为："+ str(accurcy_rate))
    # log.logger.info("GPT4的F1分数为："+ str(accurcy_rate))
    # log.logger.info("-----------------------------------------------------------------------------------------------")

    # ERNIE Bot
    log.logger.info("-------------------------------------------ERNIE Bot 结果--------------------------------------------")
    accurcy_rate, F1_rate = test_accuracy(data_dir, prompt, modle_name  = "ERNIE Bot")
    log.logger.info("ERNIE Bot的抽取准确率为："+ str(accurcy_rate))
    log.logger.info("ERNIE Bot的F1分数为："+ str(accurcy_rate))
    log.logger.info("-----------------------------------------------------------------------------------------------")


    # Qwen 72B
    log.logger.info("-------------------------------------------Qwen72B 结果--------------------------------------------")
    accurcy_rate, F1_rate = test_accuracy(data_dir, prompt, modle_name  = "Qwen72B")
    log.logger.info("Qwen72B的抽取准确率为："+ str(accurcy_rate))
    log.logger.info("Qwen72B的F1分数为："+ str(accurcy_rate))
    log.logger.info("-----------------------------------------------------------------------------------------------")


    # AndesGPT
    log.logger.info("-------------------------------------------AndesGPT 结果--------------------------------------------")
    accurcy_rate, F1_rate = test_accuracy(data_dir, prompt, modle_name  = "AndesGPT")
    log.logger.info("AndesGPT的抽取准确率为："+ str(accurcy_rate))
    log.logger.info("AndesGPT的F1分数为："+ str(accurcy_rate))
    log.logger.info("-----------------------------------------------------------------------------------------------")


    # ChatGLM
    log.logger.info("-------------------------------------------ChatGLM 结果--------------------------------------------")
    accurcy_rate, F1_rate = test_accuracy(data_dir, prompt, modle_name  = "ChatGLM")
    log.logger.info("ChatGLM的抽取准确率为："+ str(accurcy_rate))
    log.logger.info("ChatGLM的F1分数为："+ str(accurcy_rate))
    log.logger.info("-----------------------------------------------------------------------------------------------")




    log.logger.info("-------------------------------------------LLaMa2 结果--------------------------------------------")
    accurcy_rate, F1_rate = test_accuracy(data_dir, prompt, modle_name  = "LLaMa2")
    log.logger.info("LLaMa2的抽取准确率为："+ str(accurcy_rate))
    log.logger.info("LLaMa2的F1分数为："+ str(accurcy_rate))
    log.logger.info("-----------------------------------------------------------------------------------------------")



    log.logger.info("-------------------------------------------Mixtral8*7 结果--------------------------------------------")
    accurcy_rate, F1_rate = test_accuracy(data_dir, prompt, modle_name  = "Mixtral8*7")
    log.logger.info("Mixtral8*7的抽取准确率为："+ str(accurcy_rate))
    log.logger.info("Mixtral8*7的F1分数为："+ str(accurcy_rate))
    log.logger.info("-----------------------------------------------------------------------------------------------")


    log.logger.info("-------------------------------------------准确率测试结束--------------------------------------------")