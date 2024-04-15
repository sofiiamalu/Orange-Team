import streamlit as st
import fitz  
from openai import OpenAI

client = OpenAI(api_key="api-key-here")

def get_completion(food_item, model="gpt-3.5-turbo"):
    prompt = (
        f"Provide detailed information about proper storage and average storage life for {food_item}. "
        "Include ways to maximize freshness. Identify foods that are considered 'high-risk' for bacteria growth by labeling them with '⚠️ High-Risk Food Alert!'. Break each section up to clearly and easily read the infomration."
    )
    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": food_item},
            ],
        )
        return completion.choices[0].message.content
    except Exception as e:
        st.error(f"Failed to get completion from OpenAI: {e}")
        return ""

def preprocess_pdf_data(pdf_path):
    doc = fitz.open(pdf_path)
    storage_info = {}
    relevant_sections = [
        "storing food in the fridge",
        "freezing food safely",
        "storing cooked food safely"
    ]
    current_section = ''
    capture = False

    for page in doc:
        text_blocks = page.get_text("blocks")
        for block in text_blocks:
            text = block[4].strip()  # Get the text component from the block
            lower_text = text.lower()
            
            if any(section in lower_text for section in relevant_sections):
                current_section = text
                capture = True
                storage_info[current_section] = ''
            elif "avoid refreezing thawed food" in lower_text:
                capture = False
            
            if capture and current_section:
                storage_info[current_section] += ' ' + text

    return storage_info
    
pdf_data = preprocess_pdf_data(r"C:\Users\shmal\Downloads\Food safety and storage - Better Health Channel.pdf")

image_url = "https://static.vecteezy.com/system/resources/previews/003/235/639/non_2x/fridge-color-clipart-illustration-design-free-vector.jpg"

col1, col2 = st.columns([3, 1])
with col1:
    st.title("Food Storage Bot")
with col2:
    st.image(image_url, width=100) 

def display_information(food_item):
    ai_response = get_completion(food_item)
    st.write("Here is the information you requested ! :) ")
    st.write(ai_response)

    st.markdown("### <span style='color: red'>Additional Important Information!!!</span>", unsafe_allow_html=True)
    for section, content in pdf_data.items():
        st.write(f"**{section}**:")
        st.write(content)
    
food_item = st.text_input("Hello ! Please enter any food items you have:", '')
if st.button("Go Robot!"):
    if food_item:
        display_information(food_item)
    else:
        st.error("Please enter a food item to proceed.")



