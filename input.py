import streamlit as st
import pandas as pd

st.write("# Speedback session")

# Helper functions
def delete_last(names):
    del names[-1]
    st.session_state['names'] = names

def delete_all(names):
    st.session_state['names'] = []

def add_team_to_list(teams, team_name, names):
    teams[team_name] = names
    st.session_state['teams'] = teams

# Initialize the teams dict
if 'teams' not in st.session_state:
    teams = {}
    teams['default_team'] = ['name1', 'name2', 'name3']
    st.session_state['teams'] = teams

if 'names' not in st.session_state:
    names = []
    st.session_state['names'] = names

st.write("## Create a team")

st.write("### Input the names of your team members below:")
names = st.session_state["names"]
name = st.text_input('Team member name', '')
if st.button("add"):
    names.append(name)
    st.session_state['names'] = names

st.write("### These are your team members")
st.write(names)

st.button("Delete last", on_click=delete_last, args=[names])
st.button("Delete all", on_click=delete_all, args=[names])

st.write("Give your team a name")
teams = st.session_state['teams']
team_name = st.text_input('Team name', '')

st.button("Add team to list", on_click=add_team_to_list, args=[teams, team_name, names])
st.write(teams)
