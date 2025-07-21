import streamlit as st
import numpy as np
import json

DATA_DIR = r'data\sizes.json'

class Bolt:
    def __init__(self, size, d, tpi, A_t, A_m, thread_type='coarse'):
        self.size = size
        self.d = d
        self.tpi = tpi
        self.A_t = A_t
        self.A_m = A_m
        self.thread_type = thread_type

    def __repr__(self):
        return (f"Bolt(size={self.size}, nominal_diameter={self.d},"
                f"threads_per_inch={self.tpi}, tensile_stress_area={self.A_t}"
                f"minor_diameter={self.A_m}, thread_type={self.thread_type}")

def create_bolt(size, thread_type, mat):
    bolt_info = bolt_sizes[size]
    thread_info = bolt_info[thread_type]
    
    return Bolt(
        size=size,
        d=bolt_info["d"],
        tpi=thread_info["tpi"],
        A_t=thread_info["A_t"],
        A_m=thread_info["A_m"],
        thread_type=thread_type
    )

with open(DATA_DIR) as f:
    bolt_sizes = json.load(f)

col1, col2 = st.columns([1,3])

with col1:
    st.selectbox('Bolt Type', options=['Tapped Hole', 'Bolted Joint'], key='joint_type')
    st.selectbox('Bolt Size', options=bolt_sizes)
    st.write(st.session_state.joint_type)

with col2:
    st.write('col2')
