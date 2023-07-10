import streamlit as st
import os, uuid, json, PyPDF2
import numpy as np
from openai.embeddings_utils import get_embedding, cosine_similarity
import openai

openai.api_key = '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'

# 학습 데이터 저장 경로
json_file_path = 'my_knowledgebase.json'

def learn_pdf(file_path):
    content_chunks = []
    pdf_file = open(file_path, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    for page in pdf_reader.pages:
        content = page.extract_text()
        obj = {
            "id": str(uuid.uuid4()),
            "text": content,
            "embedding": get_embedding(content, engine='text-embedding-ada-002')
        }
        content_chunks.append(obj)

    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for i in content_chunks:
        data.append(i)
    with open(json_file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    pdf_file.close()


def answer_from_documents(user_query):
    user_query_vector = get_embedding(user_query, engine='text-embedding-ada-002')
    with open('my_knowledgebase.json', 'r', encoding="utf-8") as jsonfile:
        data = json.load(jsonfile)
        for item in data:
            item['embeddings'] = np.array(item['embedding'])

        for item in data:
            item['similarities'] = cosine_similarity(item['embedding'], user_query_vector)
        sorted_data = sorted(data, key=lambda x: x['similarities'], reverse=True)

        context = ''
        for item in sorted_data[:2]:
            context += item['text']

        myMessages = [
            {"role": "system", "content": "너는 훌륭한 보조야."},
            {"role": "user",
             "content": "맥락:\n{}\n\n "
                        "주어진 맥락에 기반해서 답변을 해.\n\n"
                        "query: {}".format(context, user_query)}
        ]
        response = openai.ChatCompletion.create(
            model='gpt-4',
            messages=myMessages,
            max_tokens=2048,

        )

    return response['choices'][0]['message']['content']


def save_uploaded_file(uploaded_file):
    with open(uploaded_file.name, "wb") as f:
        f.write(uploaded_file.getbuffer())



st.title("PDF + ChatGPT ")

uploaded_file = st.file_uploader("Choose a PDF file to upload", type="pdf")
if uploaded_file is not None:
    if st.button("Read PDF"):
        save_uploaded_file(uploaded_file)
        st.write("Please wait while we learn the PDF.")
        learn_pdf(uploaded_file.name)
        st.write("PDF reading completed! Now you may ask a question")
        os.remove(uploaded_file.name)
user_input = st.text_input("Enter your Query:")

if st.button("Send"):
    st.write("You:", user_input)
    response = answer_from_documents(user_input)
    st.write("Bot: "+response)

