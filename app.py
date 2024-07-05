import streamlit as st
import garminconnect
import pandas as pd
import numpy as np
import os
from datetime import date, timedelta

st.title("Analyze Garmin Data")
LOGGED_IN=False
#email = input("Enter email address: ")
email = st.text_input("Enter email address: ")
#password = getpass("Enter password: ")
password = st.text_input("Enter a password", type="password")
#st.write(type(email))
#st.write(type(password))


if st.button("Authenticate"):
    garmin = garminconnect.Garmin(email, password)
    try:
        a=garmin.login()
        st.write(a)
    except:
        st.write("Login failed")
        st.stop()
    st.write(garmin.display_name)
    GARTH_HOME = os.getenv("GARTH_HOME", "~/.garth")
    garmin.garth.dump(GARTH_HOME)
    
    yesterday = date.today() - timedelta(days=1)
    yesterday = yesterday.isoformat()

    start= date.today() - timedelta(days=21)
    start = start.isoformat()
    dailysteps=garmin.get_daily_steps(start=start,end=yesterday)
    dailyStepsDF=pd.DataFrame(dailysteps)
    st.dataframe(dailyStepsDF.style.highlight_max(axis=0))
    st.line_chart(dailyStepsDF['totalSteps'], width=0, height=0, use_container_width=True)
    st.line_chart(dailyStepsDF['totalDistance'], width=0, height=0, use_container_width=True)
