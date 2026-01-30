import streamlit as st
import pandas as pd
import random

# ページの基本設定
st.set_page_config(page_title="アランナラ検定", page_icon="🍀")

# データの読み込み
@st.cache_data
def load_data():
    # 前の工程で作ったdata.csvを読み込む
    return pd.read_csv('data.csv')

df = load_data()

# セッション状態（クイズの進行管理）の初期化
if 'quiz_started' not in st.session_state:
    st.session_state.quiz_started = False
if 'current_target' not in st.session_state:
    st.session_state.current_target = None
if 'options' not in st.session_state:
    st.session_state.options = []
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'total_answered' not in st.session_state:
    st.session_state.total_answered = 0

def next_question():
    # ランダムに1体選択
    target = df.sample().iloc[0]
    st.session_state.current_target = target
    
    # 選択肢を作成（正解1つ + 不正解3つ）
    wrong_answers = df[df['名前'] != target['名前']]['名前'].sample(3).tolist()
    options = wrong_answers + [target['名前']]
    random.shuffle(options)
    st.session_state.options = options
    st.session_state.answered = False

# メインUI
st.title("🍀 原神 アランナラ当てクイズ")

if not st.session_state.quiz_started:
    st.write("アランナラたちの名前をどれくらい覚えていますか？")
    if st.button("クイズを始める"):
        st.session_state.quiz_started = True
        st.session_state.score = 0
        st.session_state.total_answered = 0
        next_question()
        st.rerun()

else:
    target = st.session_state.current_target
    
    st.write(f"第 {st.session_state.total_answered + 1} 問")
    st.image(target['画像URL'], width=400)
    
    # クイズフォーム
    with st.form(key='quiz_form'):
        answer = st.radio("このアランナラの名前は？", st.session_state.options)
        submit = st.form_submit_button("決定")
    
    if submit:
        st.session_state.total_answered += 1
        if answer == target['名前']:
            st.success(f"⭕ 正解！ 彼は **{target['名前']}** です。")
            st.session_state.score += 1
            st.balloons()
        else:
            st.error(f"❌ 残念！ 正解は **{target['名前']}** でした。")
        
        st.info(f"解説: {target['説明']}")
        
        if st.button("次の問題へ"):
            next_question()
            st.rerun()

    # スコア表示
    st.sidebar.write(f"現在のスコア: {st.session_state.score} / {st.session_state.total_answered}")
    if st.sidebar.button("クイズを終了する"):
        st.session_state.quiz_started = False
        st.rerun()
