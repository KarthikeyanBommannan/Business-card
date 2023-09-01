from bizcard import saved_img
import os
import cv2
import matplotlib.pyplot as plt
import re
import pandas as pd

def save_card(uploaded_card):
    directory = "uploaded_image_file"
    os.makedirs(directory, exist_ok=True)  # Create the directory if it doesn't exist

    with open(os.path.join(directory, uploaded_card.name), "wb") as f:
        f.write(uploaded_card.getbuffer())
    
def image_preview(image,result): 
    for (bbox, text, prob) in result: 
    # unpack the bounding box
        (tl, tr, br, bl) = bbox
        tl = (int(tl[0]), int(tl[1]))
        tr = (int(tr[0]), int(tr[1]))
        br = (int(br[0]), int(br[1]))
        bl = (int(bl[0]), int(bl[1]))
        cv2.rectangle(image, tl, br, (0, 255, 0), 2)
        cv2.putText(image, text, (tl[0], tl[1] - 10),
        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
    plt.rcParams['figure.figsize'] = (15,15)
    plt.axis('off')
    plt.imshow(image)
    
    
def img_to_binary(file_path):
    # Convert image data to binary format
    with open(file_path, 'rb') as file:
        binary_data = file.read()
    return binary_data


data = {        "company_name" : [],
                    "card_holder" : [],
                    "designation" : [],
                    "mobile_number" :[],
                    "email" : [],
                    "website" : [],
                    "area" : [],
                    "city" : [],
                    "state" : [],
                    "pin_code" : [],
                    "image" : img_to_binary(saved_img)
            }

def get_data(res, data):
    for ind,i in enumerate(res):
    # To get WEBSITE_URL
        if "www " in i.lower() or "www." in i.lower():
            data["website"].append(i)
        elif "WWW" in i:
            data["website"] = res[4] +"." + res[5]

        # To get EMAIL ID
        elif "@" in i:
            data["email"].append(i)

        # To get MOBILE NUMBER
        elif "-" in i:
            data["mobile_number"].append(i)
            if len(data["mobile_number"]) ==2:
                data["mobile_number"] = " & ".join(data["mobile_number"])

        # To get COMPANY NAME  
        elif ind == len(res)-1:
            data["company_name"].append(i)

        # To get CARD HOLDER NAME
        elif ind == 0:
            data["card_holder"].append(i)

        # To get DESIGNATION
        elif ind == 1:
            data["designation"].append(i)

        # To get AREA
        if re.findall('^[0-9].+, [a-zA-Z]+',i):
            data["area"].append(i.split(',')[0])
        elif re.findall('[0-9] [a-zA-Z]+',i):
            data["area"].append(i)

        # To get CITY NAME
        match1 = re.findall('.+St , ([a-zA-Z]+).+', i)
        match2 = re.findall('.+St,, ([a-zA-Z]+).+', i)
        match3 = re.findall('^[E].*',i)
        if match1:
            data["city"].append(match1[0])
        elif match2:
            data["city"].append(match2[0])
        elif match3:
            data["city"].append(match3[0])

        # To get STATE
        state_match = re.findall('[a-zA-Z]{9} +[0-9]',i)
        if state_match:
            data["state"].append(i[:9])
        elif re.findall('^[0-9].+, ([a-zA-Z]+);',i):
            data["state"].append(i.split()[-1])
        if len(data["state"])== 2:
            data["state"].pop(0)

        # To get PINCODE        
        if len(i)>=6 and i.isdigit():
            data["pin_code"].append(i)
        elif re.findall('[a-zA-Z]{9} +[0-9]',i):
            data["pin_code"].append(i[10:])
            
def create_df(data):
    df = pd.DataFrame(data)
    return df
