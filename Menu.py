import numpy as np
import pandas as pd
import fastf1
import matplotlib.pyplot as plt
import streamlit as st

def main():
    years = [2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]
    selected_year = st.selectbox("Select a year:", years)
    confirmedYear = st.button("ConfirmYear")
    
    if confirmedYear:
        st.write("Year selected:", selected_year)
        # Perform further actions here
        selected_race = st.selectbox("Select a race:",["Miami","China"])
        confirmedRace = st.button("ConfirmRace")
        if(confirmedRace):
            st.write("Race Selected: ",selected_race)


if __name__ == "__main__":
    main()

