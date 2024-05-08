import numpy as np
import pandas as pd
import fastf1
import matplotlib.pyplot as plt
import shiny
from shiny import reactive
from shiny.express import input, render, ui
import streamlit as st

def main():
    years = [2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]
    selected_year = st.selectbox("Select a year:", years)
    confirmed = st.button("Confirm")
    
    if confirmed:
        st.write("Year selected:", selected_year)
        # Perform further actions here

if __name__ == "__main__":
    main()
