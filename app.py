import streamlit as st
from huggingface_hub import InferenceClient
import os

client = InferenceClient(
    model="HuggingFaceH4/zephyr-7b-beta",
    token=os.environ.get("HF_TOKEN")
)

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

                response = client.chat_completion(
                    messages=messages,
                    max_tokens=300,
                    temperature=0.7
                )
                answer = response.choices[0].message.content
            except Exception as e:
                answer = f"حدث خطأ، حاولي مرة أخرى 🙏"

        st.write(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
