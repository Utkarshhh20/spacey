import streamlit as st
import numpy as np

from funcs.trajectory import get_trajectory, fig_from_list, check_solution

# Fill up the page
c1, c2 = st.columns([8,1])
c1.title("The Game")
restart = c2.button("Restart")

# Gravity constants by planet
Gravity_constant = {'Earth': 9.8, 'Moon': 1.6, 'Mars': 3.7, 'Jupiter': 24.8}

# Setup the session_state variables
if restart or "guesses_remaining" not in st.session_state:
    st.session_state["guesses_remaining"] = 3

if restart or"guess_list" not in st.session_state:
    st.session_state["guess_list"] = []

if restart or"gravity_game_index" not in st.session_state:
    st.session_state["gravity_game_index"] = np.random.randint(0, len(Gravity_constant))
planet_list = list(Gravity_constant.keys())
planet_game = planet_list[st.session_state["gravity_game_index"]]
gravity_game = Gravity_constant[planet_game]

if restart or "solution" not in st.session_state:
    v0_sol = np.random.randint(30, 60)
    theta_deg_sol = 45
    theta_rad_sol = theta_deg_sol * np.pi / 180
    t_max_sol = 2*v0_sol*np.sin(theta_rad_sol)/gravity_game
    x_max_sol = v0_sol*np.cos(theta_rad_sol)*t_max_sol
    aste_position = [x_max_sol, 0]
    st.session_state["solution"] = {
                                    "aste_position":aste_position, 
                                    "v0_sol": v0_sol, 
                                    "theta_deg_sol": theta_deg_sol,
                                    }

article_dict = {'Earth': "", 'Moon': "the", 'Mars': "", 'Jupiter': ""}
c1.subheader(f"Can you hit the target on {article_dict[planet_game]} {planet_game}?")

# Pig position
x_text = f"x = {st.session_state.solution['aste_position'][0]:.3f} meters"
y_text = f"y = {st.session_state.solution['aste_position'][1]:.3f} meters"
st.write(f"The target is at **{x_text}** and **{y_text}**")
# Get the parameters
st.subheader("Enter the parameters")
c1, c2, c3, c4 = st.columns([3,3,3,1])
dv0 = 1
v0 = c1.slider("Initial Velocity [meters/second]", 
                        min_value=dv0, max_value=100*dv0, 
                        value=50, step=dv0, help="Initial velocity for the projectile")
dtheta = 1
theta_deg = c2.slider("Initial Angle [degrees]", 
                        min_value=5, max_value=90, 
                        value=30, step=5, help="Initial velocity for the projectile")
# options for gravity: earth, moon, mars, jupiter
c3.metric(value=gravity_game, label=f"{planet_game}'s gravity in m/s^2")

# Shoooooot
if st.session_state["guesses_remaining"] > 0:
    if c4.button("Shoot!"):
        st.session_state["guesses_remaining"] -= 1
        trajectory_dict = get_trajectory(v0, theta_deg, gravity_game, planet_game)
        st.session_state["guess_list"].append(trajectory_dict)

# Placeholder for information
placeholder = st.empty()

# Always plot, to show the target
fig = fig_from_list(st.session_state["guess_list"], st.session_state.solution["aste_position"])
st.pyplot(fig)

# We check if we hit the pig after the shoot we have guesses left
if check_solution(st.session_state.solution["aste_position"], st.session_state["guess_list"]):
    placeholder.success("You hit the rock!...I mean asteriod!")
elif st.session_state["guesses_remaining"] == 0:
    line_1 = "Oh no you are out of guesses :( anyway"
    v0_sol = st.session_state.solution["v0_sol"]
    theta_deg_sol = st.session_state.solution["theta_deg_sol"]
    line_2 = f"One possible solution was $v_0$={v0_sol} [m/s^2] and $\\\\theta$={theta_deg_sol} [deg]"
    placeholder.error(line_1 + line_2)
else:
    # Say to keep trying, but only if at least tried once
    if st.session_state['guesses_remaining']==2:
        text = f"Keep trying! You have {st.session_state['guesses_remaining']} guesses remaining. Did you try solving the equations?"
        placeholder.warning(text)
    if st.session_state['guesses_remaining']==1:
        text = f"Last Guess you got thisss!!!"
        placeholder.warning(text)
