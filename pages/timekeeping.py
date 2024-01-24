import streamlit as st
import pygame
import time

import vlc

def count_down(ts):
    with st.empty():
        while ts:
            mins, secs = divmod(ts, 60)
            time_now = '{:02d}:{:02d}'.format(mins, secs)
            st.header(f"{time_now}")
            time.sleep(1)
            ts -= 1
    st.write("Copyright: Twan Bakker - Ziltoid The Omniscient")
    st.balloons()
    
    pygame.mixer.init()
    pygame.mixer.music.load('./media/jingle.mp3')
    pygame.mixer.music.play()
    print("Audio will play for 4 seconds")
    time.sleep(4)
    pygame.mixer.music.stop()
    

st.title("Timer for speedback session")
time_minutes = st.number_input('Enter the time in minutes ', min_value=1, value=5)
time_in_seconds = time_minutes * 60
if st.button("START"):
    count_down(int(time_in_seconds))