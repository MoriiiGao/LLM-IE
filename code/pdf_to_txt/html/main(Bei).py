from flask import Flask, render_template, request, redirect, url_for, session
import model_api as ma

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 确保设置了秘密密钥

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # 处理 POST 请求的数据
        input_text = request.form['inputText']
        session['input_text'] = input_text


        processed_text = ma.model_API(input_text)
        raw_data = processed_text['choices'][0]['message']['content']

        # 格式转换
        data = []
        for line in raw_data.strip().split('\n'):
            if '|' in line:
                # field, content = line.split('|', 1)
                field = line.split('|')[1]
                content = line.split('|')[2]
                data.append({"Field": field.strip(), "Content": content.strip()})

        # 过滤表格中的"--"元素
        filtered_data = [row for row in data[1:] if "---" not in row.values()]

        # 将处理后的数据存储在 session 中
        session['data'] = filtered_data
        session['show_output'] = True  # 设置标志以显示输出

        return redirect(url_for('index'))
    else:
        # # 从 session 中获取数据
        # data = session.get('data', [])
        # show_output = session.pop('show_output', False)  # 获取并重置标志
        # return render_template('index.html', data=data, show_output=show_output)
        # 从 session 中获取数据
        data = session.get('data', [])
        # input_text = session.get('input_text', '')  # 获取输入文本
        # show_output = session.pop('show_output', False)  # 获取并重置标志
        # return render_template('index.html', data=data, show_output=show_output, input_text=input_text)
        show_output = session.pop('show_output', False)  # 获取并重置标志
        input_text = ''  # 重置输入文本
        return render_template('index.html', data=data, show_output=show_output, input_text=input_text)

@app.route('/clear', methods=['POST'])
def clear():
    # session.pop('data', None)  # 清除 session 中的数据
    session.pop('data', None)  # 清除 session 中的数据
    session.pop('input_text', None)  # 清除输入文本
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

























# from flask import Flask, render_template, request, redirect, url_for, session
# import model_api as ma
# app = Flask(__name__)


# @app.route('/')
# def index():
#     # return render_template('index.html', output="")  # 初始化输出为空
#     if request.method == 'POST':
#         # 处理 POST 请求的数据
#         input_text = request.form['inputText']
#         processed_text = ma.model_API(input_text)
#         raw_data = processed_text['choices'][0]['message']['content']

#         # 格式转换
#         data = []
#         for line in raw_data.strip().split('\n'):
#             if '|' in line:
#                 field, content = line.split('|', 1)
#                 data.append({"Field": field.strip(), "Content": content.strip()})

#         # 过滤表格中的"--"元素
#         filtered_data = [row for row in data if "---" not in row.values()]

#         # 将处理后的数据存储在 session 中
#         session['data'] = filtered_data

#         return redirect(url_for('index'))
#     else:
#         # 从 session 中获取数据
#         data = session.get('data', [])
#         return render_template('index.html', data=data)


# @app.route('/clear', methods=['POST'])
# def clear():
#     session.pop('data', None)  # 清除 session 中的数据
#     return redirect(url_for('index'))



# # @app.route('/process', methods=['POST'])
# # def process():

# #     input_text = request.form['inputText']

# #     print(input_text)
# #     processed_text = ma.model_API(input_text)

# #     raw_data = processed_text['choices'][0]['message']['content']

# #     # 格式转换
# #     data = []
# #     for line in raw_data.strip().split('\n'):
# #         if '|' in line:
# #             field = line.split('|')[1]
# #             content = line.split('|')[2]
# #             data.append({"Field": field.strip(), "Content": content.strip()})

# #     # 过滤表格中的"--"元素
# #     filtered_data = [row for row in data[1:] if "---" not in row.values()]

    
# #     return render_template('index.html', data = filtered_data)
# #     # # output = input_text.upper()  # 示例：将输入文本转换为大写
# #     # return render_template('index.html', output=output)

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=80, debug=True)