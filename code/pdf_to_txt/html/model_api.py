import dashscope
from http import HTTPStatus

dashscope.api_key="sk-8cdbec7b7486475aaa52bb8d8b37d22c"

def model_API(input_text):
    print("---------------------------------------------------模型开始运行-----------------------------------------------------")
    prompt = """ Please extract field information from the above paper content, requiring:
    1. You are an academic expert in petrochemicals;
    2. If there is no relevant information about the field in the text, fill in/for that field;
    3. If relevant information about a field appears in the text, you don't need to summarize it. You can simply extract the four sentences above and below the text where the field is located;
    4. Require to display in a table format, with two columns, one for the field and the other for the original content;
    5. The extracted information is the original content rather than the summary;
    6. The fields to be extracted include:

        Journal Ref
        DOI
        Corresponding author
        Corresponding author's affiliation
        Title	
        Polymer type and information
        Orientation
        Crystallinity
        chain structure
        Filler information
        Filler content
        Filler treatment
        Filler orientation
        Sample preparation method
        An instrument or method for testing thermal conductivity
        Thermal conductivity
    """


    messages = [{'role': 'system', 'content': 'You are an academic expert in petrochemicals.'},
                {'role': 'user', 'content': input_text + prompt}]

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