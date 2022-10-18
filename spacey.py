import streamlit as st
import streamlit_book as stb
import base64
import time
import numpy as np
import math
import plotly.graph_objects as go
import hydralit_components as hc

st.set_page_config(page_title="SpaceY", page_icon="🚀", layout="wide")
menu_data = [
    {'icon': "fa fa-desktop", 'label':"Fundamental Indicators"},
    {'icon': "fa fa-signal", 'label':"Chart Analysis"},
    {'icon': "fa fa-angle-double-left", 'label':"Backtesting"},
    {'icon': "bi bi-pie-chart", 'label':"Asteroid Defense"},
    {'icon': "bi bi-twitter", 'label':"Twitter Analysis"},
]
#    {'icon': "bi bi-telephone", 'label':"Contact us"},
over_theme = {'txc_inactive': "#D3D3D3",'menu_background':'#3948A5','txc_active':'white','option_active':'#3948A5'}
dashboard = hc.nav_bar(
menu_definition=menu_data,
override_theme=over_theme,
home_name='Tradelyne',
hide_streamlit_markers=True, #will show the st hamburger as well as the navbar now!
sticky_nav=True, #at the top or not
sticky_mode='sticky', #jumpy or not-jumpy, but sticky or pinned
use_animation=True,
key='NavBar'
)
if dashboard=='Asteroid Defense':
    stb.set_book_config(path="projectilegame")
