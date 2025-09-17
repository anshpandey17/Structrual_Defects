import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
import datetime as dt

#CONFIGURE THE MODEL
genai.configure(api_key="AIzaSyAd0ryPa58oDWVJOOlyck11oOPMHnJn2_A")
model =genai.GenerativeModel('gemini-2.5-flash-lite')

#UPLOAD AND SHOW IMAGE
st.sidebar.title(":red[UPLOAD YOUR IMAGE HERE]")
#st.title("UPLOADED IMAGE")
uploaded_image = st.sidebar.file_uploader("Here",type=['jpeg','jpg','png'])
if uploaded_image:
    image = Image.open(uploaded_image)
    st.sidebar.subheader(":green[UPLOADED IMAGE]")
    st.sidebar.image(image)

#Create main page
st.title(":orange[STRUCTURAL DEFECTS DETECTION] : :green[***AI assisted structural defects detection***]")
tips=  '''  To use the application follow the steps below:
            * Upload the Image.
            * Click onn the button to generate summary.
            * Click download to save the report generated.
            '''
st.write(tips)
rep_title = st.text_input("Report Title: ",None)
prep_by = st.text_input("Report Prebared by :",None)
prep_for = st.text_input("Report Prebared for :",None)
today = dt.datetime.now().date()

prompt = f'''Assume you are a structrual engineer,The user has provided an image of a 
            structure. You need to identify the structural defects in the image and 
            generate a repost. The repost should contain the following:

             It should start with the title,prepared by and prepared for details.Provided by the user.
             Use {rep_title} at title, {prep_by} as prepared by,{prep_for} as prepared for the same.
             Also mention the current date from {today}
            * Identify and Classify the defects, for eg- crack,spalling,corrosion,honeycombing,etc.
            * There could more than one defects, Identify all the defects seperately.
            * For each defect inentified, provide a short description of the defect and its possible potential impacts on the structure.
            * For each defect, measure the severity of the defect Low,Medium,High.
            * Also mention if the defect is inevitible or avoidable.
            * Also mention the time before this defect leads to permanent damagfe to the structure.
            * Provide Short-term and Long-term solutions along with there estimated cost and time.
            * What precatutionary measures can be taken to avoid such defects in future.
            * The report generated should be in the word format.
            * Use bullet points and tabular format.
            * Make sure that the report does not exceeds 3 Pages.
            '''
if st.button("Generate Report "):
    if uploaded_image is None:
        st.error("Please upload an image first.")
    else:
        with st.spinner("Generating Report...."):
            response = model.generate_content([prompt,image],
                                              generation_config={"temperature":0.5})
            st.write(response.text)

        st.download_button(
                  label = "Download Report",
                  data = response.text,
                  file_name = 'structural_defect_report.pdf',
                  mime = 'text/plain'
                  #mime = 
            )
