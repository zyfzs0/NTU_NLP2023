import re
import json
import argparse

def extract_quotes(text):
    pattern = r'"([^"]*)"'
    matches = re.findall(pattern, text)
    return matches

def extract_parentheses(text):
    pattern = r'（([^）]*)）'
    matches = re.findall(pattern, text)
    return matches

def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content

def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def write_json_file(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Description of your program')
    parser.add_argument('--txt_path', help='the path of gpt response .txt file')
    parser.add_argument('--json_path', help='the path of ad content .json file')
    args = parser.parse_args()


    gptRes = read_text_file(args.txt_path)
    # print(gptRes)

    texts = extract_quotes(gptRes)
    # print(texts)

    labels = extract_parentheses(gptRes)
    # print(labels)

    if 'COS' in args.txt_path:
        mapping = {'第一項法規' : '第十條第一項法規', '第二項法規' : '第十條第二項法規'}
    elif 'FOOD' in args.txt_path:
        mapping = {'第一項法規' : '第二十八條第一項法規', '第二項法規' : '第二十八條第二項法規'}
    elif 'MED' in args.txt_path:
        mapping = {'第一項法規' : '第六十七條法規', '第二項法規' : '第六十八條法規'}

    results = []
    for i in range(len(texts)):
        result = {
            "text": texts[i],
            "label": mapping[labels[i]]
        }
        results.append(result)
    
    json_data = read_json_file(args.json_path)
    json_data["violation_segment"] = results
    write_json_file(json_data, args.json_path)

    print(json_data)
