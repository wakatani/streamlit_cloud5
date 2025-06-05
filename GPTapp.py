#   
#
#
from math import exp
import json
from openai import OpenAI
import os
import random
import copy
import streamlit as st

#load_dotenv()

#
# APIキーは環境変数にセットしておく
#
client = OpenAI()

#

st.title("■ Let's study scikit-learn ■")

lang = st.radio(label='言語選択 (language)',
                 options=('Japanese', 'English'),
                 index=0,
                 horizontal=True,
)
if lang=="Japanese":
  language="日本語"
else:
  language="英語"
#
# 問題作成の元になる文章群
#
explanationList=[
    "東灘区にある阪神電鉄の駅は、深江、青木、魚崎、住吉、御影、石屋川です",
    "東灘区にある阪急電鉄の駅は、岡本、御影です",
    "コンパイラのフロントエンド部分には字句解析と構文解析が含まれます",
    "C言語はコンパイラ言語ですが、Python言語はインタプリタ言語です",
    "BNFで文法を表現する場合、終端記号と非終端記号が使われる",
    "LLパーザを用いた構文解析が利用できる文法は左再帰を含みません",
    "コンパイラ言語は高速ですが、インタプリタ言語は遅いです"
]

quiz_response="NONE"
b=["","","",""]
ans=""
expl=""

if 'counter' not in st.session_state:
  st.session_state['counter'] = 0

counter=st.session_state['counter']

if st.button('問題 (quiz)'):
  print("XXXX ",counter)
#
# 文章群から文章をランダムに選ぶ
#
  explanation=explanationList[int(random.random()*len(explanationList))]

  response1 = client.chat.completions.create(
    model="gpt-4o-2024-08-06",
    temperature=0.8,
    messages=[
      {"role": "system",\
               "content":"あなたはクイズ出題者です。知っている知識を駆使して問題を作ります。"},
      {"role": "user",\
               "content": "「{0}」の文章に関する4択問題の4個の選択肢の文言とその答の番号を示せ。選択肢の文言は選択肢の番号は不要である。正解の選択肢以外の選択肢の文言は間違っているようにすること。正解の選択肢の番号はランダムにすること。言語は{1}で。".format(explanation,language)}],
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "quiz_data",
            "schema": {
                "type": "object",
                "properties": {
                    "選択肢１": {"type": "string"},
                    "選択肢２": {"type": "string"},
                    "選択肢３": {"type": "string"},
                    "選択肢４": {"type": "string"},
                    "答え": {"type": "number"},
                },
                "required": ["選択肢１", "選択肢２", "選択肢３", "選択肢４","答え"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    },
  )

  quiz_response = json.loads(response1.choices[0].message.content)
  st.session_state['quiz'] = quiz_response
  st.session_state['expl'] = explanation

if 'quiz' in st.session_state:
  quiz_response=st.session_state['quiz']
  explanation=st.session_state['expl'] 
  msg=quiz_response
  b[0]="１：{0}".format(quiz_response["選択肢１"])
  b[1]="２：{0}".format(quiz_response["選択肢２"])
  b[2]="３：{0}".format(quiz_response["選択肢３"])
  b[3]="４：{0}".format(quiz_response["選択肢４"])
  ans ="答えは{0}です。".format(quiz_response["答え"])
  expl="  [ {0} ]".format(explanation)

  counter=st.session_state['counter']
  msg="-----------------------------------------------------{0}".format(counter)
  st.write(msg)
  msg="正しいものを選べ (choose the correct answer)"
  st.write(msg)
  for i in range(4):
    st.write(b[i])
  msg="-----------------------------------------------------"
  st.write(msg)

  st.session_state['counter'] += 1


def ANS():
  try:
    quiz_response=st.session_state['quiz']
    explanation=st.session_state['expl']

    st.write("Your answer is ",int(answer))
    st.write("Real answer is ",int(quiz_response["答え"]))
                 
  
    if int(answer)==int(quiz_response["答え"]):
      st.write("正解でした")
    else:
      st.write("間違いでした")
    st.write("--------------")

    b[0]="１：{0}".format(quiz_response["選択肢１"])
    b[1]="２：{0}".format(quiz_response["選択肢２"])
    b[2]="３：{0}".format(quiz_response["選択肢３"])
    b[3]="４：{0}".format(quiz_response["選択肢４"])
    ans ="答えは{0}です。".format(quiz_response["答え"])
    expl="  [ {0} ]".format(explanation)
    st.write(ans,expl)
    counter=st.session_state['counter']
#    msg="-----------------------------------------------------{0}".format(counter)
#    st.write(msg)
#    for i in range(4):
#      st.write(b[i])
#    msg="-----------------------------------------------------"
#    st.write(msg)
    msg="◇◇◇ 次の問題は「問題」を押してください"
    st.write(msg)

    st.session_state['counter'] += 1
    
  except:
    st.write('まず「問題」を押してください')

answer= st.radio(
    "答えは？ (What is your answer ?)",
    ["１", "２", "３", "４"],
    horizontal=True,
    index=None,
)

if st.button('解答 (answer)'):
  try:
    quiz_response=st.session_state['quiz']
    explanation=st.session_state['expl']
  
    if int(answer)==int(quiz_response["答え"]):
      st.write("正解でした (correct)")
    else:
      st.write("間違いでした (incorrect)")
    st.write("--------------")
      
    b[0]="１：{0}".format(quiz_response["選択肢１"])
    b[1]="２：{0}".format(quiz_response["選択肢２"])
    b[2]="３：{0}".format(quiz_response["選択肢３"])
    b[3]="４：{0}".format(quiz_response["選択肢４"])
    ans ="答えは{0}です。".format(quiz_response["答え"])
    expl="  [ {0} ]".format(explanation)
    st.write(ans,expl)
    counter=st.session_state['counter']
#    msg="-----------------------------------------------------"
#    st.write(msg)
#    for i in range(4):
#      st.write(b[i])
#    msg="-----------------------------------------------------"
#    st.write(msg)
    msg="◇◇◇ 次の問題は「問題」を押してください (Click quiz, again)"
    st.write(msg)

  except:
      st.write('まず「問題」を押してください')




