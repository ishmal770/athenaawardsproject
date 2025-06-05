import streamlit as st
from streamlit_scroll_navigation import scroll_navbar
import openai
from openai import OpenAI 
import turtle
from PIL import Image
def draw_FBD():
    screen = turtle.Screen()
    screen.setup(width = 500, height=500)
    screen.bgcolor("white")
    t = turtle.Turtle()
    t.speed(3)
    t.color("blue")
    for dihhhh in range(4):
        t.forward(100)
        
        t.right(90)
    ts = t.getscreen()
    ts.getcanvas().postscript(file="drawing.eps") 
    img = Image.open("drawing.eps")
    img.save("drawing.png")
    






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

    sections = st.sidebar.radio("Go to:", ["Physics Tutoring", "Free-body Diagram Tutoring", "Learning Resources", "Personal Quizzes", "My progress"])

    





if sections == "Physics Tutoring":
    #basic chatbot
    st.write("--------")
    st.subheader("Ask your issues! :tada:")
    
    user = OpenAI(api_key=st.secrets["api_keys"]["openai_key"])
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-4o-mini"
    if "messages" not in st.session_state:
        st.session_state.messages = []
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message['content'])
    if prompt := st.chat_input("Provide your issues and we will answer!"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
                stream = user.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[{"role": "user", "content": prompt}],
                stream=True,
            )
        response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})

    suggestions = ["What is Newton's First Law?", "How to implment air-resistnace in overall Net Force of these problems?", "How to calculate momentum with objects coliding?", "A 70 kg football player tackles an 90 kg player running toward him at 6 m/s. If they stic, what's their final velocity?"]
    st.write("Suggested questions")
    for suggestion in suggestions:
        if st.button(suggestion):
            prompt = suggestion
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            with st.chat_message("assistant"):
                stream = user.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[{"role": "user", "content": prompt}],
                stream=True,
            )
            
                
            response = st.write_stream(stream)
            st.session_state.messages.append({"role": "assistant", "content": response})

        #give sugestion questions

elif sections == "Free-body Diagram Tutoring":
     #freebody diagram questions
    st.write("-----------")
    st.subheader("Got any Free Body Diagram issues? Allow us to assist you")
    user = OpenAI(api_key=st.secrets["api_keys"]["openai_key"])
    chat_input = st.chat_input("Don't know what forces are required? Ask!")
    if chat_input:
        response_1 = user.chat.completions.create(
            model = 'gpt-4o',
            messages=[{"role":"user", "content": "What forces are required for this problem:" +chat_input+"Please only state the forces and nothing else. Do not mention the reasoning as well, please state the forces in one string, like a list"}] #sends the forces needed so user to adjust which forces are needed
        )
        st.write(response_1["choices"][0]["message"]["content"])
        response_list = response_1["choices"][0]["message"]["content"]
    example_forces = ["Tension", "Gravity"]
    for force in response_list:
        for f_1 in example_forces:
            if f_1 == force:
                st.write("force")
    if st.button("Draw & Display"):
        draw_FBD()
    st.image("drawing.png", caption="Turtle Drawing", use_column_width=True)


#with the list of forces, if each force cheks with one of these, draw the forces then expoert them

elif sections == "Learning Resources":
     #learning resources
    st.write("-------------")
    st.subheader("Don't know where to start? Click here! Learning Resources for your guidance")

#my quizes (personal quizes for given topic)
elif sections == "Personal Quizzes":
    st.write("-------------")
    st.subheader("Want some practice? Here's your go to place!")

elif sections == "My progress":
    st.write("---------------")
    st.subheader("Check out your progress!")
#my progress


    

