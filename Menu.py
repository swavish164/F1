import numpy as np
import pandas as pd
import fastf1
import matplotlib.pyplot as plt
import streamlit as st
def get_race_schedule(year):
    return fastf1.get_event_schedule(year)
def main():
    years = [2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019,2020, 2021, 2022, 2023, 2024]
    selected_year = st.selectbox("Select a year:", years,key = "year")
    #confirmedYear = st.button("ConfirmYear")
    #st.write("Year selected:", selected_year)
    # Perform further actions here
    eventNames = []
    season = fastf1.get_event_schedule(selected_year)
    if(selected_year == 2020):
        nonTesting = 2
    else:
        nonTesting = 1
    for i in range (nonTesting,len(season)-int(nonTesting/2)):
        events = season.get_event_by_round(i)
        number = 1
        for event in events:
            if(number < 6):
                number+=1
            else:
                eventNames.append(event)
                break


    selected_race = st.selectbox("Select a race:",eventNames,key = "race")
    #confirmedRace = st.button("ConfirmRace")
    #st.write("Race Selected: ",selected_race)
    event = season.get_event_by_name(selected_race)
    sessionNames = []
    for i in range(1,int((len(event)-8)/3) + 1):
        sessionNames.append(event.get_session_name(i))
    selected_session = st.selectbox("Select a session: ",sessionNames)
    #confirmedSession = st.button("ConfirmSession")
    #st.write("Session Selected: ",selected_session)
    session = event.get_session(selected_session)
    session.load()
    modes = ["All drivers","Team","Driver"]
    selected_mode = st.selectbox("Select what mode:",modes)
    #confirmedMode = st.button("ConfirmMode")
    #st.write("Mode Selected: ",selected_mode)
    if(selected_mode == "All drivers"):
        st.write("All drivers")
    elif(selected_mode == "Team"):
        teams = pd.unique(session.laps['Team'])
        selected_teams = st.selectbox("Select a team: ",teams)
        #st.write("Team Selected: ",selected_teams)
            
    else:
        drivers = pd.unique(session.laps['Driver'])
        selected_driver = st.selectbox("Select a driver: ",drivers)
        #st.write("Driver Selected: ",selected_driver)


            



if __name__ == "__main__":
    main()

