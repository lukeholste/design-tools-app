import streamlit as st
import pandas as pd
import numpy as np
import json
from classes import Bolt, Washer, Member, BoltedJoint
from resources import bolt_sizes, materials, clearance_holes
from plotter import plot_bolted_joint
from threading import RLock

_Lock = RLock()

# ========= Load Data ========
BOLT_SIZES = bolt_sizes()
MATERIALS = materials()
CLEARANCE_HOLES = clearance_holes()

# ========= Helper Functions ========
def create_bolt(size, tpi, mat):
    return Bolt(
        size=size,
        tpi=str(tpi),
        material=mat
    )

def create_bolt_instance():
    try:
        bolt_instance = create_bolt(bolt, tpi, material)
        st.session_state.bolt_instance = bolt_instance
    except ValueError as e:
        st.error(str(e))
        st.session_state.bolt_instance = None

def update_material_properties(df):
    for idx, row in df.iterrows():
        mat = row['Material']
        if mat in MATERIALS:
            df.at[idx, 'E [GPa]'] = round(MATERIALS[mat]['E'] / 1e9, 2)
            df.at[idx, 'S-y [MPa]'] = round(MATERIALS[mat]['S-y'] / 1e6, 2)
            df.at[idx, 'ν'] = round(MATERIALS[mat]['v'], 3)
    return df

def rows_to_members(df):
    members = []
    for _, row in df.iterrows():
        t_in = row.get('t [in]')
        mat = row.get('Material')
        if pd.notna(t_in) and pd.notna(mat):
            try:
                members.append(Member(thickness=t_in, material=mat))
            except Exception as e:
                st.error(f"Error creating Member: {e}")
    return members

def create_joint(bolt, members, washers=None, clearance='Normal'):
    if bolt and len(members) > 1:
        try:
            st.session_state.joint_instance = BoltedJoint(bolt=bolt, members=members, clearance_hole=CLEARANCE_HOLES[bolt][clearance.lower()],  washers=washers, preload=0)
        except Exception as e:
            st.error(f"Error creating BoltedJoint: {e}")
            print(e)
    else:
        st.session_state.joint_instance = None

# ======== Streamlit App ========
st.set_page_config(page_title="Bolted Joint Analyzer", layout="wide")
st.title("Bolted Joint Analyzer")
st.subheader("Fastener Parameters")

col1, col2 = st.columns([1, 2])

with col1:
    joint_type = st.selectbox('Bolt Type', options=['Tapped Hole', 'Bolted Joint'], key='joint_type', index=1)
    bolt = st.selectbox('Bolt Size', options=BOLT_SIZES, index=0, placeholder='Select bolt size', on_change=create_bolt_instance)

    if joint_type == 'Bolted Joint':
        clearance = st.selectbox('Clearance Hole Dia.', options=['Loose', 'Normal', 'Tight','Custom'])
        if clearance == 'Custom':
            st.number_input(label='Hole Dia. [in]', min_value = BOLT_SIZES[bolt]['d'])
        else:
            st.write(f"Hole Diameter: {CLEARANCE_HOLES[bolt][clearance.lower()]:.3f} in")

    tpi = st.selectbox('TPI', options=BOLT_SIZES[bolt]['tpi'], index=0, placeholder='Select TPI', on_change=create_bolt_instance)
    material = st.selectbox('Bolt Material', options=list(MATERIALS.keys()), index=0, placeholder='Select material', on_change=create_bolt_instance)

    st.button('Create Bolt', on_click=create_bolt_instance)

    st.subheader('Member Parameters')

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

    st.dataframe(updated_df, use_container_width=True, hide_index=True)

    st.button('Create Joint', on_click=create_joint, args=(st.session_state.get('bolt_instance'), rows_to_members(updated_df), None))
    if 'bolt_instance' in st.session_state and st.session_state.bolt_instance:
        st.write(st.session_state.bolt_instance.__repr__())
    
    if 'joint_instance' in st.session_state and st.session_state.joint_instance:
        st.write(st.session_state.joint_instance.__repr__() if 'joint_instance' in st.session_state and st.session_state.joint_instance else "No joint created yet.")

with col2:
    st.subheader("Bolt Visualization")
    if 'joint_instance' in st.session_state and st.session_state.joint_instance:
        with _Lock:
            fig, ax = plot_bolted_joint(
                st.session_state.joint_instance
            )
            st.pyplot(fig, use_container_width=True)
    else:
        st.info("Create a bolt and joint to see the visualization.")
