import gtts.lang as lang
import streamlit as st
import openai
from gtts import gTTS  # new import
from io import BytesIO  # new import

openai.api_key = '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'

messages=[
    {"role": "system", "content": "You are a helpful assistant."},
]

langs = lang.tts_langs()

st.markdown("<h1 style='text-align: center; color: blue;'>챗봇 만들기(음성지원)</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: blue;'>프롬프트를 입력하고 언어를 선택하세요. </h3>", unsafe_allow_html=True)

def get_key(val):
    for key, value in langs.items():
        if val == value:
            return key

def text_to_speech(text, lang):
    """
    Converts text to an audio file using gTTS and
    returns the audio file as binary data
    """
    audio_bytes = BytesIO()
    tts = gTTS(text=text, lang=get_key(lang))
    tts.write_to_fp(audio_bytes)
    audio_bytes.seek(0)
    return audio_bytes.read()

def chatbot():
    global messages

    user_input = st.text_input("Enter a prompt: ")
    user_lang = st.selectbox('음성 언어', options=langs.values())
    if user_input:
        messages.append({"role": "user", "content": user_input})
    searchbutton = st.button("Search")
    if searchbutton:
        response = openai.ChatCompletion.create(
            model = 'gpt-4', # gpt-3.5-turbo
            messages = messages
        )
        system_response=response["choices"][0]["message"]["content"]
        messages.append({"role": "system", "content": system_response})

        for message in messages:
            st.write(message["content"])
        st.audio(text_to_speech(system_response, user_lang), format="audio/wav")


chatbot()