import streamlit as st
import os
import time
from langchain_google_genai import ChatGoogleGenerativeAI

os.environ['GOOGLE_API_KEY'] =  'AIzaSyDNBCKeFjjtfOqk4lzVUP0PZVJ55mkLkJM'


def generative_Model(input):
    llm  = ChatGoogleGenerativeAI(model='gemini-pro',api_key=os.environ['GOOGLE_API_KEY'])
    response = llm.invoke(input)
    return response.content


def Clean_Text(data):
    form_one = data.split('\n')
    
    mcqs = []
    current_question = None

    for line in form_one:
        line = line.strip()
        if line.startswith('**MCQ'):
            if current_question:
                mcqs.append(current_question)
            current_question = {
                'question': '',
                'options': [],
                'answer': ''
            }
        elif line.startswith('**Answer:'):
            current_question['answer'] = line.split(' ')[-1].strip('()')
        elif line.startswith('('):
            current_question['options'].append(line)
        elif line:
            if not current_question['question']:
                current_question['question'] = line
            else:
                current_question['question'] += ' ' + line

    if current_question:
        mcqs.append(current_question)
    return mcqs


def index():

    st.title('Langchain Gemini & Streamlit')
    st.header('Quiz Application 📚')
    input = st.text_input('Enter Topic Name')
    button = st.button('Submit Topic')
    if button :
        if input:
            st.success('Please Fill Requirement')
        else:
            st.error('Please Enter Topic Name')



    with st.sidebar:
        st.title('Please Fill Requirement 🖋 ')
        option = st.selectbox(
            "Select Difficulties Level",
            ("Basic", "Intermedit", "Advancecd"))
        noMcqs = st.selectbox(
            "Numbers Of Mcqs",
            ('5','6',"7", "8", "9","10","11","12"))
        my_button = st.button('Submit')
        if my_button:
            with st.spinner("Loading..."):
                time.sleep(1)
                st.success('Done')
        st.subheader('Follow Me 🎓')
        st.link_button("Connect LinkedIn",'https://www.linkedin.com/in/alihassanml')
        st.link_button("Follow On Github",'https://github.com/alihassanml',type="secondary")
        st.caption('Develop by: Ali Hassan')
    if my_button:
        my_input = f'Generate 4 option Mcqs topic is {input} no of mcqs is {noMcqs} level {option} also answer'
        data = []
        data = generative_Model(my_input)
        mcqs = Clean_Text(data)
        st.session_state['mcqs'] = mcqs
        
    result =0
    if 'mcqs' in st.session_state:
        for i, mcq in enumerate(st.session_state['mcqs']):
            a = st.radio(
                mcq['question'],
                mcq['options'],
                index=None
            )
            if a:
                if a[1] == mcq['answer'][0]:
                    st.success('Answer Is Correct')
                    result +=1
                else:
                    st.error(f"Incorrect Answer! Correct Answer {mcq['answer'][0]}")
        button = st.button('Show Result')
        if button:
            persentage = (result/ int(noMcqs))*100
            if persentage >= 40.0:
                st.success(f'Congurlation! Your Resule is : {result} / {noMcqs} \n Persentage {persentage} ')
            else:
                st.error(f'Try again! Your Resule is : {result} / {noMcqs} \n Persentage {persentage} ')

        


if __name__ == '__main__':
    index()




