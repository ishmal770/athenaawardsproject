import streamlit as st
from streamlit_scroll_navigation import scroll_navbar
import openai
from openai import OpenAI 
import turtle
from PIL import Image
import time
from openai import RateLimitError

def draw_Forcearrow(force): #drawign first the square then the arrow
    screen = turtle.Screen()
    screen.setup(width = 500, height=500)
    screen.bgcolor("white")
    t = turtle.Turtle()
    t.speed(3)
    t.color("blue")
    t.goto(50,50)
    for dihhhh in range(4):
        t.forward(100)
        
        t.right(90)
    t=turtle.Turtle() 
    initlizae()
    if force == "Friction":
        t.backward(150)
        
        t.right(135)  # Rotate for arrowhead
        t.forward(20)  # First part of arrowhead
        t.backward(20)  # Return to line
        t.left(90)  # Rotate for second part
        t.forward(20)
        
        t.goto(50, 50)
    if force == "Applied Force":
        t.forward(150)
        
        t.right(135)  # Rotate for arrowhead
        t.forward(20)  # First part of arrowhead
        t.backward(20)  # Return to line
        t.left(90)  # Rotate for second part
        t.forward(20)
        
        t.goto(50, 50)
    if force == "Normal Force" or force == "Air Resistance" or force == "Tension":
        t.left(90)
        t.forward(150)
        
        t.right(135)  # Rotate for arrowhead
        t.forward(20)  # First part of arrowhead
        t.backward(20)  # Return to line
        t.left(90)  # Rotate for second part
        t.forward(20)
        
        t.goto(50, 50)
    if force == "Gravity":
        t.right(90)
        t.right(135)  # Rotate for arrowhead
        t.forward(20)  # First part of arrowhead
        t.backward(20)  # Return to line
        t.left(90)  # Rotate for second part
        t.forward(20)
        
        t.goto(50, 50)
    return t
def initlizae(): #sets turtle to the middle of the square
    t = turtle.Turtle()
    t.goto(50, 50)
    return t

def save_turtle_image():
    
    ts = turtle.getscreen()
    ts.getcanvas().postscript(file="forces_diagram.eps")
    img = Image.open("forces_diagram.eps")
    img.save("forces_diagram.png")
    turtle.done()





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

    




user = OpenAI(api_key=st.secrets["api_keys"]["openai_key"])
if sections == "Physics Tutoring":
    #basic chatbot
    st.write("--------")
    st.subheader("Ask your issues! :tada:")
    
    
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
                time.sleep(2)  # Wait for 2 seconds before making a new API call
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
                time.sleep(2)  # Wait for 2 seconds before making a new API call
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
    
    chat_input = st.chat_input("Don't know what forces are required? Ask!")
    response_list=[]
    try:
        if chat_input:
            time.sleep(2)  # Wait for 2 seconds before making a new API call
            response_1 = user.chat.completions.create(
                model = 'gpt-4o',
                messages=[{"role":"user", "content": "What forces are required for this problem:" +chat_input+"Please only state the forces and nothing else. Do not mention the reasoning as well, please state the forces in a list format"}] #sends the forces needed so user to adjust which forces are needed
            )
            st.write(response_1["choices"][0]["message"]["content"])
            response_list = list(response_1["choices"][0]["message"]["content"].split(", "))
        example_forces = ["Tension", "Gravity", "Friction", "Applied Force", "Normal Force", "Air Resistance"]
        if len(response_list)>0:
            for force in response_list:
                for f_1 in example_forces:
                    if f_1 == force:
                        draw_Forcearrow(f_1)
            if st.button("Draw & Display"):
                st.image("forces_diagram.png")
                
            st.image("drawing.png", caption="Turtle Drawing", use_column_width=True)
    except RateLimitError as e:
        st.write("Rate limit exceeded.Please check your usage or upgrade your plan")


#with the list of forces, if each force cheks with one of these, draw the forces then expoert them

elif sections == "Learning Resources":
     #learning resources
    st.write("-------------")
    st.subheader("Don't know where to start? Click here! Learning Resources for your guidance")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("Cheat Sheets")
        physicstopics = st.selectbox("Choose a topic:" ["Forces", "Newton's First Laws", "Momentum", "Free-body Diagrams", "Kinematics"])
    with col2:
        st.write("Worksheets on Provided Topics")
        physicstopics = st.selectbox("Choose a topic:" ["Forces", "Newton's First Laws", "Momentum", "Free-body Diagrams", "Kinematics"])
    with col3:
        st.write("Learn more!")

#my quizes (personal quizes for given topic)
elif sections == "Personal Quizzes":
    st.write("-------------")
    st.subheader("Want some practiche? Here's your go to place!")

#my progress


    

