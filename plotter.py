# plotter.py

from dataclasses import dataclass
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Constants for visualization
BOLT_HEAD_HEIGHT_RATIO = 0.5  # Bolt head height as ratio of diameter
BOLT_HEAD_WIDTH_RATIO = 2.0   # Bolt head width as ratio of diameter
MEMBER_WIDTH_RATIO = 10.0     # Member width as ratio of thickness  
NUT_SIZE_RATIO = 1.5          # Nut size as ratio of bolt diameter
FIGURE_SIZE = (2, 2)          # Default figure size
BOLT_MARGIN_RATIO = 2.0       # Margin around bolt as ratio of diameter

# Function to plot a bolt
def plot_bolt(ax, bolt_length, bolt_diameter):
    """Plot a simple representation of a bolt."""
    # Draw bolt shaft
    shaft = patches.Rectangle((-bolt_diameter/2, 0), bolt_diameter, bolt_length, 
                            facecolor='gray', edgecolor='black')
    ax.add_patch(shaft)
    
    # Draw bolt head
    head_height = bolt_diameter * BOLT_HEAD_HEIGHT_RATIO
    head_width = bolt_diameter * BOLT_HEAD_WIDTH_RATIO
    head = patches.Rectangle((-head_width/2, bolt_length), head_width, head_height, 
                           facecolor='darkgray', edgecolor='black')
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
        member_width = member.thickness * MEMBER_WIDTH_RATIO
        member_rect = patches.Rectangle((-member_width/2, current_position), 
                                      member_width, member.thickness, 
                                      facecolor='sandybrown', edgecolor='black')
        ax.add_patch(member_rect)
        current_position -= member.thickness
    return current_position, ax

# Function to plot nut
def plot_nut(ax, nut_size, position):
    """Plot a simple representation of a nut."""
    # Draw nut as a hexagon
    hexagon = patches.RegularPolygon((0, position), numVertices=6, radius=nut_size/2, 
                                   orientation=np.pi/6, facecolor='darkgoldenrod', 
                                   edgecolor='black')
    ax.add_patch(hexagon)
    
    return ax

def plot_bolted_joint(joint):
    """Main function to plot the entire bolted joint."""
    fig, ax = plt.subplots(figsize=FIGURE_SIZE)
    ax.set_aspect('equal')
    
    bolt_diameter = joint.bolt.d
    grip_length = joint.grip_length()
    
    # Set plot limits with proper margins
    margin = bolt_diameter * BOLT_MARGIN_RATIO
    ax.set_xlim(-margin, margin)    
    ax.set_ylim(-bolt_diameter, grip_length + bolt_diameter * BOLT_MARGIN_RATIO)
    
    # Plot bolt
    bolt_length = grip_length + bolt_diameter  # Extra length for head and some margin
    y, ax = plot_bolt(ax, bolt_length, bolt_diameter)
    
    # Plot members
    y, ax = plot_members(ax, joint.members, y, joint.clearance_hole)
    
    # Calculate nut position
    washer_pos = y + sum(member.thickness for member in joint.members)
    
    # Plot washer if present
    if joint.washers:
        for washer in joint.washers:
            plot_washer(ax, washer.di, washer.do, washer.t, washer_pos)
            washer_pos += washer.t
    
    # Plot nut
    nut_size = bolt_diameter * NUT_SIZE_RATIO
    plot_nut(ax, nut_size, washer_pos)

    plt.show()
    return fig, ax