from flask import Flask, render_template, request, jsonify
import model_api as ma

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    input_text = request.form['inputText']
    processed_text = ma.model_API(input_text)
    raw_data = processed_text['choices'][0]['message']['content']

    # 格式转换
    data = []
    for line in raw_data.strip().split('\n')[1:]:
        if '|' in line:
            print(line)
            field = line.split('|')[1]
            content = line.split('|')[2]
            # field, content = line.split('|', 1)
            data.append({"Field": field.strip(), "Content": content.strip()})

    # 过滤表格中的"--"元素
    filtered_data = [row for row in data if "---" not in row.values()]

    return jsonify(filtered_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)