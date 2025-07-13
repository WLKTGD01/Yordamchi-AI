import streamlit as st
import time
from mistralai import Mistral

# Suhbat tarixini saqlash
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mistral AI ni ishga tushurish
ai = Mistral(api_key="fXEf24hfVLvmIEHRvilwOKN6hPpSET7b")  # ← bu yerga o‘zingizning API kalitingizni yozing

st.title("Yordamchi AI")
st.markdown("_Sun'iy intellekt harfma-harf javob yozadi va suhbat tarixini saqlaydi._")

user_input = st.text_input("Sizning xabaringiz:", "")

# Harfma-harf yozish funksiyasi
def show_typing(text, delay=0.02):
    placeholder = st.empty()
    output = ""
    for char in text:
        output += char
        placeholder.markdown(output)
        time.sleep(delay)

# AI javobini olish va ko‘rsatish
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Mistral AI dan javob olish
    full_prompt = "\n".join([f"{msg['role']}: {msg['content']}" for msg in st.session_state.messages])
    try:
        response = ai.chat.complete(
            model="mistral-small",  # yoki boshqa model
            messages=[{"role": "system", "content": 'You get answer to question in Uzbek language.'},{"role": "user", "content": full_prompt}]
        )
        reply = response.choices[0].message.content
    except Exception as e:
        reply = f"❌ AI javob bera olmadi: {e}"

    st.session_state.messages.append({"role": "assistant", "content": reply})

    # Javobni harfma-harf ko‘rsatish
    show_typing(reply)

# Suhbat tarixini ko‘rsatish
st.divider()
st.subheader("🗂 Suhbat Tarixi")
for msg in st.session_state.messages:
    role = "👤 Siz" if msg["role"] == "user" else "🤖 AI"
    st.markdown(f"**{role}:** {msg['content']}", unsafe_allow_html=True)
