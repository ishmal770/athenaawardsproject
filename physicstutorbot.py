import streamlit as st
from streamlit_scroll_navigation import scroll_navbar
import openai
from openai import OpenAI 
import turtle
from PIL import Image
import time
from openai import RateLimitError
import matplotlib.pyplot as plt
import numpy as np






def draw_Forcearrow_matplot(forces_dict):
    fig,ax = plt.subplots(figsize=(5, 5))
    #draw square in center
    square = plt.Rectangle((0.4,0.4),0.2,0.2, fill=None, edgecolor = 'blue', linewidth =3)
    ax.add_patch(square)

    

    
    

    # Draw the force arrow
    if force == "Friction":
        dx, dy= (-1,0)
        
    elif force == "Applied Force":
        dx, dy = (1,0)
    elif force in ["Normal Force", "Air Resistance", "Tension"]:
        dx,dy = (0,1)
    elif force == "Gravity":
        dx, dy = (0, -1)
    for force, mag in forces_dict.items():
        arrow_length = mag/100*0.3 #scaled
        ax.arrow(0.5, 0.5, dx*arrow_length, dy*arrow_length, head_width=0.04, head_length=0.04, fc='red', ec='red', length_includes_head=True)
        ax.text(0.5+dx(arrow_length+0.05), 0.5+dy*(arrow_length+0.05), f"{force}\n({mag} N)", fontsize=12, color='black', ha='center', va='center')
    ax.set_xlim(0,1)
    ax.set_ylim(0,1)
    ax.axis('off')
    plt.tight_layout()
    st.pyplot(fig)
    #draw arrow
    

   





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

    sections = st.sidebar.radio("Go to:", ["Physics Tutoring", "Free-body Diagram Tutoring", "Learning Resources", "Personal Quizzes"])

    




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
                time.sleep(2)  #Wait for 2 seconds before making a new API call
                stream = user.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[{"role": "user", "content": prompt}],
                stream=True,
            )
        response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})

    suggestions = ["What is Newton's First Law?", "How to implement air-resistance in overall Net Force of these problems?", "How to calculate momentum with objects coliding?", "A 70 kg football player tackles an 90 kg player running toward him at 6 m/s. If they stic, what's their final velocity?"]
    st.write("Suggested questions")
    for suggestion in suggestions:
        if st.button(suggestion):
            prompt = suggestion
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            with st.chat_message("assistant"):
                time.sleep(2)  #Wait for 2 seconds before making a new API call
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
    forces_dict={}
    st.write("-----------")
    st.subheader("Got any Free Body Diagram issues? Allow us to assist you")
    example_forces = ["Tension", "Gravity", "Friction", "Applied Force", "Normal Force", "Air Resistance"]
    airresistance = st.checkbox("Air Resistance", value=False)
    tension = st.checkbox("Tension", value=False)
    gravity = st.checkbox("Gravity", value=False)
    applied_force = st.checkbox("Applied Force", value=False)
    normal_force = st.checkbox("Normal Force", value=False)
    friction = st.checkbox("Friction", value=False)
    st.write("Please choose the magnitude of the forces you selected")
    if airresistance:
        
        airmag = st.slider("Air Resistance Magnitude (N)", min_value=0, max_value=100, value=50)
        forces_dict["Air Resistance"] = airmag
        
    if tension:
        tensionmag = st.slider("Tension Magnitude (N)", min_value=0, max_value=100, value=50)
        forces_dict["Tension"] = tensionmag
    elif gravity:
        gravitymag = st.slider("Gravity Magnitude (N)", min_value=0, max_value=100, value=50)
        forces_dict["Gravity"] = gravitymag
        
    elif applied_force:
        appliedforcemag = st.slider("Applied Force Magnitude (N)", min_value=0, max_value=100, value=50)
        forces_dict["Applied Force"] = appliedforcemag
    elif normal_force:
        normalforcemag = st.slider("Normal Force Magnitude (N)", min_value=0, max_value=100, value=50)
        forces_dict["Normal Force"] = normalforcemag
    elif friction:
        frictionmag = st.slider("Friction Magnitude (N)", min_value=0, max_value=100, value=50)
        forces_dict["Friction"] = frictionmag
    
    if forces_dict and st.button("Draw & Display"):
        draw_Forcearrow_matplot(forces_dict)


    """
    if "fbd_last_input" not in st.session_state:
        st.session_state["fbd_last_input"] = ""
    if "fbd_response" not in st.session_state:
        st.session_state["fbd_response"] = ""
    if "fbd_forces" not in st.session_state:
        st.session_state["fbd_forces"] = []
    
    chat_input = st.chat_input("Don't know what forces are required? Ask!")
    response_list=[]
    example_forces = ["Tension", "Gravity", "Friction", "Applied Force", "Normal Force", "Air Resistance"]
    if chat_input and chat_input != st.session_state['fbd_last_input']:
        try:
            time.sleep(2)
            response_1 = user.chat.completions.create(
                model = 'gpt-4o',
                messages=[{"role":"user", "content": "What forces are required for this problem:" +chat_input+"Please only state the forces and nothing else. Do not mention the reasoning as well, please state the forces in a list format"}] #sends the forces needed so user to adjust which forces are needed
            )
            response_text = response_1["choices"][0]["message"]["content"]
            st.session_state["fbd_response"] = response_text
            st.session_state["fbd_last_input"] = chat_input
            st.session_state["fbd_forces"] =[f.strip() for f in response_text.split(' ')]
        except:
            st.warning("An error occurred while processing your request. Please try again.")
            st.stop()
    
    if st.session_state["fbd_response"]:
        st.write(st.session_state["fbd_response"])
            
        
        
        for force in st.session_state["fbd_forces"]:
            for f_1 in example_forces:
                if f_1 == force:
                    draw_Forcearrow(f_1)
        if st.button("Draw & Display"):
            st.image("forces_diagram.png")
                
        st.image("drawing.png", caption="Turtle Drawing", use_column_width=True)
    """
    

#with the list of forces, if each force cheks with one of these, draw the forces then expoert them

elif sections == "Learning Resources":
     #learning resources
    st.write("-------------")
    st.subheader("Don't know where to start? Click here! Learning Resources for your guidance")
    physicstopics = st.selectbox("Choose a topic:", ["Newton's Laws", "Momentum", "Kinematics", "Work Energy and Power"])
    option = st.selectbox(
    "Select a difficulty level:",
    ["Beginner", "Intermediate", "Advanced"],
    index=1  #default is intermediate
    )
    st.write(f"You have chosen:")
    st.write(f"- Topic: {physicstopics}")
    st.write(f"- Difficulty Level: {option}")

    resources= {
        "Newton's Laws": {
            "Beginner":{
                "cheatsheets": "[Newton's Laws Beginner CheatSheets](https://docs.google.com/document/d/1aMXKxg8wvjad8Mkp1bsozAD-v-7co1f7HhIEO_hI6X0/edit?usp=sharing)",
                "worksheets": "[Newton's Laws Beginner  Worksheets](https://docs.google.com/document/d/1VGhDk3gPLV2ybv2oVoUXUuKnrv0tg_7SbvpbZNRM2Og/edit?usp=sharing)",
                "learnmore":"[Newton's Laws Beginner  Resources](https://www.britannica.com/science/Newtons-laws-of-motion)"

                #cheatsheets first
                #worksheets second
                #websites for learning third
            },
            "Intermediate":{
                "cheatsheets":"[Newton's Laws Intermediate CheatSheets](https://docs.google.com/document/d/1kvPoVHqKRtap8ElkgU0Aaz2vd_HpAtDu0IlFaOcsHyU/edit?usp=sharing)", #changed
                "worksheets": "[Newton's Laws Intermediate Worksheets](https://docs.google.com/document/d/1pGWgZqkW5tQPelP7LVVhk_GyUEe82kBQTl5DHIFqj7g/edit?usp=sharing)", #changed
                "learnmore":"[Newton's Laws Intermediate Resources](https://edu.gcfglobal.org/en/newtons-laws-of-motion/)" #changed

            },
            "Advanced": {
                "cheatsheets":"[Newton's Laws Advanced CheatSheets](https://docs.google.com/document/d/15bF8z3eI_fwnlepEnGzdHGOcaCQ9KcjKjK--oJjGZvc/edit?usp=sharing)", #changed
                "worksheets":"[Newton's Laws Advanced Worksheets](https://docs.google.com/document/d/1J72wqBTOLD4EAzjrRoVZ0M6gYarIm1cxFD6hxT27RZY/edit?usp=sharing)", #changed
                "learnmore":"[Newton's Laws Advanced Resources](https://www.khanacademy.org/science/physics/forces-newtons-laws)" #changed


            }
        },
        "Momentum": {
            "Beginner":{
                "cheatsheets": "[Momentum Beginner  CheatSheets](https://cheatography.com/goldennfluff/cheat-sheets/momentum-physics-12-unit-2)", #changed
                "worksheets": "[Momentum Beginner  Worksheets](https://www.teacherspayteachers.com/Product/Momentum-Calculations-Classwork-Worksheet-beginner-friendly-11764257)", #changed
                "learnmore":"[Momentum  Beginner Resources](https://momentum.org/)" #changed

                #cheatsheets first
                #worksheets second
                #websites for learning third
            },
            "Intermediate":{
                "cheatsheets":"[Momentum  Intermediate CheatSheets](https://physicstutorials.org/impulse-momentum/impulse-momentum-cheat-sheet)", #changed
                "worksheets": "[Momentum  Intermediate Worksheets](https://sfponline.org/Uploads/71/Momentum Worksheet.pdf)", #changed
                "learnmore":"[Momentum  Intermediate Resources](https://www.sciencefacts.net/momentum.html)" #changed

            },
            "Advanced": {
                "cheatsheets":"[Momentum Advanced CheatSheets](https://flippingphysics.com/uploads/2/1/1/0/21103672/0198_lecture_notes_-_ap_physics_c-_momentum_impulse_collisions_and_center_of_mass_review__mechanics_.pdf)", #changed 
                "worksheets":"[Momentum Advanced Worksheets](https://studylib.net/doc/8947608/momentum-worksheet)", #changed
                "learnmore":"[Momentum Advanced Resources](https://phet.colorado.edu/)" #changed


            }
        },
        "Kinematics": {
            "Beginner":{
                "cheatsheets": "[Kinematics Beginner  CheatSheets](https://physicstutorials.org/mechanics/kinematics/kinematics-cheatsheet)", #changed
                "worksheets": "[Kinematics Beginner  Worksheets](https://scribd.com/document/535863807/WORKSHEET-1-KINEMATICS)", #changed
                "learnmore":"[Kinematics  Beginner Resources](https://www.physicsclassroom.com/class/1DKin/Lesson-1/Introduction)" #changed

                #cheatsheets first
                #worksheets second
                #websites for learning third
            },
            "Intermediate":{
                "cheatsheets":"[Kinematics Intermediate CheatSheets](https://courses.physics.illinois.edu/phys211/sp2020/practice/formula-sheet.pdf)", #changed
                "worksheets": "[Kinematics Intermediate Worksheets](https://owhentheyanks.com/kinematics-worksheet-with-answers)", #changed
                "learnmore":"[Kinematics Intermediate Resources](https://www.coursera.org/courses?query=kinematics)" #changed

            },
            "Advanced": {
                "cheatsheets":"[Kinematics Advanced CheatSheets](https://acejee.com/blog/kinematics-notes-jee-main-jee-advanced)",  #changed
                "worksheets":"[Kinematics Advanced Worksheets](https://physexams.com/Pdf-files/Kinematics)", #changed
                "learnmore":"[Kinematics Advanced Resources](https://www.khanacademy.org/)" #changed


            }
        },
        "Work Energy and Power": {
            "Beginner":{
                "cheatsheets": "[Work Energy and Power Beginner  CheatSheets](https://worksheeto.com/post_physics-work-energy-and-power-worksheet_247580)", #changed
                "worksheets": "[Work Energy and Power Beginner  Worksheets](https://www.physicsclassroom.com/getattachment/Teacher-Toolkits/Work-Energy-Fundamentals/Work-Energy-Fundamentals-PDF-Version/WorkEnergy1.pdf?ext=.pdf)", #changed 
                "learnmore":"[Work Energy and Power  Beginner Resources](https://www.physicsclassroom.com/CLASS/energy)" #changed

                #cheatsheets first
                #worksheets second
                #websites for learning third
            },
            "Intermediate":{
                "cheatsheets":"[Work Energy and Power Intermediate CheatSheets](https://www.physicstutorials.org/energy-work-power/work-power-energy-cheat-sheet/)", #changed
                "worksheets": "[Work Energy and Power Intermediate Worksheets](https://lessondberoticised.z22.web.core.windows.net/work-energy-and-power-worksheet.html)", #changed 
                "learnmore":"[Work Energy and Power Intermediate Resources](https://www.need.org/need-students/energy-infobooks/)" #changed 

            },
            "Advanced": {
                "cheatsheets":"[Work Energy and Power Advanced CheatSheets](https://classoraclemedia.com/uploads/4/2/3/1/42314577/phbcs07workpowerenergy-141009145603-conversion-gate01.pdf)",  
                "worksheets":"[Work Energy and Power Advanced Worksheets](https://www.physicsclassroom.com/calcpad/energy)", 
                "learnmore":"[Work Energy and Power Advanced Resources](https://phys.libretexts.org/Bookshelves/College_Physics/College_Physics_1e_%28OpenStax%29/07%3A_Work_Energy_and_Energy_Resources)" 


            }
        }
    }
        
        
        
        
        
        
        
        #all the resources for each topic and the difficulty
    selected_Course = resources.get(physicstopics, {}).get(option, {})

    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("Cheat Sheets")
        
        

        
        cheatsheet_url = selected_Course.get("cheatsheets", None)

        if cheatsheet_url:
            st.markdown(cheatsheet_url, unsafe_allow_html=True)
            
        else:
            st.write("No cheat sheets available.")


        
    with col2:
        st.subheader("Worksheets on Provided Topics")
        
        worksheets_url = selected_Course.get("worksheets", None)
        if worksheets_url:
            st.markdown(worksheets_url, unsafe_allow_html=True)
            
        else:
            st.write("No worksheets available.")

        

    with col3:
        st.subheader("Learn more!")
        
        learnmore_url = selected_Course.get("learnmore", None)
        if learnmore_url:
            st.markdown(learnmore_url, unsafe_allow_html=True)
            
        else:
            st.write("No additional learning resources available.")


#my quizes (personal quizes for given topic)
elif sections == "Personal Quizzes":
    st.write("-------------")
    st.subheader("Want some practice? Here's your go to place!")
    list_ofchoices = ["Newton's Laws", "Momentum", "Kinematics", "Work Energy and Power"]
    topic = st.selectbox("Choose a topic:", list(list_ofchoices))
    quiz_questions = {
        "Newton's Laws": [
            
            {"question": "What is Newton's First Law also known as?", "options": ["Law of Gravity", "Law of Inertia", "Law of Motion"], "answer": "Law of Inertia"},
            {"question": "Which force keeps planets in orbit?", "options": ["Friction", "Gravity", "Magnetism"], "answer": "Gravity"},
            
            
            {"question": "What is the equation for Newton's Second Law?", "options": ["F = ma", "P = mv", "E = mc²"], "answer": "F = ma"},
            
            
            {"question": "In a frictionless environment, an object in motion will…?", "options": ["Stop", "Continue moving", "Change direction"], "answer": "Continue moving"},
            {"question": "A 10kg object accelerates at 4 m/s^2. What's the net force?", "options": ["30", "55", "45", "40"], "answer": "40"},
            {"question": "A 50 N forces pushes a 5 kg box. What's its acceleration", "options": ["10", "15", "6", "3.3"], "answer": "10"},
            {"question": "A 1000 kg car accelerates from 0 to 20 m/s in 5 s. What's the net force?", "options": ["4000", "2500", "1500", "1000"], "answer": "4000"},
            {"question": "A 5kg object's velocity changes from 10 m/s to 4 m/s in 2s. Whats the Net Force", "options": ["30", "15", "45", "40"], "answer": "15"},
            {"question": "A 60 kg skydiver falls with 400 N of air resistance. What's acceleration?", "options": ["0.312", "20.2", "99", "34"], "answer": "20.2"},
            {"question": "A 30 kg child on a sled experiences 60 N of friction. If pulled with 100 N, what's a?", "options": ["4/3", "2/3", "1/5", "0"], "answer": "4/3"},
            {"question": "A 500 N net force stops a 100 kg object from moving at 10 m/s. How long does it take?", "options": ["3", "55", "2", "44"], "answer": "2"},
            
        ],
        "Momentum": [
            
            {"question": "A 5 kg cat runs at 8 m/s. What its momentum?", "options": ["40", "35", "23"], "answer": "40"}, #changed
            {"question": "A 0.2 kg baseball has a momentum of 6 kg*m/s. What's its velocity", "options": ["30", "15", "45"], "answer": "30"}, #changed
            
            
            {"question": "A 1200 kg car moves at 25 m/s. What's its momentum?", "options": ["12,578", "25,000", "30,000"], "answer": "30,000"}, #changed
            
            
            {"question": "A 60 kg sprinter has a momentum of 720*kg*m/s. What's her speed?", "options": ["1", "2", "5"], "answer": "2"}, #changed
            {"question": "A 0.02 kg bullet travels at 400 m/s. What's its momentum?", "options": ["30", "80", "45", "40"], "answer": "80"}, #changed
            {"question": "A 90 kg hockey player skates at 10 m/s. What's its momentum?", "options": ["6", "5", "2", "3.3"], "answer": "6"}, #changed
            {"question": "A 1500 kg truck's momentum is 45,000 kg*m/s. What's its momentum", "options": ["900", "2500", "1500", "1000"], "answer": "900"},#changed
            {"question": "A 0.5 kg soccer ball is kicked to 12 m/s. What's its momentum?", "options": ["30", "6", "5", "4"], "answer": "6"}, #changed
            {"question": "A 70 kg runner's momentum is 490 kg*m/s. What's her velocity?", "options": ["7", "20.2", "9", "4"], "answer": "7"}, #changed
            {"question": "A 2 kg toy car moving at 3 m/s hits a 1 kg stationary car. If they stick, what's their final speed?", "options": ["4", "2", "1", "0"], "answer": "2"},
            {"question": "A 50 kg archer shoots a 0.1 kg arrow at 50 m/s. What's the archer's recoil speed?", "options": ["0.3", "0.1", "2", "4.4"], "answer": "0.1"},

       


            
        ],
        "Kinematics": [
            
            {"question": "Which of the following is a vector quantity?", "options": ["Speed", "Distance", "Velocity"], "answer": "Velocity"}, #changed
            {"question": "What does the slope of a velocity-time graph represent?", "options": ["Speed", "Acceleration", "45"], "answer": "Acceleration"}, #changed
            
            
            {"question": " If an object moves with constant acceleration, its velocity vs. time graph is:", "options": ["A curved line", "A horizontal line", "A diagonal straight line"], "answer": "A diagonal straight line"}, #changed
            
            
            {"question": " A car accelerates from rest at 4 m/s² for 5 seconds. What is its final velocity?", "options": ["1", "2", "5"], "answer": "20"}, #changed
            {"question": "Which of the following statements is true about free-falling objects?", "options": ["They experience constant velocity", "They accelerate at 9.8 m/s² downward", "Their motion depends on their mass", "40"], "answer": "They accelerate at 9.8 m/s² downward"}, #changed 
            {"question": "The area under a velocity-time graph represents:", "options": ["Acceleration", "Distance traveled", "2", "3.3"], "answer": "Distance traveled"}, #changed
            {"question": "Which of the following equations is NOT a kinematics equation?", "options": ["( v = u + at )", "( F = ma )", "v2 + 2as", "1000"], "answer": " F = ma"},#changed
            {"question": "A projectile is launched at an angle. Its horizontal acceleration is:", "options": ["9.8", "6", "5", "4"], "answer": "9.8"}, #changed
            {"question": "A ball thrown straight up reaches its highest point. At that moment, its velocity is:?", "options": ["Maximum", "Zero", "Negative", "Constant"], "answer": "Zero"}, #changed
            {"question": "If an object moves in uniform circular motion, its speed is:?", "options": ["Constant", "Increasing", "Decreasing", "0"], "answer": "Constant"},#changed
            {"question": "What happens to the acceleration of an object in free fall when air resistance is considered?", "options": ["It stays the same", "0", "It decreases over time", "It increases over time"], "answer": "It decreases over time"},
            
        ],
        "Work Energy and Power": [
            
            {"question": "What is the SI unit of work?", "options": ["Newton", "Joule", "Watt"], "answer": "Joule"}, #changed
            {"question": "Which of the following is an example of kinetic energy?", "options": ["A stretched rubber band", "A moving car", "A compressed spring"], "answer": "A moving car"}, #changed
            
            
            {"question": " What is the formula for work done when force is applied at an angle θ?", "options": ["( W = Fd )", "( W = Fd \cosθ )", "A diagonal straight line"], "answer": "( W = Fd \cosθ )"}, #changed
            
            
            {"question": " Which of the following statements is true about power?", "options": ["Power is the rate at which work is done", "Power is measured in Joules", "Power depends only on force applied"], "answer": "Power is the rate at which work is done"}, #changed
            {"question": "A machine does 500 Joules of work in 10 seconds. What is its power output?", "options": ["50 W", "5000 W", "5 W", "40 W"], "answer": "50 W"},  #changed
            {"question": "What type of energy is stored in a stretched spring?", "options": ["Kinetic energy", "Thermal energy", "2", "3.3"], "answer": "Thermal energy"}, #changed
            {"question": "Which of the following is an example of work being done?", "options": ["Holding a book in place", "Pushing a box across the floor", "v2 + 2as", "1000"], "answer": "Pushing a box across the floor"}, #changed
            {"question": "If the velocity of an object is doubled, its kinetic energy will:", "options": ["Remain the same", "Double", "Quadruple", "4"], "answer": "Quadruple"}, #changed
            {"question": "What is the work done when a force of 10 N moves an object 5 meters in the direction of the force?", "options": ["45", "50", "23", "Constant"], "answer": "50"}, #changed
            {"question": "Which of the following is NOT a form of mechanical energy?", "options": ["Kinetic Energy", "Potential Energy", "Thermal Energy", "Elastic Energy"], "answer": "Thermal Energy"}, #changed
            {"question": "A wind-powered generator converts wind energy into electrical energy. The electrical power output is proportional to:?", "options": ["Wind speed", "0", "Wind speed squared", "Wind speed cubed"], "answer": "Wind speed cubed"}, #changed
            
        ],
    }
    if "quiz_topic" not in st.session_state or st.session_state["quiz_topic"] != topic:
        st.session_state["quiz_topic"] = topic
        st.session_state["question_index"] = 0
        st.session_state["score"] = 0
        st.session_state["show_result"] = False
        st.session_state["selected_answer"] = None


    selected_questions = quiz_questions.get(topic, {})
    total_questions = len(selected_questions)
    progress = (st.session_state["question_index"] / total_questions) if total_questions else 0
    
    
    
   
    if st.session_state["question_index"]< total_questions:
            

            
        current_question = selected_questions[st.session_state["question_index"]]

        st.subheader(f"Question {st.session_state['question_index'] + 1}: {current_question['question']}")
        
        selected_answer = st.radio("Choose your answer:", current_question["options"], index=None)
        submit = st.button("Submit", key=f"submit_{st.session_state['question_index']}")

        
        if submit:
            if selected_answer == current_question["answer"]:
                st.session_state["score"] += 1
                st.success("✅ Correct!")
                        
            else:
                st.error(f"❌ Incorrect! The correct answer is {current_question['answer']}.")

                    
            st.session_state["selected_answer"] = selected_answer
                    
                    
            st.session_state["question_index"] += 1
                    
                    
            st.rerun()
                    
            
    else:
        st.success(f"🎉 Quiz Completed! Your final score: {st.session_state['score']} / {len(selected_questions)}")

    st.progress(progress)



 
   


#my progress




