import os
import pandas as pd
import tensorflow as tf
from keras.layers import TextVectorization
import streamlit as st

import re

def clean_text(text):
    # Chuyển về dạng str nếu không phải
    if not isinstance(text, str):
        text = str(text)
    # chuyển về dạng chữ thường
    text = text.lower()
    # xoá URL
    text = re.sub(r"http\S+|www\S+|https\S+", "", text, flags=re.MULTILINE)
    # xoá emoji
    text = text.encode('ascii', 'ignore').decode('ascii')
    # xoá các ký tự đặc biệt ngoại trừ chữ và số
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)
    # xoá số
    text = re.sub(r'\d+', '', text)
    # xoá nhiều khoảng trắng liền kề nhau
    text = re.sub(r'\s+', ' ', text).strip()
    return text

@st.cache_resource(show_spinner=False)
def load_data_and_model():
    # Load data để adapt vectorizer (chỉ cần sample nhỏ)
    train_path = os.path.join('data', 'train', 'train.csv')
    if os.path.exists(train_path):
        # Chỉ đọc một phần nhỏ để adapt vectorizer (tối ưu cho Streamlit Cloud)
        df = pd.read_csv(train_path, nrows=10000)  # Chỉ đọc 10000 dòng đầu
    else:
        # Fallback: sử dụng test data nếu không có train data
        test_path = os.path.join('data', 'test', 'test_demo.csv')
        if os.path.exists(test_path):
            df = pd.read_csv(test_path)
        else:
            st.error("Không tìm thấy file dữ liệu để adapt vectorizer!")
            st.stop()
    
    df['comment_text'] = df['comment_text'].apply(clean_text)
    X = df['comment_text']
    
    vectorizer = TextVectorization(
        max_tokens=200000,  
        output_sequence_length=231,  
        output_mode='int'
    )
    vectorizer.adapt(X.values)
    
    # Load model
    model_path = 'toxic_comment_model.h5'
    if not os.path.exists(model_path):
        st.error(f"Không tìm thấy file mô hình: {model_path}")
        st.stop()
    
    model = tf.keras.models.load_model(model_path, compile=False)
    return vectorizer, model

# Load model và vectorizer khi khởi động app
try:
    vectorizer, model = load_data_and_model()
except Exception as e:
    st.error(f"Lỗi khi tải mô hình hoặc dữ liệu: {str(e)}")
    st.stop()

def limit_text(text):
    return text[:20]

def score_comment(comment):
    comment = clean_text(comment)
    input_text = vectorizer([comment])
    input_text = input_text.numpy()
    prediction = model.predict(input_text, verbose=0)
    toxic_list = []
    for idx, col in enumerate(['toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate']):
        if prediction[0][idx] > 0.5:
            toxic_list.append(col)
    return toxic_list

st.title('Toxic Comment Detection')
col1, col2 = st.columns(2)
# Use session state to track which button is active (for toggling)
if 'active_button' not in st.session_state:
    st.session_state.active_button = 'enter_comment'  # Default active button

with col1:
    enter_comment = st.button(
        'Enter comment',
        type='secondary' if st.session_state.active_button != 'enter_comment' else 'primary',
        on_click=lambda: st.session_state.update(active_button='enter_comment')
    )
with col2:
    insert_from_file = st.button(
        'Insert from file',
        type='secondary' if st.session_state.active_button != 'insert_from_file' else 'primary',
        on_click=lambda: st.session_state.update(active_button='insert_from_file')
    )
if st.session_state.active_button != '':
        if st.session_state.active_button == 'enter_comment':
            with st.form('my_form'):
                comment = st.text_area('Enter your comment:')
                submit_button = st.form_submit_button('Submit')
                if submit_button:
                    if comment:
                        toxic_categories = score_comment(comment)
                        if len(toxic_categories) == 0:
                            st.success('The comment is not toxic!', icon='👍')
                        else:
                            st.error(f'The comment is toxic! Types of toxicity: {", ".join(toxic_categories)}', icon='👎')
        elif st.session_state.active_button == 'insert_from_file':
            with st.form('my_form'):
                file = st.file_uploader('Upload a file:', type=['csv'])
                submit_button = st.form_submit_button('Submit')
                if submit_button:
                    if file:
                        df_file = pd.read_csv(file)
                        comments = df_file['comment_text']
                        df_toxic = []
                        df_non_toxic = []
                        for comment in comments:
                            toxic_categories = score_comment(comment)
                            if len(toxic_categories) != 0:
                                st.error(f'{comment}\n is toxic! Types of toxicity: {", ".join(toxic_categories)}', icon='👎')
                                df_toxic.append({'comment_text': comment, 'toxic_categories': toxic_categories})
                            else:
                                st.success(f'{comment}\n is not toxic!', icon='👍')
                                df_non_toxic.append({'comment_text': comment})
                        df_toxic = pd.DataFrame(df_toxic)
                        df_non_toxic = pd.DataFrame(df_non_toxic)
                        df_toxic.to_csv('toxic_comments.csv', index=False)
                        df_non_toxic.to_csv('non_toxic_comments.csv', index=False)