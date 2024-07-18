import streamlit as st
import os
import re
import json
import shutil
from PIL import Image
from multi_modal import multimodal
from SQLdata import init_db, insert_business_cards_from_json, fetch_all_business_cards


def extract_json(data_list):
    extracted_data = []
    for item in data_list:
        # 'info' 필드에서 JSON 부분 추출
        json_string = re.search(r'```json\n(.*)\n```', item['info'], re.DOTALL).group(1)
        # JSON 문자열을 딕셔너리로 변환
        json_data = json.loads(json_string)
        extracted_data.append(json_data)
    return extracted_data

# Set the path to the directory where images will be saved
save_path = '/root/LLM_Bootcamp/exercise_2/data/img'

# Ensure the directory exists
os.makedirs(save_path, exist_ok=True)

st.set_page_config(page_title="명함 인식 서비스", layout="centered")

# Function to display business card information
def display_business_card(card):
    id, name, company, job_title, phone, address, email, image_path = card

    st.image(image_path, width=250)
    st.markdown(f"### {name}")
    st.markdown(f"**회사:** {company}")
    st.markdown(f"**직함:** {job_title}")
    st.markdown(f"**전화번호:** {phone}")
    st.markdown(f"**주소:** {address}")
    st.markdown(f"**이메일:** {email}")
    st.markdown("---")

# Function to delete all files in a directory
def delete_all_files_in_directory(directory_path):
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            st.error(f'Failed to delete {file_path}. Reason: {e}')

# Main upload and processing logic
def image_upload_page():
    st.title("명함을 업로드 해주세요.")

    uploaded_files = st.file_uploader("Upload Images", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

    if uploaded_files:
        for uploaded_file in uploaded_files:
            # Save the uploaded file
            file_path = os.path.join(save_path, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # Open the uploaded image
            img = Image.open(file_path)

            # Create a resized copy for display purposes, preserving aspect ratio
            display_img = img.copy()
            display_img.thumbnail((250, 250))  # Resize the image to fit within a 250x250 box, preserving aspect ratio

            # Display the resized image
            st.image(display_img, caption=uploaded_file.name, use_column_width=True)

        st.success(f"Successfully saved {len(uploaded_files)} file(s) to {save_path}")

        try:
            data_of_card = extract_json(multimodal())[0]
            image_path = f"/root/LLM_Bootcamp/exercise_2/data/img/{uploaded_file.name}"

            conn1 = init_db()
            insert_business_cards_from_json(conn1, data_of_card, image_path)

            u = fetch_all_business_cards(conn1)
            st.title("Saved Business Cards")
            for card in u:
                display_business_card(card)
        except AttributeError:
            st.error(f"해당 사진은 명함이 아닙니다.")
        except IndexError:
            st.error(f"차단된 사람입니다.")

        if st.button("Delete All Data and Images"):
            delete_all_files_in_directory("/root/LLM_Bootcamp/exercise_2/data/img/")
            os.remove('/root/LLM_Bootcamp/exercise_2/data/business_cards.db')
            st.warning("All data and images have been deleted.")

# Run the image upload page function
image_upload_page()
