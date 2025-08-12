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
import time

#load_dotenv()

def translateE(source,model):
  response1 = client.chat.completions.create(
    #model="gpt-4o-2024-08-06",
    model=model,
    #temperature=0.8,
    messages=[
      {"role": "system",\
               "content":"あなたは日本語から英語に翻訳する翻訳家です"},
      {"role": "user",\
               "content": "「{0}」を英文にしてください。".format(source)}],
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "english",
            "schema": {
                "type": "object",
                "properties": {
                    "英文": {"type": "string"},
                },
                "required": ["英文"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    },
  )
  english_response = json.loads(response1.choices[0].message.content)
  return english_response['英文']

#
# APIキーは環境変数にセットしておく
#
client = OpenAI()

#

st.title("■ Let's study scikit-learn ■")
st.write("[powered by Konan digital-twin lab.]")

lang = st.radio(label='★言語選択 (language)',
                options=('Japanese', 'English'),
                index=0,
                horizontal=True,
)
if lang=="Japanese":
  language="日本語"
else:
  language="英語"

#model="gpt-4o-2024-08-06"
model = st.radio(label='★モデル選択 (model)',
                 options=('gpt-4o', 'gpt-4o-mini', 'gpt-4.1','gpt-5','o1','o1-mini','o3','o3-mini'),
                index=0,
                horizontal=True,
)
promptP = st.radio(label='★プロンプト',
                   options=('A','B','C','D','AE','BE','CE','DE'),
                   index=0,
                   horizontal=True,
)

prompt_texts={
  'A':"問題は4択問題とし、問題はPythonプログラムの一部を空欄にし、その内容を問うものである。",
  'B':"Pythonプログラムの一部を空欄にし、その内容を問う4択問題を作成する。",
  'C':"問題は4択問題とし、問題はPythonプログラムの一部を空欄にし、その内容を問うものである。ただし問題文にはPythonプログラムは含まない。",
  'D':"Pythonプログラムの一部を空欄にし、その内容を問う4択問題を作成する。ただし問題文にはPythonプログラムは含まない。",
  'AE':"The questions are four-choice questions, and the questions ask for the content of a Python program, leaving a portion of the program blank.",
  'BE':"Create a four-choice question that leaves part of a Python program blank and asks what to put in the blank.",
  'CE':"The question should be a four-choice question, and the question should show a Python program with a part of the program blank and ask what should be placed in the blank. However, the question text does not include the Python program.",
  'DE':"Create a four-choice question that leaves part of a Python program blank and asks what to put in the blank. However, do not include the Python program in the question text.",
}
st.write("Prompt:",prompt_texts[promptP])



#
# 問題作成の元になる文章群
#
explanationList=[
    "scikit-learnでLasso回帰を使う場合は、Lasso関数を用います。alphaオプションで正則化を制御します。fitメソッドとpredictメソッドが使われます。モデルはintercept_属性と、coef_属性にで示されます。",
    "scikit-learnでRidge回帰を使う場合は、Ridge関数を用います。alphaオプションで正則化を制御します。fitメソッドとpredictメソッドが使われます。モデルはintercept_属性と、coef_属性にで示されます。",
    "scikit-learnで線形回帰を使う場合は、LinearRegression関数を用います。fitメソッドとpredictメソッドが使われます。モデルはintercept_属性と、coef_属性にで示されます。"
]

probtypeList=[
    "関数の名前を問うようにしろ。",
    "属性について問うようにしろ。",
    "メソッドについて問うようにしろ。",
    "オプションの値の大小について問うようにしろ。",
    "オプションについて問うようにしろ。",
    "Numpyと組み合せるようにしろ。",
    "pandasと組み合せるようにしろ。"
]

quiz_response="NONE"
b=["","","",""]
ans=""
expl=""
  

if 'counter' not in st.session_state:
  st.session_state['counter'] = 0
if 'time' not in st.session_state:
  st.session_state['time'] = 0

counter=st.session_state['counter']

if st.button('問題 (quiz)',type="primary"):
  print("XXXX ",counter)


#
# 文章群から文章をランダムに選ぶ
#
  st.session_state['counter'] += 1

  explanation=explanationList[int(random.random()*len(explanationList))]
  probtype   =probtypeList[int(random.random()*len(probtypeList))]
  if language =='英語':
    explanation = translateE(explanation,model)
  
  prompt ="「{0}」の文章に関して、Pythonコードの一箇所を空欄にした穴埋め問題を考えます。".format(explanation)
  prompt+="さらに、問題は4択問題にします。"
  prompt+="問題のPythonコードと問題文と、4個の選択肢の文言とその答の番号を示せ。"
  prompt+="選択肢の文言は選択肢の番号は不要である。"
  prompt+="また、Pythonコードは改行をつけること。"
  prompt+="また、Pythonコードではデータの初期化をすること。"
  prompt+="「{0}」を守ること。".format(probtype)
  prompt+="正解の選択肢以外の選択肢の文言は間違っているようにすること。"
  prompt+="言語は{0}を用いること。".format(language)

# "「{0}」の文章に関して、Pythonの4択問題を考えます。問題にはPythonコードの一部を穴埋めする問題とします。問題のPythonコードと問題文と、4個の選択肢の文言とその答の番号を示せ。選択肢の文言は選択肢の番号は不要である。また、Pythonコードは改行をつけること。また、Pythonコードではデータの初期化をすること。「{1}」を守ること。正解の選択肢以外の選択肢の文言は間違っているようにすること。{2}で。".format(explanation,probtype,language)}],

  start_t=time.time()
  response1 = client.chat.completions.create(
    #model="gpt-4o-2024-08-06",
    model=model,
    #temperature=0.8,
    messages=[
      {"role": "system",\
               "content":"あなたは機械学習の専門家です。知っている知識を駆使して初心者向けの機械学習の学習のための問題を作ります。"},
      {"role": "user",\
               "content": prompt}],
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "quiz_data",
            "schema": {
                "type": "object",
                "properties": {
                    "問題文": {"type": "string"},
                    "Pythonコード": {"type": "string"},
                    "選択肢１": {"type": "string"},
                    "選択肢２": {"type": "string"},
                    "選択肢３": {"type": "string"},
                    "選択肢４": {"type": "string"},
                    "答え": {"type": "number"},
                },
                "required": ["問題文","Pythonコード","選択肢１", "選択肢２", "選択肢３", "選択肢４","答え"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    },
  )
  end_t=time.time()

  quiz_response = json.loads(response1.choices[0].message.content)
  st.session_state['quiz'] = quiz_response
  st.session_state['expl'] = explanation
  st.session_state['time'] = end_t-start_t

if 'quiz' in st.session_state:

  quiz_response=st.session_state['quiz']
  explanation=st.session_state['expl']
  time_e=st.session_state['time']
  msg=quiz_response
  prob=quiz_response["問題文"]
  code="{0}".format(quiz_response["Pythonコード"])

  b[0]="１：{0}".format(quiz_response["選択肢１"])
  b[1]="２：{0}".format(quiz_response["選択肢２"])
  b[2]="３：{0}".format(quiz_response["選択肢３"])
  b[3]="４：{0}".format(quiz_response["選択肢４"])
  ans ="答えは{0}です。".format(quiz_response["答え"])
  expl="  [ {0} ]".format(explanation)

  counter=st.session_state['counter']
  msg="-------------------------------count={0},{1:.2f} sec.".format(counter,time_e)
  st.write(msg)
  msg=prob
  st.write(msg)
  msg=code
  st.code(msg)
  msg="次の選択肢から正しいものを選べ (Choose the correct one)"
  st.write(msg)
  for i in range(4):
    st.write(b[i])
  msg="-----------------------------------------------------"
  st.write(msg)
  st.session_state['counter'] += 1


answer= st.radio(
    "答えは？ (What is your answer ?)",
    ["１", "２", "３", "４"],
    horizontal=True,
    index=None,
)

if st.button('解答 (answer)',type="primary"):
  try:
    if 'total_prob' not in st.session_state:
      st.session_state['total_prob']=0
    if 'total_correct' not in st.session_state:
      st.session_state['total_correct']=0

    quiz_response=st.session_state['quiz']
    explanation=st.session_state['expl']
  
    st.session_state['total_prob']+=1
    
    if int(answer)==int(quiz_response["答え"]):
      st.write("正解でした (correct)")
      st.session_state['total_correct']+=1
    else:
      st.write("間違いでした (incorrect)")
    st.write("--------------")

    ratio=100.0*int(st.session_state['total_correct'])/int(st.session_state['total_prob'])
    #ratio=10.0
    b[0]="１：{0}".format(quiz_response["選択肢１"])
    b[1]="２：{0}".format(quiz_response["選択肢２"])
    b[2]="３：{0}".format(quiz_response["選択肢３"])
    b[3]="４：{0}".format(quiz_response["選択肢４"])
    ans ="答えは{0}です (The answer is {0}) [score={1:0.2f}％ ({2}/{3})]".format(quiz_response["答え"],ratio,st.session_state['total_correct'],st.session_state['total_prob'])
    expl="  [ {0} ]".format(explanation)
    st.write(ans)
    st.write(expl)
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




