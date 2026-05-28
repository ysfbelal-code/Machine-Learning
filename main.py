import streamlit as st

st.set_page_config("Graphics Collision Detection + Hand Landmarks using CV2")
st.title("Graphics Collision Detection + Hand Landmarks using CV2 - by Youssef Belal", text_alignment="center")
st.markdown("""
Hi there! I'm Youssef Belal, and this is a little project I made that tests ball collision detection using the CV2 module and Mediapipe's Tasks 
API in Python. It detects your hand landmarks, and allows you to play around with a blue ball flying around your screen by slapping or hitting it. 
I had a lot of fun making it, and I hope you enjoy testing it :). 
            
I'm 14 years old, and have been learning Python for more than a year now. 
Although this project itself is impressive, I still wish to learn and improve beyond it. Anyways, here's what you need for this project:""")
with open("hand_landmarker.task", "rb") as task_file:
    st.download_button("Download hand_landmarker.task from Google AI for Developers (NECESSARY FOR THIS PROJECT)", data=task_file, file_name="hand_landmarker.task")
with open("physics_using_cv2.py") as code:
    st.code(code.read())

st.text("Output:")
st.video(r"output.mp4")
st.markdown("That's the project! Because of the new Tasks API that I mentioned earlier, " \
"all other websites for projects involving hand landmark "
"detection using mediapipe.solutions are all outdated. As far as I know, this is the only project in the web " \
"that uses the Tasks API for hand landmark detection.")

st.page_link("https://ai.google.dev/edge/mediapipe/solutions/tasks", label="To learn more about Mediapipe Tasks, click me...")
