"""
Plotting module for visualizing bolted joints.

This module provides functions to create matplotlib visualizations of bolted joints,
including bolts, washers, members, and nuts.
"""

from dataclasses import dataclass
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

LINE_WIDTH = 0.25

# Function to plot a bolt
def plot_bolt(ax, bolt_length, bolt_diameter):
    """Plot a simple representation of a bolt."""
    # Draw bolt shaft
    shaft = patches.Rectangle((-bolt_diameter/2, 0), bolt_diameter, -bolt_length, facecolor='gray', 
                              edgecolor='black', linewidth=LINE_WIDTH, alpha=1)
    ax.add_patch(shaft)

    # Draw bolt head
    head_height = bolt_diameter * 0.5
    head = patches.Rectangle((-bolt_diameter/2*2, 0), bolt_diameter*2, head_height, facecolor='darkgray', 
                             edgecolor='black', linewidth=LINE_WIDTH, alpha=1)
    ax.add_patch(head)
    
    # return y axis position for stacking
    y = 0
    return y, ax

# Function to plot a washer
def plot_washer(ax, washer, position):
    """Plot a simple representation of a washer."""

    return ax

# Function to plot members
def plot_members(ax, members, y, clearance_hole):
    """Plot members as stacked rectangles."""
    colors = ['sandybrown', 'brown', 'peru', 'chocolate']
    for idx, member in enumerate(members):
        left_member_rect = patches.Rectangle((clearance_hole/2, y), 5, -member.thickness, 
                                             facecolor=colors[idx], edgecolor='black', linewidth=LINE_WIDTH, alpha=1)
        right_member_rect = patches.Rectangle((-clearance_hole/2, y), -5, -member.thickness, 
                                              facecolor=colors[idx], edgecolor='black', linewidth=LINE_WIDTH, alpha=1)
        ax.add_patch(left_member_rect)
        ax.add_patch(right_member_rect)
        y -= member.thickness
    return y, ax

# Function to plot nut
def plot_nut(ax, bolt, y):
    """Plot a simple representation of a nut."""
    # Draw nut as a hexagon
    rect = patches.Rectangle((bolt.d/2, y), width=bolt.d*.5, height=-bolt.d*.75, facecolor='darkgoldenrod',
                             edgecolor='black', linewidth=LINE_WIDTH, alpha=1)
    ax.add_patch(rect)
    
    rect = patches.Rectangle((-bolt.d/2, y), width=-bolt.d*.5, height=-bolt.d*.75, facecolor='darkgoldenrod',
                             edgecolor='black', linewidth=LINE_WIDTH, alpha=1)
    ax.add_patch(rect)

    return ax

# Main function to plot the entire bolted joint
def plot_bolted_joint(joint):

    fig, ax = plt.subplots(figsize=(1, 2))
    ax.set_aspect('equal')
    ax.set_xlim(-joint.bolt.d*3,joint.bolt.d*3)    
    ax.set_ylim(-joint.grip_length()*2,joint.bolt.d*1)
    
    # Plot bolt
    bolt_length = joint.grip_length() + joint.bolt.d  # Extra length for head and some margin
    y, ax = plot_bolt(ax, bolt_length, joint.bolt.d)
    
    # Plot washer under bolt head if present
    plot_washer(ax, joint.washers[0], y) if joint.washers else None

    # Plot members
    y, ax = plot_members(ax, joint.members, y, joint.clearance_hole)
    
    # # Plot washer if present
    # washer_pos = y + sum(member.thickness for member in joint.members)
    # if joint.washers:
    #     for washer in joint.washers:
    #         plot_washer(ax, washer.di, washer.do, washer.t, washer_pos)
    #         washer_pos += washer.t
    
    # Plot nut
    plot_nut(ax, joint.bolt, y)

    # Add minor and major gridlines behind all patches
    ax.grid(which='major', color='grey', linestyle='-', linewidth=0.5, alpha=0.3, zorder=-1)
    ax.grid(which='minor', color='grey', linestyle='--', linewidth=0.25, alpha=0.2, zorder=-1)
    ax.minorticks_on()

    for label in (ax.get_xticklabels() + ax.get_yticklabels()):
        label.set_fontsize(4)

    ax.xaxis.label.set_fontsize(4)
    ax.yaxis.label.set_fontsize(4)
    ax.set_xlabel('inches')
    ax.axis('off')

    return fig, ax