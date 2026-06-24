import streamlit as st
import json
import os
def CreateSession():
    if CheckKey():
        session_data = {
            "name": st.session_state.name,
            "nature": st.session_state.nature,
            "mymessages": st.session_state.mymessages,
            "Dialog_name": st.session_state.Dialog_name
        }
        st.success(os.path.join(tempfile.gettempdir(), f"{st.session_state.Dialog_name}.json"))
        with open(os.path.join(tempfile.gettempdir(), f"{st.session_state.Dialog_name}.json"), "w", encoding="utf-8") as f:
            json.dump(session_data, f, ensure_ascii=False, indent=2)

def CheckKey():
    for key in st.session_state.keys():
        if key=="Dialog_name":
            return True
    return False

def LoadSessionPath():
    PathName=st.session_state["Dialog_name"]
    old_Session_list=[]
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"SessionPath.json"),"r",encoding="utf-8") as fp:
        old_Session_list = json.load(fp)
        for i in old_Session_list:
            if st.session_state.Dialog_name==i:
                return
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"SessionPath.json"), "w", encoding="utf-8") as fp:
        AllSession_list=[*old_Session_list,PathName]
        json.dump(AllSession_list, fp,ensure_ascii=False,indent=2)

def LoadSession(SessionName):
    if os.path.exists(os.path.join(tempfile.gettempdir(), f"{SessionName}.json")):
        ClearSessionState()
        with open(os.path.join(tempfile.gettempdir(), f"{SessionName}.json"),"r",encoding="utf-8") as fp:
            session_data=json.load(fp)
            st.session_state.mymessages=session_data["mymessages"]
            st.session_state.name=session_data["name"]
            st.session_state.nature=session_data["nature"]
            st.session_state.Dialog_name=session_data["Dialog_name"]

def ClearSessionState():
    for key in st.session_state.keys():
        del st.session_state[key]

def ceshi():
    st.success("来过")
