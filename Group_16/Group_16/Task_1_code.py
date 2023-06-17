from time import sleep

import pandas as pd
import openai

openai.api_key = "your key" #api


class Chat: #The class implementation of idea four was unsuccessful
    def __init__(self, conversation_list=[]) -> None:
        # 初始化对话列表，可以加入一个key为system的字典，有助于形成更加个性化的回答
        # self.conversation_list = [{'role':'system','content':'你是一个非常友善的助手'}]
        self.conversation_list = []


    def ask(self, prompt):
        self.conversation_list.append({"role": "user", "content": prompt})
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=self.conversation_list)
        answer = response.choices[0].message['content']
        self.conversation_list.append({"role": "assistant", "content": answer})
        self.show_conversation(self.conversation_list)


def gpt_classification(data): #main handle function
    sleep(20)
    s1 = "請閱讀法規判斷該廣告違反哪一條法規。\n"
    #s1 = "請閱讀法規，根據之前訓練的分類模型判斷該廣告違反哪一條法規。\n"
    s2 = "法規: 第二十四條第一項 化粧品不得於報紙、刊物、傳單、廣播、幻燈片、電影、電視及其他傳播工具登載或宣播猥褻、有傷風化或虛偽誇大之廣告。 第二十四條第二項 化粧品之廠商登載或宣播廣告時，應於事前將所有文字、畫面或言詞，申請中央或直轄市衛生主管機關核准，並向傳播機構繳驗核准之證明文件。\n"
    #s2 = "法規: 第二十四條第一項 化粧品不得於報紙、刊物、傳單、廣播、幻燈片、電影、電視及其他傳播工具登載或宣播猥褻、有傷風化或虛偽誇大之廣告。 第二十四條第二項 化粧品之廠商登載或宣播廣告時，應於事前將所有文字、畫面或言詞，申請中央或直轄市衛生主管機關核准，並向傳播機構繳驗核准之證明文件。"
    s3 = "廣告: " + data + "\n"
    s4 = "回答形式僅限於0和1這兩個數位中的一個，其中0代表違反第二十四條第一項，1代表不違反第二十四條第一項"
    #s4 = "回答形式僅限於0和1這兩個數位中的一個，其中0代表違反第二十四條第一項，1代表違反第二十四條第而項"
    #s4 = "回答形式僅限於0和1這兩個數位中的一個，其中0代表不違反第二十四條第二項，1代表違反第二十四條第二項"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0.2,
        max_tokens=1000,
        messages=[
            {"role": "user", "content": s1 + s2 + s3 + s4}
        ]
    )
    raw_response = response['choices'][0]['message']['content']
    return int(raw_response)


def train_gpt(train_text): #The class implementation of idea four was unsuccessful
    i = 0
    for e in range(train_text.shape[0]):
        s = ""
        if i == 0:
            s += "現在需要你完成一個廣告法律違規的分類問題的模型，就是通過訓練數據將模型訓練好並應用在測試集上，得到最後的分類結果。 問題背景是我們輸入的廣告都存在違反法律的問題，但是目前有兩條法律，請你判斷其具體違反的是哪一條對應法規。\n"
        i += 1
        s1 = "以下是第"+str(i)+"條訓練數據\n"
        s2 = "法規: 第二十四條第一項 化粧品不得於報紙、刊物、傳單、廣播、幻燈片、電影、電視及其他傳播工具登載或宣播猥褻、有傷風化或虛偽誇大之廣告。 第二十四條第二項 化粧品之廠商登載或宣播廣告時，應於事前將所有文字、畫面或言詞，申請中央或直轄市衛生主管機關核准，並向傳播機構繳驗核准之證明文件。 第二十四條第三項 經中央或直轄市衛生主管機關依前項規定核准之化粧品廣告，自核發證明文件之日起算，其有效期間為一年，期滿仍需繼續廣告者，得申請原核准之衛生主管機關延長之，每次核准延長之期間不得逾一年；其在核准登載、宣播期間，發現內容或登載、宣播方式不當者，原核准機關得廢止或令其修正之。\n"
        s3 = "廣告: " + train_text['sentence'][e] + "\n"
        s4 = "請先進行分類判斷,回答形式僅限於0和1這兩個數位中的一個，其中0代表違反第二十四條第一項，1代表違反第二十四條第二項"
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            temperature=0.2,
            max_tokens=1000,
            messages=[
                {"role": "user", "content": s + s1 + s2 + s3 + s4}
            ]
        )
        raw_response = response['choices'][0]['message']['content']
        if int(raw_response) == int(train_text['label_for_kaggle'][e]):
            s6 = "針對本次訓練集數據的預測正確，請進一步保存模型"
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                temperature=0.2,
                max_tokens=1000,
                messages=[
                    {"role": "user", "content": s6}
                ]
            )
        else:
            s6 = "針對本次訓練集數據的預測錯誤，正確答案為"+str(int(train_text['label_for_kaggle'][e]))+"請根據測試提示和測試數據重新進行這一步的模型訓練並進一步保存模型"
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                temperature=0.2,
                max_tokens=1000,
                messages=[
                    {"role": "user", "content": s6}
                ]
            )



if __name__ == '__main__': #main function
    train_FileName = "COS_train.csv"
    test_FileName = "COS_test.csv"
    train_text = pd.read_csv(train_FileName, encoding='utf-8')
    test_text = pd.read_csv(test_FileName, encoding='utf-8')
    text_data = test_text['sentence']
    result = []
    #train_gpt(train_text)
    for i in range(text_data.shape[0]):
        print(gpt_classification(text_data[i]))
        result.append(gpt_classification(text_data[i]))
    df = pd.DataFrame({"source_id": test_text['source_id'],
                       "label_for_kaggle": result
                       })
    df.to_csv("submission.csv", index=False, encoding='utf-8')