# plotter.py

from dataclasses import dataclass
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Function to plot a bolt
def plot_bolt(ax, bolt_length, bolt_diameter, ):
    """Plot a simple representation of a bolt."""
    # Draw bolt shaft
    shaft = patches.Rectangle((-bolt_diameter/2, 0), bolt_diameter, bolt_length, color='gray', edgecolor='black')
    ax.add_patch(shaft)
    
    # Draw bolt head
    head_height = bolt_diameter * 0.5
    head = patches.Rectangle((-bolt_diameter, bolt_length), bolt_diameter*2, head_height, color='darkgray', edgecolor='black')
    ax.add_patch(head)
    
    # return y axis position for stacking
    y = bolt_length
    return y, ax

# Function to plot a washer
def plot_washer(ax, washer_di, washer_do, washer_t, position):
    """Plot a simple representation of a washer."""
    # Draw washer outer circle
    outer_circle = patches.Circle((0, position + washer_t/2), washer_do/2, color='lightgray', zorder=1)
    ax.add_patch(outer_circle)
    
    # Draw washer inner circle (hole)
    inner_circle = patches.Circle((0, position + washer_t/2), washer_di/2, color='white', zorder=2)
    ax.add_patch(inner_circle)
    
    # Draw washer thickness as a rectangle
    thickness_rect = patches.Rectangle((-washer_do/2, position), washer_do, washer_t, color='lightgray', zorder=0)
    ax.add_patch(thickness_rect)
    
    return ax

# Function to plot members
def plot_members(ax, members, start_position, clearance_hole):
    """Plot members as stacked rectangles."""
    current_position = start_position
    for member in members:
        member_rect = patches.Rectangle((-member.thickness*5, current_position), member.thickness*10, member.thickness, color='sandybrown')
        ax.add_patch(member_rect)
        current_position -= member.thickness
    return current_position, ax

# Function to plot nut
def plot_nut(ax, nut_size, position):
    """Plot a simple representation of a nut."""
    # Draw nut as a hexagon
    hexagon = patches.RegularPolygon((0, position), numVertices=6, radius=nut_size/2, orientation=np.pi/6, color='darkgoldenrod')
    ax.add_patch(hexagon)
    
    return ax

# Main function to plot the entire bolted joint
def plot_bolted_joint(joint):

    fig, ax = plt.subplots(figsize=(2, 2))
    ax.set_aspect('equal')
    ax.set_xlim(-joint.bolt.d*2,joint.bolt.d*2)    
    ax.set_ylim(-joint.bolt.d,joint.grip_length()+joint.bolt.d*2)
    # Plot bolt
    bolt_length = joint.grip_length() + joint.bolt.d  # Extra length for head and some margin
    y, ax = plot_bolt(ax, bolt_length, joint.bolt.d)
    
    # Plot members
    y, ax = plot_members(ax, joint.members, y, joint.clearance_hole)
    
    # Plot washer if present
    washer_pos = y + sum(member.thickness for member in joint.members)
    # if joint.washers:
    #     for washer in joint.washers:
    #         plot_washer(ax, washer.di, washer.do, washer.t, washer_pos)
    #         washer_pos += washer.t
    
    # Plot nut
    nut_size = joint.bolt.d * 1.5
    plot_nut(ax, nut_size, washer_pos)

    plt.show()
    return fig, ax