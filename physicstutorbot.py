import streamlit as st
from streamlit_scroll_navigation import scroll_navbar



st.set_page_config(
    page_title="Physics TutorBot",
    page_icon="🧪",
    layout="wide"
)
left_col, right_col = st.columns(2)

with st.container(): #first section
    with left_col:
    
    

        st.markdown("<h1 style='color: #D3D3D3;'>Welcome to Physics TutorBot!</h1>", unsafe_allow_html=True)

        st.subheader("Struggling with Newton’s laws or momentum problems? Meet Physics Tutor AI – the smart, interactive way to master physics!")

        st.write("Explore interactive lessons, problem-solving techniques, and expert guidance")


        import streamlit as st

        page_bg_color = """
        <style>
        body {
            background-color: #1E1E2E;  /* Dark navy blue */
            color: white;
        }
        </style>
        """
        st.markdown(page_bg_color, unsafe_allow_html=True)

    

with right_col:
    st.sidebar.title("Navigation")

    sections = st.sidebar.radio("Go to:", ["Physics Tutoring", "Free-body Diagram Tutoring", "Learning Resources"])

    





if sections == "Physics Tutoring":
    #basic chatbot
    st.write("--------")
    st.subheader("Ask your issues! :tada:")
    suggestions = ["What is Newton's First Law?", "How to implment air-resistnace in overall Net Force of these problems?", "How to calculate momentum with objects coliding?", "A 70 kg football player tackles an 90 kg player running toward him at 6 m/s. If they stic, what's their final velocity?"]
    st.write("Sugested questions")
    for suggestion in suggestions:
        if st.button(suggestion):
            st.session_state

        #give sugestion questions

elif sections == "Free-body Diagram Tutoring":
     #freebody diagram questions
    st.write("-----------")
    st.subheader("Got any Free Body Diagram issues? Allow us to assist you")

elif sections == "Learning Resources":
     #learning resources
    st.write("-------------")
    st.subheader("Don't know where to start? Click here! Learning Resources for your guidance")

#my quizes (personal quizes for given topic)
#my progress


    

