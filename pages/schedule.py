import streamlit as st
import pandas as pd
import datetime

from itertools import combinations

st.write("# Speedback session")

# Initialize the teams dict
if 'teams' not in st.session_state:
    teams = {}
    teams['default_team'] = ['name1', 'name2', 'name3']
    st.session_state['teams'] = teams

if 'names' not in st.session_state:
    names = []
    st.session_state['names'] = names

teams = st.session_state['teams']

st.write("## Planning")
selected_team = st.selectbox(
    'Which team are you planning for?',
    teams.keys())

st.write('You selected:', selected_team)
st.write('Your team has', len(teams[selected_team]), 'members')

st.write("## Table planning")

def generate_sessions(people: list, excl=[]):
    # all the pairings you need are all possible pairings, except the exclusions
    needed_pairings = [set(pair) for pair in combinations(people, 2)]
    
    for pair in excl:
        needed_pairings.remove(pair)

    # while there pairing that haven't happened yet
    while needed_pairings:
        # each session starts empty
        session = []
        # keep track of all people still available for this session
        available = set(people)
        # create an iterator, so we can loop over the needed pairings
        iter_needed_pairings = iter(needed_pairings)
        # as long as there are more than 2 people still waiting and there's a pair left in the needed pairings
        while (len(available) > 1) and (pair := next(iter_needed_pairings, False)):
            # are both people in the pair in the group of available people?
            if available.intersection(pair) == pair:
                # then they can meet in this session
                session.append(pair)
                # and they're no longer available
                available -= pair
        # once we have a session, remove the pairs in it from the pairings still needed
        for pair in session:
            needed_pairings.remove(pair)
        # yield the session
        yield session


sessions = list(generate_sessions(people=teams[selected_team]))
st.session_state[sessions] = sessions

for i in range(len(sessions)):
    st.write("Session", i+1)
    tables = [table+1 for table in range(0,len(sessions[i]))]
    names_1 = []
    names_2 = []
    for j in range(len(sessions[i])):
        names_1.append(list(sessions[i][j])[0])
        names_2.append(list(sessions[i][j])[1])

    df = pd.DataFrame({
        'Tables': [j+1 for j in range(len(sessions[i]))],
        'Person 1': names_1,
        'Person 2': names_2,
    })
    st.table(df)

st.write("## Time planning")
sessions_before_break = st.slider(
    "How many sessions do you do before a break?",
    value=3,
    min_value=1,
    max_value=10
)

break_duration = st.slider(
    "How long is the break [in minutes]?",
    value=5,
    min_value=0,
    max_value=30
)

session_start = st.time_input('When will the session start?', datetime.time(14, 15))
st.write('Session start at: ', session_start)

session_duration = st.slider(
    "How long will a session be [in minutes]?",
    value=5,
    min_value=0,
    max_value=10
)

def addSecs(tm, secs):
    fulldate = datetime.datetime(100, 1, 1, tm.hour, tm.minute, tm.second)
    fulldate = fulldate + datetime.timedelta(seconds=secs)
    return fulldate.time()

session_times = []
session_details = {}
session_details['session_name'] = 0
session_details['session_start'] = session_start
session_details['session_end'] = addSecs(session_start, session_duration*60)
session_times.append(session_details)

for i in range(1, len(sessions)):
    if i % sessions_before_break == 0:
        session_details = {}
        session_details['session_name'] = 'Break'
        session_details['session_start'] = session_times[-1]['session_end']
        session_details['session_end'] = addSecs(session_details['session_start'], break_duration*60)
        session_times.append(session_details)

        session_details = {}
        session_details['session_name'] = i
        session_details['session_start'] = session_times[-1]['session_end']
        session_details['session_end'] = addSecs(session_details['session_start'], session_duration*60)
        session_times.append(session_details)
    else:
        session_details = {}
        session_details['session_name'] = i
        session_details['session_start'] = session_times[-1]['session_end']
        session_details['session_end'] = addSecs(session_details['session_start'], session_duration*60)
        session_times.append(session_details)

st.write("## Timetable")
for i in range(len(session_times)):
    session_name = session_times[i]['session_name']
    if isinstance(session_name, int):
        st.write("### Session", session_name+1)
        st.write("Start:", session_times[i]['session_start'], "-", "End:", session_times[i]['session_end'])
        tables = [table+1 for table in range(0,len(sessions[session_name]))]
        names_1 = []
        names_2 = []
        for j in range(len(sessions[session_name])):
            names_1.append(list(sessions[session_name][j])[0])
            names_2.append(list(sessions[session_name][j])[1])

        df = pd.DataFrame({
            'Tables': [j+1 for j in range(len(sessions[session_name]))],
            'Person 1': names_1,
            'Person 2': names_2,
        })
        st.table(df)
    
    else:
        st.write("## " + session_name)
        st.write("Start:", session_times[i]['session_start'], "-", "End:", session_times[i]['session_end'])
      