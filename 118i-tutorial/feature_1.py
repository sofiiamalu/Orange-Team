import os
import openai
import streamlit as st
from openai import OpenAI


st.markdown("# Page 1: Recipe Creation 🥑")
st.sidebar.markdown("# Page 1: Recipe Creation 🥑") 

openai.api_key = os.environ["OPENAI_API_KEY"]

client = OpenAI()


def get_completion(prompt, model="gpt-3.5-turbo"):
   completion = client.chat.completions.create(
        model=model,
        messages=[
        {"role":"system",
         "content": "You make recipes based on ingredients provided and create plans of those recipes catered towards adults."},
        {"role": "user",
         "content": prompt},
        ]
    )
   return completion.choices[0].message.content

# create our streamlit app
with st.form(key = "chat"):
    prompt = st.text_input("Enter ingreidents that you want to use: ") 
    
    submitted = st.form_submit_button("Submit")
    
    if submitted:
        st.write(get_completion(prompt))