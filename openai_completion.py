import openai
import streamlit as st

openai.api_key = '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'

# This function uses the OpenAI Completion API to generate a
# response based on the given prompt. The temperature parameter controls
# the randomness of the generated response. A higher temperature will result
# in more random responses,
# while a lower temperature will result in more predictable responses.


def generate_response(prompt):
    completions = openai.Completion.create (
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        n=3,
        stop=None,
        temperature=0.8,
    )

    message = completions.choices[0].text
    return message

st.title("AI Assistant : openAI + Streamlit")

prompt = st.text_input("Enter your message:", key='prompt')
if st.button("Submit", key='submit'):
    response = generate_response(prompt)
    st.success(response)

