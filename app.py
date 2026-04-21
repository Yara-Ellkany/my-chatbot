import streamlit as st
from groq import Groq
import os

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

st.title("🤖 My Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("اكتبي سؤالك هنا..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("جاري التفكير..."):
            try:
                messages = [{"role": "system", "content": "You are a helpful assistant."}]
                for msg in st.session_state.messages:
                    messages.append({"role": msg["role"], "content": msg["content"]})

                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=messages,
                    max_tokens=500,
                    temperature=0.7
                )
                answer = response.choices[0].message.content
            except Exception as e:
                answer = f"خطأ: {str(e)}"

        st.write(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
