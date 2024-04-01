import streamlit as st
from openai import OpenAI

client = OpenAI(api_key="my-api-key")

def get_completion(prompt, model="gpt-3.5-turbo"):
    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "Provide information about proper storage and average storage life (in days), as well as ways to maximize freshness for the foods listed:"},
                {"role": "user", "content": prompt},
            ],
        )
        return completion.choices[0].message.content
    except Exception as e:
        st.error(f"Failed to get completion from OpenAI: {e}")
        return ""

def display_food_info(response):
    food_info = response.strip().split('\n\n')
    for info in food_info:
        st.write(info)
        st.divider()


image_url = "https://static.vecteezy.com/system/resources/previews/003/235/639/non_2x/fridge-color-clipart-illustration-design-free-vector.jpg"  # Replace with your actual image source (URL or base64 string)


col1, col2 = st.columns([3, 1])
with col1:
    st.title("Food Lifespan and Proper Storage Information")

with col2:
    st.image(image_url, width=100) 

with st.form(key="food_input_form"):
    prompt = st.text_input("Enter food separated by commas (e.g., carrots, apples):", help="List the foods you want to know about, separated by commas.")
    submitted = st.form_submit_button("Submit")

if submitted and prompt:
    response = get_completion(prompt)
    if response:
        display_food_info(response)
    else:
        st.write("No data available or failed to fetch data.")


