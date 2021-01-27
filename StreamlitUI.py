import streamlit as st
from ImageCollectorClass import ImageGrabber
import pandas as pd
from PIL import Image
import glob
import base64

st.set_page_config('Pinterest Bot')
title_col1, title_col2, title_col3, title_col4, title_col5, title_col6 = st.beta_columns((1.1, 3, 1, 1, 1, 1))
title_col1.image('Images/logo1.png', width=100)
title_col2.title("interest Bot")

search_img = st.empty()
total_img = st.empty()
search_flag = False


st.sidebar.subheader('Search Image')
search_img = st.sidebar.text_input("e.g., 'cats'")
st.sidebar.subheader('Total Image')
total_img = st.sidebar.text_input("e.g., 10")

col1, col2 = st.beta_columns((0.9, 0.1))
with col1:
    progress = st.sidebar.progress(0)
with col2:
    score = st.sidebar.empty()
    #score.text("")

success = st.sidebar.empty()
success.text("")
side_col1, side_col2, side_col3 = st.sidebar.beta_columns(3)

with side_col1:
    search_btn = st.button("Search")
with side_col2:
    reset_btn = st.button("Reset")

st.sidebar.markdown('''<h3>Created By: Ameer Tamoor Khan</h3>
                    <h4>Github : <a href="https://github.com/AmeerTamoorKhan" target="_blank">Click Here </a></h4> 
                    <h4>Email: drop-in@atkhan.info</h4> ''', unsafe_allow_html=True)

def default():
    st.header('Working Demonstration:')
    st.video('Images/final.mp4')
    st.header('How is Works:')
    st.markdown('''
            <p>Pinterest is known as an Image hub, where quality images are available on almost everything in abundance. 
            So to avoid the tireless effort of saving images one by one, the ”Pinterest Bot” will crawl and collect images for
            us along with captions and will save them on our PC.</p>
            <p>This project is mainly developed to collect images for machine learning, where we need thousands of images of the
            same kind to train our model. The application is self-explanatory, as it takes two parameters, Image that we want 
            to search and total images. On the right-hand side, it will show all the images we collected and at bottom all 
            images with there name and caption are placed in a pandas dataframe.</p>
            <p>Scraping is a process of extracting information from the web. Big Data plays an important role in Machine 
            learning. And it happens that you are in search of particular data, which is not easily available, then scraping 
            comes into play.</p>
            <h3><strong>#scraping</strong>  <strong>#selenium</strong>  <strong>#python</strong>  
            <strong>#machinelearning</strong></h3>
            ''', unsafe_allow_html=True)


if search_btn:
    total_img = int(total_img)
    bot = ImageGrabber(search_img, total_img, search_img, progress, score)
    st.balloons()
    success.success('Done')
    search_flag = True
elif reset_btn:
    st.empty()
    default()
else:
    default()

if search_flag:
    df = pd.read_csv(f'{search_img}/{search_img}.csv')
    st.header("Collected Images")
    cols_img = st.beta_columns(4)
    for i in range(0, len(df), 4):
        temp = len(df)-i
        if temp > 4:
            count = 4
        else:
            count = temp
        for j in range(count):
            cols_img[j].image(f"{search_img}/{df['Image Name'].loc[i+j]}")
            img = open(f"{search_img}/{df['Image Name'].loc[i+j]}", 'rb')
            b64 = base64.b64encode(img.read()).decode()
            cols_img[j].markdown(f'''<a href="data:file/{search_img}{i+j};base64,{b64}">{search_img}{i+j} </a>''', unsafe_allow_html=True)
    st.header("Images Name And Captions")
    st.table(df)
    data = open(f"{search_img}/{search_img}.csv", 'rb')
    b64 = base64.b64encode(data.read()).decode()
    st.markdown(f'''<a href="data:file/csv;base64,{b64}">{search_img}.csv</a>''', unsafe_allow_html=True)



