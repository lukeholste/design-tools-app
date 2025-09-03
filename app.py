import streamlit as st
import pandas as pd
import numpy as np
from typing import List, Optional

from classes import Bolt, Washer, Member, BoltedJoint
from resources import bolt_sizes, materials, clearance_holes
from plotter import plot_bolted_joint

# ========= Load Data ========
BOLT_SIZES = bolt_sizes()
MATERIALS = materials()
CLEARANCE_HOLES = clearance_holes()

# ========= Session State Initialization ========
def initialize_session_state():
    """Initialize session state variables if they don't exist."""
    if 'bolt_instance' not in st.session_state:
        st.session_state.bolt_instance = None
    if 'joint_instance' not in st.session_state:
        st.session_state.joint_instance = None

# ========= Helper Functions ========
def create_bolt(size: str, tpi: str, material: str) -> Optional[Bolt]:
    """Create a bolt instance with error handling."""
    try:
        return Bolt(size=size, tpi=str(tpi), material=material)
    except ValueError as e:
        st.error(f"Error creating bolt: {e}")
        return None

def create_bolt_instance():
    """Create and store bolt instance in session state."""
    if all(key in st.session_state for key in ['bolt_size', 'bolt_tpi', 'bolt_material']):
        bolt_instance = create_bolt(
            st.session_state.bolt_size,
            st.session_state.bolt_tpi, 
            st.session_state.bolt_material
        )
        st.session_state.bolt_instance = bolt_instance

def update_material_properties(df: pd.DataFrame) -> pd.DataFrame:
    """Update material properties in dataframe based on selected materials."""
    df = df.copy()  # Avoid modifying original dataframe
    for idx, row in df.iterrows():
        mat = row['Material']
        if mat in MATERIALS:
            df.at[idx, 'E [GPa]'] = round(MATERIALS[mat]['E'] / 1e9, 2)
            df.at[idx, 'S-y [MPa]'] = round(MATERIALS[mat]['S-y'] / 1e6, 2)
            df.at[idx, 'ν'] = round(MATERIALS[mat]['v'], 3)
    return df

def rows_to_members(df: pd.DataFrame) -> List[Member]:
    """Convert dataframe rows to Member objects."""
    members = []
    for _, row in df.iterrows():
        t_in = row.get('t [in]')
        mat = row.get('Material')
        if pd.notna(t_in) and pd.notna(mat) and t_in > 0:
            try:
                members.append(Member(thickness=t_in, material=mat))
            except Exception as e:
                st.error(f"Error creating Member: {e}")
    return members

def create_joint(bolt: Optional[Bolt], members: List[Member], 
                washers: Optional[List[Washer]] = None, clearance: str = 'Normal'):
    """Create and store joint instance in session state."""
    if bolt and len(members) > 1:
        try:
            clearance_hole_dia = CLEARANCE_HOLES[bolt.size][clearance.lower()]
            st.session_state.joint_instance = BoltedJoint(
                bolt=bolt, 
                members=members, 
                clearance_hole=clearance_hole_dia,
                washers=washers, 
                preload=0
            )
        except Exception as e:
            st.error(f"Error creating BoltedJoint: {e}")
            st.session_state.joint_instance = None
    else:
        st.session_state.joint_instance = None

# ======== Streamlit App ========
def main():
    """Main Streamlit application."""
    st.set_page_config(page_title="Bolted Joint Analyzer", layout="wide")
    st.title("Bolted Joint Analyzer")
    
    # Initialize session state
    initialize_session_state()
    
    st.subheader("Fastener Parameters")

    col1, col2 = st.columns([1, 2])

    with col1:
        # Bolt configuration section
        joint_type = st.selectbox('Bolt Type', options=['Tapped Hole', 'Bolted Joint'], 
                                key='joint_type', index=1)
        
        bolt_size = st.selectbox('Bolt Size', options=list(BOLT_SIZES.keys()), 
                               index=0, placeholder='Select bolt size', 
                               key='bolt_size', on_change=create_bolt_instance)

        # Clearance hole selection for bolted joints
        if joint_type == 'Bolted Joint':
            clearance = st.selectbox('Clearance Hole Dia.', 
                                   options=['Loose', 'Normal', 'Tight', 'Custom'],
                                   key='clearance_type')
            if clearance == 'Custom':
                st.number_input(label='Hole Dia. [in]', min_value=BOLT_SIZES[bolt_size]['d'],
                              key='custom_hole_dia')
            else:
                hole_dia = CLEARANCE_HOLES[bolt_size][clearance.lower()]
                st.write(f"Hole Diameter: {hole_dia:.3f} in")

        # Thread pitch selection
        tpi_options = BOLT_SIZES[bolt_size]['tpi']
        tpi = st.selectbox('TPI', options=list(tpi_options.keys()), 
                         index=0, placeholder='Select TPI', 
                         key='bolt_tpi', on_change=create_bolt_instance)
        
        # Material selection
        material = st.selectbox('Bolt Material', options=list(MATERIALS.keys()), 
                              index=0, placeholder='Select material', 
                              key='bolt_material', on_change=create_bolt_instance)

        st.button('Create Bolt', on_click=create_bolt_instance)

        # Member configuration section
        st.subheader('Member Parameters')
        render_member_editor()
        
        # Display current instances
        display_current_instances()

    with col2:
        # Visualization section
        render_visualization()

def render_member_editor():
    """Render the member editor interface."""
    # Member dataframe
    df = pd.DataFrame(columns=['t [in]', 'Material', 'E [GPa]', 'S-y [MPa]', 'ν'])
    material_options = list(MATERIALS.keys())

    editable_cols = ['t [in]', 'Material']
    edited_df = st.data_editor(
        df[editable_cols],
        num_rows='dynamic',
        column_config={
            "Material": st.column_config.SelectboxColumn(
                "Material",
                options=material_options
            ),
            "t [in]": st.column_config.NumberColumn(
                "t [in]",
                min_value=0.000,
                format="%.3f",
            )
        },
        hide_index=True, key='member_editor', width=400
    )

    df[editable_cols] = edited_df
    updated_df = update_material_properties(df)
    st.dataframe(updated_df, width='stretch', hide_index=True)

    # Create joint button
    clearance_type = st.session_state.get('clearance_type', 'Normal')
    st.button('Create Joint', on_click=create_joint, 
            args=(st.session_state.get('bolt_instance'), 
                  rows_to_members(updated_df), None, clearance_type))

def display_current_instances():
    """Display current bolt and joint instances."""
    if st.session_state.bolt_instance:
        st.write("**Current Bolt:**")
        st.write(st.session_state.bolt_instance)
    
    if st.session_state.joint_instance:
        st.write("**Current Joint:**")
        st.write(st.session_state.joint_instance)
    elif st.session_state.bolt_instance:
        st.info("Add members and create joint to see joint details.")

def render_visualization():
    """Render the bolt visualization."""
    st.subheader("Bolt Visualization")
    if st.session_state.joint_instance:
        try:
            fig, ax = plot_bolted_joint(st.session_state.joint_instance)
            st.pyplot(fig, width='stretch')
        except Exception as e:
            st.error(f"Error creating visualization: {e}")
    else:
        st.info("Create a bolt and joint to see the visualization.")

if __name__ == "__main__":
    main()
