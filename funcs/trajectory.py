from matplotlib import pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import numpy as np

def motion(v0, theta, t, g=9.81, x0=0, y0=0):
    x = v0*np.cos(theta)*t 
    y = v0*np.sin(theta)*t - 0.5 * g * t**2
    return x, y

def get_time(v0, theta, g=9.81, x0=0, y0=0):
    t_max = 2*v0*np.sin(theta)/g

    t = np.linspace(0, t_max, 100)
    return t

def get_trajectory(v0, theta_deg, g=9.81, gravity_label="", x0=0, y0=0):
    theta_rad = theta_deg * np.pi / 180
    t = get_time(v0, theta_rad, g=g, x0=x0, y0=y0)
    x, y = motion(v0, theta_rad, t, g=g, x0=x0, y0=y0)
    legend = f"$v_0$={v0}, $\\theta$={theta_deg:.2f}, g={g} ({gravity_label})"
    color_dict = {'Earth':"green", 'Moon':"gray", 'Mars':"red", 'Jupiter':"black"}
    color = color_dict[gravity_label]
    trajectory_dict = {"x": x, "y": y, "legend": legend, "color": color, "v0": v0, "theta_deg": theta_deg}
    return trajectory_dict

def plot_emoji(emoji_path, ax, x, y, zoom=0.35):
    image = plt.imread(emoji_path)
    image_box = OffsetImage(image, zoom=zoom)
    ab = AnnotationBbox(image_box, (x, y), frameon=False)
    ax.add_artist(ab)
    return


def fig_from_list(trajectory_list, pig_position=[]):
    fig = plt.figure(figsize=(16,12))
    ax = plt.subplot(111)
    legend = []
    xmax_list = []
    linestyles = ['-', '--', '-.', ':']
    for i, trajectory in enumerate(trajectory_list):
        plt.plot(trajectory["x"], trajectory["y"], 
                    color = trajectory["color"], 
                    linestyle=linestyles[i%len(linestyles)])
        legend.append(trajectory["legend"])
        xmax_list.append(np.max(trajectory["x"]))
    plt.xlabel('x - horizonal distance in meters', fontsize=20)
    plt.ylabel('y - vertical distance in meters', fontsize=20)

    if len(pig_position) > 0:        
        plot_emoji("images/pig.png", ax, pig_position[0], pig_position[1])
        xmax_list.append(pig_position[0])
        for trajectory in trajectory_list:
            plot_emoji("images/bird.png", ax, trajectory["x"][-1], trajectory["y"][-1])
        plt.legend(legend, fontsize=20, loc='upper center')

    if len(xmax_list) > 0:
        xmax = max(xmax_list)
        plt.xlim(-xmax*0.05, xmax*1.05)
        plt.ylim(-xmax*0.05, xmax*1.05)

    return fig

def check_solution(pig_position, trajectory_list):
    x_tol, y_tol = 1.0, 1.0
    for trajectory in trajectory_list:
        x = trajectory["x"][-1]
        y = trajectory["y"][-1]
        if abs(pig_position[0] - x) < x_tol and abs(pig_position[1] - y) < y_tol:
            return True
    return False
