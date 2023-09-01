import streamlit as st
from PIL import Image
import easyocr
import matplotlib.pyplot as plt
import cv2
import os
from conversion import *

st.markdown(f""" <style>.stApp {{
                        background: url("https://cutewallpaper.org/22/plane-colour-background-wallpapers/189265759.jpg");
                        background-size: cover}}
                     </style>""", unsafe_allow_html=True)

st.write("Business Card")
st.sidebar.form("Upload Business Card Image")
uploaded_image_file = st.sidebar.file_uploader("Upload Business Image File", type=['PNG', 'JPEG', 'JPG'])
submitted = st.sidebar.button("Submit")
if submitted:
    images = Image.open(uploaded_image_file)
    st.image(images)

if uploaded_image_file is not None:
    save_card(uploaded_image_file)

    # INITIALIZING THE EasyOCR READER
    reader = easyocr.Reader(['en'])

    saved_img = os.getcwd() + "\\" + "uploaded_image_file" + "\\" + uploaded_image_file.name
    result = reader.readtext(saved_img, detail=0, paragraph=False)
    image = cv2.imread(saved_img)
    res = reader.readtext(saved_img)
    st.markdown("### Image Processed and Data Extracted")
    st.plt.pyplot(image_preview(image, res))

data = {
    "company_name": [],
    "card_holder": [],
    "designation": [],
    "mobile_number": [],
    "email": [],
    "website": [],
    "area": [],
    "city": [],
    "state": [],
    "pin_code": [],
    "image": img_to_binary(saved_img)
}

get_data(res)  # <-- Pass the data dictionary to the function
df = create_df(data)
upload_to_database(df)
