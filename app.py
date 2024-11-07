import streamlit as st
import numpy as np
import pandas as pd
import datetime
from datetime import time
import joblib

sleep_efficiency = 0

st.title("Sleep Efficiency Predictor")

with st.form("Sleep Efficiency"):
    st.subheader("Name")
    name = st.text_input('Enter your name:', max_chars = 25)
    
    st.subheader('Age')
    age = st.number_input('Enter your age:', max_value=100, min_value=1)

    st.subheader('Gender')
    gender = st.radio('Select your gender:',options=('Male','Female'), horizontal=True)

    st.subheader('Bedtime')
    bedtime = st.time_input("Select at what time do you sleep at night", value=time(12, 0))

    st.subheader('Wakeup Time')
    wakeup = st.time_input("Select at what time do you wakeup in the morning", value=time(12, 0))

    st.subheader('Sleep Duration')
    sleep_duration = st.number_input('Enter the approximate number of hours you slept:', min_value=0)
    
    # REM Sleep Percentage
    st.subheader("REM Sleep Percentage")
    rem_sleep = st.slider("Enter your REM sleep percentage:", 0, 100, 20)
    
    # Deep Sleep Percentage
    st.subheader("Deep Sleep Percentage")
    deep_sleep = st.slider("Enter your deep sleep percentage:", 0, 100, 20)
    st.caption("Deep sleep is important for physical recovery and health. Typically, it comprises 15% - 20% of total sleep time.")
    
    # Light Sleep Percentage
    st.subheader("Light Sleep Percentage")
    light_sleep = st.slider("Enter your light sleep percentage:", 0, 100, 50)
    st.caption("Light sleep helps in mental and physical recovery, and takes up a majority of total sleep time.")
    
    # Awakenings
    st.subheader("Awakenings")
    awakenings = st.number_input("Number of times you wake up during the night:", min_value=0, max_value=20, value=2)
    st.caption("Frequent awakenings may affect sleep quality. Most people experience 1-3 awakenings per night.")
    
    # Caffeine Consumption
    st.subheader("Caffeine Consumption")
    caffeine = st.slider("Cups of caffeine consumed per day:", 0, 10, 1)
    st.caption("High caffeine intake, especially in the evening, can disrupt sleep. Try to limit it to morning hours if possible.")
    
    # Alcohol Consumption
    st.subheader("Alcohol Consumption")
    alcohol = st.slider("Alcohol consumption (drinks per day):", 0, 10, 0)
    st.caption("While alcohol may make you sleepy, it can disrupt sleep cycles. Moderation is recommended.")
    
    # Exercise Frequency
    st.subheader("Exercise Frequency")
    exercise = st.slider("Exercise frequency (times per week):", 0, 7, 3)
    st.caption("Regular exercise improves sleep quality. The recommended frequency is around 3-5 times per week.")
    
    # Smoker
    st.subheader("Smoking Status")
    smoker = st.radio("Do you smoke?", options=["Yes", "No"])
    st.caption("Smoking negatively impacts sleep quality due to the stimulant effect of nicotine.")
    
    # Submit Button
    submit_button = st.form_submit_button(
        label="Submit",
        help="Submit your form after entering all details"
    )

    
    if(submit_button):
        
        gender_details = {'Male':1, 'Female':0}
        
        smoking = {'Yes':1, 'No':0}
        
        df = pd.DataFrame({'bedtime': [bedtime], 'wakeup': [wakeup]})
        df['bedtime'] = df['bedtime'].apply(lambda t: datetime.datetime.combine(datetime.date(2000, 1, 1), t))
        df['wakeup'] = df['wakeup'].apply(lambda t: datetime.datetime.combine(datetime.date(2000, 1, 1), t))
        df['bedtime_normalized'] = (df['bedtime'].dt.hour + df['bedtime'].dt.minute / 60) / 24
        df['wakeup_normalized'] = (df['wakeup'].dt.hour + df['wakeup'].dt.minute / 60) / 24
        df.drop(columns=['bedtime', 'wakeup'], inplace=True)
        bedtime = df['bedtime_normalized'].iloc[0]
        wakeup = df['wakeup_normalized'].iloc[0]

        input_data = np.array([
        age,
        sleep_duration,
        rem_sleep,
        deep_sleep,
        light_sleep,
        awakenings,
        caffeine,
        alcohol,
        exercise,
        smoking[smoker],
        gender_details[gender],
        bedtime,
        wakeup
        ]).reshape(1, -1) 

        # Loading the model
        import pickle
        pickle_in = open("model.pkl", "rb")
        model = pickle.load(pickle_in)
        sleep_efficiency = model.predict(input_data) * 100

        st.markdown("## *Sleep Efficiency Prediction*")
        st.markdown("###### Based on the data entered, the model predictions on your sleep quality are as follows:")

        st.markdown("#### Sleep efficiency in percentage:")
        st.text(f"{sleep_efficiency[0]} %")

        st.markdown("#### Sleep quality:")
        if(sleep_efficiency[0]>=0 and sleep_efficiency[0]<=25):
            st.text("Very bad :(")
            st.caption("Your sleep quality is significantly below optimal. Consider improving your sleep habits to avoid fatigue and health issues. A consistent sleep routine could make a big difference.")
        elif(sleep_efficiency[0]>25 and sleep_efficiency[0]<=50):
            st.text("Average :/")
            st.caption("You're getting an average night’s sleep. There’s room for improvement to feel more rested and energized throughout the day. Small adjustments, like optimizing your sleep environment, could help.")
        elif(sleep_efficiency[0]>50 and sleep_efficiency[0]<=75):
            st.text("Good :)")
            st.caption("Your sleep quality is good, but there’s always room for improvement! Keeping a consistent schedule and making minor lifestyle tweaks could help you achieve even better rest.")
        elif(sleep_efficiency[0]>75 and sleep_efficiency[0]<90):
            st.text("Very Good!")
            st.caption("Your sleep quality is very good, just a step away from excellent! With a few more tweaks to your routine, you can reach your peak sleep potential.")
        else:
            st.text("Impressive!")
            st.caption("Great job! Your sleep quality is excellent. You're on track for optimal rest and recovery. Keep up the good work to maintain your health and energy levels!")

        st.markdown("#### Comparing your routine with the recommended routine:")
        data = {
    'Parameter': ['Sleep_duration',
                  'REM sleep %','Deep sleep %' ,'Light sleep %' ,'Awakenings','Caffeine Intake','Alcohol Consumption (No. of drinks)','Exercise Count','Smoking(Y/N)'],
        'Your Data': [sleep_duration, rem_sleep, deep_sleep, light_sleep, awakenings, caffeine, alcohol, exercise, smoker],
    'Recommended Values': ['7-8 hours','Close to 30%', '>50%', '<25%', '<=1', '0 or none', '0 or none', '4-5', 'No']
}
        df = pd.DataFrame(data)
        st.dataframe(df)

        st.markdown("#### Recommendations for improvements:")
        if(sleep_duration<6):
            st.markdown("- Prioritize improving sleep duration. \n- Aim for at least 7-8 hours of sleep per night for optimal health. \n- Ensure a relaxing pre-sleep routine\n(e.g., reduce screen time, engage in calming activities).\n- Manage stress levels and consider sleep hygiene practices (e.g., a consistent bedtime, comfortable sleep environment).")
        elif(sleep_duration>8):
            st.markdown("- While longer sleep can be beneficial, ensure it’s quality sleep.\n- If experiencing excessive daytime sleepiness despite long sleep, evaluate for potential underlying health conditions.\n- Keep a regular sleep schedule, as oversleeping can sometimes be linked to poorer health outcomes.")

        if (alcohol>=3):
            st.markdown("- Reduce alcohol intake, as high consumption can disrupt sleep cycles and decrease sleep quality.\n- Aim for alcohol-free nights, especially before bedtime, to allow for better restorative sleep.\n- Consider seeking support for alcohol reduction or cessation if it becomes a habit.")
        
        if(exercise<2):
            st.markdown("- Increase physical activity to at least 3-4 times a week.\n- Regular exercise can improve sleep quality and duration by reducing stress and promoting relaxation.\n- Engage in moderate-intensity activities like walking, cycling, or swimming, which are known to enhance sleep.")
        elif(exercise>=3):
            st.markdown("- Ensure exercise is not too close to bedtime, as vigorous physical activity can sometimes interfere with sleep onset.\n- Maintain a balanced routine with proper rest days to avoid overtraining, which can negatively impact sleep quality.")

        if(smoker=='Yes'):
            st.markdown("- Smoking, especially close to bedtime, can significantly reduce sleep quality due to nicotine's stimulating effects.\n- Aim to quit smoking for both long-term health and improved sleep quality.")
        else:
            st.markdown("- Continue to foster a healthy sleep environment and habits to support optimal rest.")

        if(caffeine>=2):
            st.markdown("- Limit caffeine intake, particularly in the afternoon or evening, as it can disrupt sleep patterns.\n- Aim for no caffeine at least 6 hours before bedtime to minimize sleep disturbances.")
        else:
            st.markdown("- Continue with low or moderate caffeine consumption, but be mindful of other sources of stimulants (e.g., energy drinks, chocolate).\n- If you still experience sleep issues, evaluate other factors such as stress or environmental conditions")



        st.title("Thank You!")
st.write("Thank you for using our service. We appreciate your time and hope you had a great experience!")

            

        
        
        
        


                
        

        
        
        
        