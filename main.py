import streamlit as st

st.set_page_config("Graphics Collision using CV2 in Python")
st.title("Graphics Collision using CV2 - by Youssef Belal", text_alignment="center")

with open("physics_using_cv2.py") as code:
    st.code(code.read())

st.markdown("That's the project! Because of the new Tasks API that I mentioned earlier, " \
"all other websites for projects involving hand landmark "
"detection using mediapipe.solutions are all outdated. As far as I know, this is the only project in the web " \
"that uses the Tasks API for hand landmark detection.")