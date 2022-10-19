import streamlit as st
import streamlit_book as stb
import base64
import time
import numpy as np
import math
import hydralit_components as hc
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from collections import namedtuple
import altair as alt
from sim import World, Vehicle

st.set_page_config(page_title="SpaceY", page_icon="🚀", layout="wide")

df = px.data.iris()

@st.experimental_memo
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


img = get_img_as_base64("spacebg.png")

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("https://images.unsplash.com/photo-1555226196-f9930c35a7b6?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2068&q=80");
background-size: 100%;
background-position: top left;
background-repeat: repeat;
background-attachment: local;
}}
[data-testid="stSidebar"] > div:first-child {{
background-image: url("data:image/png;base64,{img}");
background-position: center; 
background-repeat: repeat;
background-attachment: fixed;
}}
[data-testid="stHeader"] {{
background: rgba(0,0,0,0);
}}
[data-testid="stToolbar"] {{
right: 2rem;
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

menu_data = [
    {'icon': "fa fa-desktop", 'label':"Fundamental Indicators"},
    {'icon': "fa fa-signal", 'label':"Rocket Simulation"},
    {'icon': "fa fa-angle-double-left", 'label':"Create your own galaxy"},
    {'icon': "bi bi-pie-chart", 'label':"Asteroid Defense"},
    {'icon': "bi bi-twitter", 'label':"Rocket Launch Prediction"},
]
#    {'icon': "bi bi-telephone", 'label':"Contact us"},
over_theme = {'txc_inactive': "#D3D3D3",'menu_background':'#3948A5','txc_active':'white','option_active':'#3948A5'}
dashboard = hc.nav_bar(
menu_definition=menu_data,
override_theme=over_theme,
home_name='SpaceY.',
hide_streamlit_markers=True, #will show the st hamburger as well as the navbar now!
sticky_nav=True, #at the top or not
sticky_mode='sticky', #jumpy or not-jumpy, but sticky or pinned
use_animation=True,
key='NavBar'
)
st.write('')
st.write('')
st.write('')
st.write('')
if dashboard=='Asteroid Defense':
    stb.set_book_config(path="projectilegame")
elif dashboard=='Rocket Simulation':
    earth = World()

    rocket = Vehicle()
    print(type(rocket))

    rocket.place_on_surface(earth)

    i = 0
    dt = 0.1

    x = []
    y = []
    dy = []
    dx = []
    t_arr = []
    t = 0
    alt = []
    range = []
    ang = []
    heading = []
    rocket.theta = 1
    thrust = 0
    col1, colc, col2 = st.columns((1, 5, 1))


    colc.markdown('<h1 style="text-align: center;">Rocket Space Program Simulation</h1>',
                  unsafe_allow_html=True)
    colc.markdown("""*This project was inspired to emulate a simplified model of a Falcon-9. This ended up being one of our team's most favorite projects as it utilized applied physics and programming""", unsafe_allow_html=False)
    colc.markdown(""" ## The Simulation""", unsafe_allow_html=False)
    colc.markdown("""The environment of the simulation is a simple atmosphere with different pressures based on different altitudes, This was done by using the formulas from this [site](https://www.grc.nasa.gov/www/k-12/rocket/atmosmet.html). \
                    This lets the rocket experience different drag at different positions, making the simulation more realistic. The atmosphere ends at an altitude of 120km, where it is nearly negligible.
                    """, unsafe_allow_html=False)
    colc.markdown("""The gravity changes based off of the  Newton's Universal Law of Gravitation.
                     """, unsafe_allow_html=False)


    colc.markdown(""" ## The Rocket""", unsafe_allow_html=False)
    colc.markdown("""The rocket has 2 control variables: angle and thrust. The angle determines the direction the thrust is applied and the angle is the direction in the absolute cartesian grid of the environment
                    Thrust has a value between 0.0 and 1.0, where one is to the max thrust of the vehicle. The rocket actually also has a grid fin deployment control variable which changes the coefficient of drag from 0.3 to 0.8 (the values are guessed though:)).
                    """, unsafe_allow_html=False)

    colc.markdown("""Other parameters include:\n* Wet Mass -- 549,000 kg\n* Dry Mass (inc. second stage) -- 109,000 kg\n* Fuel Mass -- 440,000 kg\n* Thrust -- 8027 kN\n* Burn Time at full thrust -- 162 seconds""", unsafe_allow_html=True)
    colc.markdown(""" ## Roadmap for the app""", unsafe_allow_html=False)

    colc.markdown('<h1 style="text-align: center;">Vehicle Control</h1>',
                  unsafe_allow_html=True)
    col1, colc1, col2 = st.columns((1,6,1))

    colc1.markdown("""You can program the rocket behaviour in the window below.
    The rocket program is dictionary of dictionaries. At the highest level the dictionary contains unique `rules`. Each `rule` in the dictionary has the following structure:
    """)

    code = """
    ‘UID0’:{‘condition’: {‘var’:{‘>’:0,’<=’:10}},’action’:{‘var_to_set’:1.0}}
    """


    colc1.code(code,language = 'python')

    colc1.markdown("""`UID0` can be any *uniqe* string, it must be uniqe otherise the parser might overwrite the rules.
    \n`var` is the variable that is being evaluated for the rule to activate, this can be anything from the follwoing list:\n- `t` -- Mission time\n- `alt` -- Altitude\n- `range`-- Downrange distance\n- `heading`-- Heading\n- `dalt`-- Rate of change of altitude\n- `drange`-- Rate of change of downrange distance\n""")
    colc1.markdown("""`val_to_set` stands for any of the variables that you can control, you can have multiple values in one rule:\n- `thrust`-- value between 0.0 and 1.0 (zero to max thrust respectively)\n- `angle` -- the direction the thrust is applied, can be an absolute angle between -180 and 180, `prograde` or `retrograde`\n- `gridfins` -- increase coefficent of drag when deployed, the options are `deploy` or `fold`\n- `separation` -- When this keyword is used the mass eqivalent of a Falcon-9 second stage is subrtacted from the vehicle mass. The accimplanying dictionary has to be empty `'separation:{}'`. In the future this will deploy a second vehicle to control.
    """)


    default_command ="""{
    '0': {'condition': {'t': {'>': 0, '<=': 150}}, 'action': {'thrust': 1,'angle':10}},
    '1': {'condition': {'t': {'>': 151, '<=': 200}}, 'action': {'thrust': 0,'angle':'retrograde','separation':{}}},
    '2': {'condition': {'alt': {'>': 0, '<=': 3000},'t':{'>':100},'drange':{'>':10}}, 'action': {'thrust': 1,'angle':'retrograde'}}
     }"""
    commands = colc1.text_area("Program Input",default_command , height = 300)

    ry = colc1.slider("Initial altitude (km)",0,500,0)
    rdy = colc1.slider("Initial vertical velocity (m/s)",-10000,10000,0)
    rdx = colc1.slider("Initial horizontal velocity (m/s)",-10000,10000,0)

    rocket.y = earth.radius + ry*1000
    rocket.dx = rdx
    rocket.dy = rdy

    if colc1.button("Run"):


        while(i < 4*16000):

            rocket.step(commands,earth,dt)

            wx, wy = earth.get_location()
            diffx = -wx + rocket.x
            diffy = -wy + rocket.y
            distance = np.sqrt(np.power(diffx,2)+np.power(diffy,2))

            if distance < earth.radius and t > 10:
                print("crash!")
                break

            t += dt
            i += 1


        template = "plotly_dark"


        # columns for better alignment
        _,col1, col2,_ = st.columns((1,3,3,1))

        labels0 = {
            "x": "x-displacement (m)",
            "y": "y-displacement (m)",
            "alt": "Altitude - displacement (m)",
            "range": "Range - displacement (m)",
            "t": "Mission time (s)",
            "dx": "x - velocity (m/s)",
            "dy": "y - velocity (m/s)",
            "dxy": "Magnitude velocity (m/s)",
            "t": "Mission time (s)",
            "heading": "Heading (deg)",
            "ang": "Vehicle direction (deg)",
            "t": "Mission time (s)"
        }

        bgfix = {
            "plot_bgcolor": "rgba(0, 0, 0, 0)",
            "paper_bgcolor": "rgba(0, 0, 0, 0)",
            }

        df = rocket.get_log()
        # print(df)

        def make_fig(x,y,title,text,col):
            fig = px.line(df, x=x, y=y, template=template, title=title,
                           labels=labels0)
            fig.update_layout(bgfix)
            col.plotly_chart(fig, use_container_width=True)
            col.markdown(text)

        text0 = 'Range is the displacement following the surface of the earth, altitude is the distance above the surface of the earth.'
        make_fig("range","alt","Downrange distance and Altitude",text0,col1)

        text1 = 'Same information as above but split into alt and range; plotted against mission time.'
        make_fig("t",["alt", "range"],"Altitude and range displacements.",text1,col1)

        text10 = 'alt,range and magnitude velocity against mission time.'
        make_fig("t",["dalt", "drange", "dxy"],"X and y displacements against time in the xy plane",text10,col1)


        text2 = 'This graph shows the same information as on the left but in an absolute xy plane form. Useful for seeing how the rocket flies around the curvuture of the earth.'
        make_fig("x","y","x and y displacements in the xy plane",text2,col2)

        text3 = 'Same info as above, split into compnents '
        make_fig("t",["y","x"],"x and y displacements in the xy plane",text3,col2)

        text3 = 'x,y and magnitude velocity against mission time.'
        make_fig("t",["dy", "dx", "dxy"],"X and y displacements against time in the xy plane",text3,col2)

        text4=''
        make_fig("t",["heading","ang"],"Heading (in the absolute xy plane)",text4,col2)


        text5='Fuel and total vehicle mass'
        make_fig("t",["fuel","mass"],"Heading (in the absolute xy plane)",text5,col1)
if dashboard=='Create your own galaxy':
    total_points = st.slider("Number of points in spiral", 1, 6000, 2000)
    num_turns = st.slider("Number of turns in spiral", 1, 150, 9)

    Point = namedtuple('Point', 'x y')
    data = []

    points_per_turn = total_points / num_turns

    for curr_point_num in range(total_points):
        curr_turn, i = divmod(curr_point_num, points_per_turn)
        angle = (curr_turn + 1) * 2 * math.pi * i / points_per_turn
        radius = curr_point_num / total_points
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        data.append(Point(x, y))

    st.altair_chart(alt.Chart(pd.DataFrame(data), height=650, width=650)
        .mark_circle(color='#0068c9', opacity=0.5)
        .encode(x='x:Q', y='y:Q'))
elif dashboard=='Rocket Launch Prediction':
    st.title('Rocket Launch Prediction')
elif dashboard=='SpaceY.':
    title='''
    <link href='https://fonts.googleapis.com/css?family=Arva' rel="stylesheet">
        <style>
        .spacey {
            font-family: 'Arva';
            font-size: 25px;
            margin-top:0px;
            font-weight: 700;
            margin-bottom: 0px;
        }
        </style>
        <body>
        <center> <p1 class='spacey'> SpaceY. </p1> </center>
        </body>
        '''
    st.markdown(title, unsafe_allow_html=True)
