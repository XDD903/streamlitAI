import streamlit as st
from openai import OpenAI
import Fun
import json
import os
import tempfile
st.set_page_config(
    page_title="AI蠢货伴侣",
    page_icon="pai.png",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.write("当前工作目录:", os.getcwd())
st.write("主脚本路径:", __file__)
st.write("临时目录",tempfile.gettempdir())

st.title("我叫AI，我很强！")
st.sidebar.subheader("控制面包")
if st.sidebar.button("新建对话",width=200):
    Fun.CreateSession()#按下创建对话后，创建了对话文件，之后清空session_state，下面1号块显示对话就为空
    Fun.ClearSessionState()#创建新对话后，要清除原本session_state内的缓存，留给新对话用
st.sidebar.write("历史对话")
st.success(os.path.join(os.path.dirname(os.path.abspath(__file__)),"SessionPath.json"))
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"SessionPath.json"),"r",encoding="utf-8") as fp:
    Session_list=json.load(fp)
    for i in Session_list:
        if st.sidebar.button(i,width=175):
            Fun.LoadSession(i)

name:str=st.sidebar.text_input("名？",placeholder="我已急哭")
nature:str=st.sidebar.text_area("性？")

client = OpenAI(
    api_key="sk-2289471daa3747119dae65b42094e798",
    base_url="https://api.deepseek.com")

if "mymessages" not in st.session_state:
    st.session_state["mymessages"]=[]
st.session_state.name=name
st.session_state.nature=nature

for message in st.session_state.mymessages:#1号：显示人机对话
    if message["role"]=="user":
        st.chat_message("user").write(message["content"])
    else:
        st.chat_message("system").write(message["content"])

AI_what = "你叫%s，你的性格是%s。若没有指定名字或者性格，则不要提及。"
shu=st.chat_input("吧唧吧唧吧唧吧唧")
if shu:
    st.session_state.mymessages.append({"role": "user", "content": shu})
    st.chat_message("user").write(shu)
    if "Dialog_name" not in st.session_state:
        if len(shu)>8:
            st.session_state.Dialog_name=str(shu[:8])+"..."
        else:
            st.session_state.Dialog_name=shu
    response = client.chat.completions.create(
        model="deepseek-v4-pro",
        messages=[
            {"role": "system", "content": AI_what % (st.session_state.name,st.session_state.nature)},
            *st.session_state.mymessages
        ],
        stream=True,
        reasoning_effort="high",
        extra_body={"thinking": {"type": "enabled"}}
    )
    All_response=""
    zhanwei=st.empty()
    for data in response:
        if data.choices[0].delta.content is not None:
            All_response+=data.choices[0].delta.content
        zhanwei.write(All_response)
    st.session_state.mymessages.append({"role": "system", "content": All_response})
    Fun.CreateSession()#发送了消息，马上创建好对话文件
    Fun.LoadSessionPath()
    st.rerun()
#st.write(st.session_state) 查看session_state内容


