
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

plt.rcParams["figure.dpi"]=300

# Function to calculate volume of liquid in an inverted truncated cone
def calculate_volume(R, r, H, h):
    if h > H:
        h = H
    r_h = r + (R - r) * h / H
    volume = (1/3) * np.pi * h * (r**2 + r * r_h + r_h**2)
    return volume


# Functions from @Mateen Ulhaq and @karlo
def set_axes_equal(ax: plt.Axes):
    """Set 3D plot axes to equal scale.

    Make axes of 3D plot have equal scale so that spheres appear as
    spheres and cubes as cubes.  Required since `ax.axis('equal')`
    and `ax.set_aspect('equal')` don't work on 3D.
    """
    limits = np.array([
        ax.get_xlim3d(),
        ax.get_ylim3d(),
        ax.get_zlim3d(),
    ])
    origin = np.mean(limits, axis=1)
    radius = 0.5 * np.max(np.abs(limits[:, 1] - limits[:, 0]))
    _set_axes_radius(ax, origin, radius)

def _set_axes_radius(ax, origin, radius):
    x, y, z = origin
    ax.set_xlim3d([x - radius, x + radius])
    ax.set_ylim3d([y - radius, y + radius])
    ax.set_zlim3d([z - radius, z + radius])

# Function to plot the 3D cone and water level
def plot_cone(R, r, H, h):
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')

    # Create mesh for the full cone
    z = np.linspace(0, H, 50)
    theta = np.linspace(0, 2 * np.pi, 50)
    Z, Theta = np.meshgrid(z, theta)
    R_mesh = r + (R - r) * Z / H
    X = R_mesh * np.cos(Theta)
    Y = R_mesh * np.sin(Theta)

    ax.plot_surface(X, Y, Z, alpha=0.1, color='grey', edgecolor='k')
    ax.set_zlim(0,H+50)
    ax.set_box_aspect([1.0, 1.0, 1.0])

    # ax.set_aspect("auto")
    # set_axes_equal(ax)

    # Create mesh for the water level
    z_water = np.linspace(0, h, 30)
    Z_w, Theta_w = np.meshgrid(z_water, theta)
    R_w = r + (R - r) * Z_w / H
    X_w = R_w * np.cos(Theta_w)
    Y_w = R_w * np.sin(Theta_w)

    ax.plot_surface(X_w, Y_w, Z_w, alpha=0.6, color='blue', edgecolor='k')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Height', fontsize=10)
    # ax.set_title('Inverted Truncated Cone with Water Level',fontsize=14)
    plt.tight_layout()
    # ax.set_box_aspect([1,1,H/10])  # Aspect ratio

    return fig

# Streamlit UI
st.header("Slurry Tank Volume Calculator",divider=True)
R=st.number_input("Top Radius R (cm)",value=150.0)
# R = st.slider("Top Radius R (m)", min_value=1.0, max_value=5.0, value=2.0)
r=st.number_input("Bottom Radius r (cm)",value=15.0)
# r = st.slider("Bottom Radius r (m)", min_value=0.1, max_value=R, value=0.15)
H=st.number_input("Total Height H (cm)",value=200.0)
# H = st.slider("Total Height (H)", min_value=1.0, max_value=5.0, value=2.0)
h = st.slider("Water Height h (cm)", min_value=0.0, max_value=H, value=100.0,step=0.5)

volume = calculate_volume(R, r, H, h)
st.write(f"### Volume of liquid at height {h} cm is: {volume/1000:.2f} Liters")

fig = plot_cone(R, r, H, h)
st.pyplot(fig)
