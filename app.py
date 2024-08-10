import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai 
import os
from PIL import Image

#loading all the environment variables
load_dotenv()

#calling my api key here
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))


input_prompt=''' you are an expert nutritionsit where you need to accuratly identify the food items from the image and calculate the total calaories present in it and tell if consuming this is good for health or not. Give some details of the food items, if they are healthy or not. 
give the name of the food item present and the calory it have in the following format:
1. Item 1 - no. of calories
2. Item 1 - no. of calories
----
----
give a nutiriton report like as of a nutritionist
'''

#function interacting with the moel
def gemini_response(input_prompt, image):
    model=genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input_prompt,image[0]])
    return response.text

def image_format(file_uploaded):
    if file_uploaded is not None:   #if file is uploaded
        bytes_data= file_uploaded.getvalue()   #reading the file into bytes


        image_parts = [
            {
                "mime_type": file_uploaded.type,   #getting mime type of the image
                "data": bytes_data
            }
        ]
        return image_parts
    
    else:
        raise FileNotFoundError('Upload a file first')
 
st.set_page_config(page_title='Virtual Nutritionists')


st.header('Hello! I am your Virtual ready-to-go Nutritionist!')
file_uploaded =st.file_uploader('choose your image', type=['jpg','jpeg','png'])

image= ''
if file_uploaded is not None:
    image=Image.open(file_uploaded) #image should open below (preview)
    st.image(image, caption='uploaded image', use_column_width=True)

submit=st.button('Tell me')

if submit: #botton is clicked
    image_data= image_format(file_uploaded)
    response= gemini_response(input_prompt, image_data)
    st.header("for your better health and well being :")
    st.write(response)
