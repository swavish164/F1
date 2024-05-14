import numpy as np
import pandas as pd
import fastf1
import matplotlib.pyplot as plt
import streamlit as st
import fastf1.plotting
from AllDrivers import *
from Teams import *
confirmedYear = False
fastf1.plotting.setup_mpl(misc_mpl_mods=False)
st.set_option('deprecation.showPyplotGlobalUse', False)
def main():
    years = [2015, 2016, 2017, 2018, 2019,2020, 2021, 2022, 2023, 2024]
    selected_year = st.selectbox("Select a year:", years,key = "year")
    confirmedYear = st.button("ConfirmYear")
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
    #try:
    session.load()
    modes = ["All drivers","Team","Driver"]
    selected_mode = st.selectbox("Select what mode:",modes)
        #confirmedMode = st.button("ConfirmMode")
        #st.write("Mode Selected: ",selected_mode)
    options = ["Tyres Used","Fastest Laps"]
    if(selected_mode == "All drivers"):
        match selected_session:
            case("Race" | "Sprint"):
                options += ["Position Changes","Pit Stop Times","Race History"]
            case("Practice 1" | "Practice 2" | "Practice 3"):
                options.append("F")
        selected_options = st.selectbox("Select an option: ",options)
        print("Selected Year: "+str(selected_year)+" Selected Race: "+selected_race+" Selected Session: "+selected_session)
        fig = allDrivers(session,selected_options)
        st.pyplot(fig)
    elif(selected_mode == "Team"):
        match selected_session:
            case("Race" | "Sprint"):
                options += ["Pit Stop Times"]
        teams = pd.unique(session.laps['Team'])
        selected_teams = st.selectbox("Select a team: ",list(teams) + ['All'])
        if(selected_teams == 'All'):
            selected_optionsTeams = st.selectbox("Select an option for teams: ",options)
            fig = teams(session,selected_optionsTeams)
            st.pyplot(fig)
        #st.write("Team Selected: ",selected_teams)
            
    else:
        drivers = pd.unique(session.laps['Driver'])
        selected_driver = st.selectbox("Select a driver: ",drivers)
        compare = st.checkbox("Compare to other driver")
        if(compare):
            selected_second_driver = st.selectbox("Select a second driver: ",drivers)
            if(selected_driver == selected_second_driver):
                st.write("Can't be the same driver")
            else:
                selected_options = st.selectbox("Select an option: ",options)
        else:
            selected_options = st.selectbox("Select an option: ",options)

        #st.write("Driver Selected: ",selected_driver)


    #except:
        #st.write("Select a race that has happened")
            



if __name__ == "__main__":
    main()

