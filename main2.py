import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import t

# Read the CSV file
df = pd.read_csv('avgtimeuse.csv')

# Calculate statistics
mean_time_spent = df['time_spent'].mean()
median_time_spent = df['time_spent'].median()
std_dev_time_spent = df['time_spent'].std()
variation_time_spent = df['time_spent'].var()

# Page Config
st.set_page_config(page_title="Time Spent Tracker",
                   page_icon="⏳",
                   layout="wide",
                   initial_sidebar_state="expanded",
                   )

# Sidebar to switch between sections
selected_section = st.sidebar.selectbox("Select Section", ["Statistics", "Random 100 People", "Social Media Less Than 2 Hours", "Social Media 3-4 Hours", "Social Media Over 5 Hours", "Margin of Error and Confidence Interval", "Compare Men and Women"])

# Header
st.markdown("""
# Time Spent Tracker ⏳📊🕰️
This Web-App helps you analyze your average time spent with information such as a bar chart below.
""")

# Display selected section
if selected_section == "Statistics":
    st.header('❤️ Statistics')
    st.write(f"💡 Mean Time Spent: {mean_time_spent:.2f}")
    st.write(f"💡 Median Time Spent: {median_time_spent}")
    st.write(f"💡 Standard Deviation of Time Spent: {std_dev_time_spent:.2f}")
    st.write(f"💡 Variation of Time Spent: {variation_time_spent:.2f}")

    # Create a bar chart with custom colors
    fig, ax = plt.subplots(figsize=(8, 4))  # Adjust the size as needed
    bars = ax.bar(['Mean', 'Median', 'Std Dev', 'Variation'], [mean_time_spent, median_time_spent, std_dev_time_spent, variation_time_spent], color='#FF968A')
    ax.set_title('Time Spent Statistics')
    ax.set_ylabel('Time Spent')

    # Set monospace font
    plt.rcParams['font.family'] = 'monospace'

    # Display the plot
    st.pyplot(fig)
    st.write("💡 All data")
    st.write(df)

elif selected_section == "Random 100 People":
    st.header('❤️ Random 100 People')
    
    # Randomly select 100 people
    random_sample = df.sample(n=100, random_state=42)
    
    # Calculate the percentage of people whose time spent is greater than the mean
    passed_mean_percentage = (random_sample['time_spent'] > mean_time_spent).mean() * 100
    
    st.write(f"👇 Randomly Selected 100 People:")
    st.write(random_sample)
    st.write(f"💡 Percentage of People Whose Time Spent is Greater Than Mean: {passed_mean_percentage:.2f}%")

elif selected_section == "Social Media Less Than 2 Hours":
    st.header('❤️ Social Media Usage - Less Than 2 Hours')

    random_sample = df.sample(n=100, random_state=42)

    st.write("👇 Randomly Selected 100 People:")
    st.write(random_sample)

    # Calculate the expectation value (mean) for the selected sample
    expectation_value_less_than_2_hours = random_sample['time_spent'].mean()

    st.write(f"💡 Expectation Value (Mean) for Social Media Less Than 2 Hours: {expectation_value_less_than_2_hours:.2f} hours")

elif selected_section == "Social Media 3-4 Hours":
    st.header('❤️ Social Media Usage - 3 to 4 Hours')

    random_sample = df.sample(n=100, random_state=42)

    st.write("👇 Randomly Selected 100 People:")
    st.write(random_sample)

    social_media_3_4_hours = random_sample[(random_sample['time_spent'] >= 3) & (random_sample['time_spent'] <= 4)]
    num_social_media_3_4_hours = len(social_media_3_4_hours)

    total_people = len(random_sample)
    probability_3_4_hours = 1 - t.cdf(4, df=99, loc=mean_time_spent, scale=std_dev_time_spent)  # Assuming a normal distribution

    st.write(f"💡 Number of People Using Social Media for 3 to 4 Hours: {num_social_media_3_4_hours}")
    st.write(f"💡 Probability of People Using Social Media for 3 to 4 Hours: {probability_3_4_hours:.2%}")



elif selected_section == "Social Media Over 5 Hours":
    st.header('❤️ Social Media Usage - Over 5 Hours')

    random_sample_100 = df.sample(n=100, random_state=42)

    st.write("👇 Randomly Selected 100 People:")
    st.write(random_sample_100)

    social_media_over_5_hours = random_sample_100[random_sample_100['time_spent'] > 5]
    num_social_media_over_5_hours = len(social_media_over_5_hours)

    total_people_100 = len(random_sample_100)
    probability_over_5_hours = 1 - t.cdf(5, df=99, loc=mean_time_spent, scale=std_dev_time_spent)  # Assuming a normal distribution

    st.write(f"💡 Number of People Using Social Media for Over 5 Hours: {num_social_media_over_5_hours}")
    st.write(f"💡 Probability of People Using Social Media for Over 5 Hours: {probability_over_5_hours:.2%}")


elif selected_section == "Margin of Error and Confidence Interval":
    st.header('❤️ Margin of Error and Confidence Interval')

    # Randomly select 100 people
    random_sample = df.sample(n=100, random_state=42)

    # Display CSV data
    st.write("👇 Randomly Selected 100 People:")
    st.write(random_sample)

    # Calculate Margin of Error and Confidence Interval
    confidence_level = 0.95
    standard_error = std_dev_time_spent / np.sqrt(100)  # Assuming a population size of 100
    t_value = t.ppf((1 + confidence_level) / 2, df=99)  # Degrees of freedom = n - 1

    margin_of_error = t_value * standard_error
    lower_ci = mean_time_spent - margin_of_error
    upper_ci = mean_time_spent + margin_of_error

    st.write(f"💡 Margin of Error: {margin_of_error:.2f}")
    st.write(f"💡 Confidence Interval: [{lower_ci:.2f}, {upper_ci:.2f}]")

elif selected_section == "Compare Men and Women":
    st.header('❤️ Compare Men and Women - Average Time Spent')

    # Filter data for men and women
    men_data = df[df['gender'] == 'male']
    women_data = df[df['gender'] == 'female']

    # Calculate the average time spent for men and women
    avg_time_spent_men = men_data['time_spent'].mean()
    avg_time_spent_women = women_data['time_spent'].mean()

    st.write(f"💡 Average Time Spent for Men: {avg_time_spent_men:.2f} hours")
    st.write(f"💡 Average Time Spent for Women: {avg_time_spent_women:.2f} hours")

    # Plot a bar chart to visualize the comparison
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(['Men', 'Women'], [avg_time_spent_men, avg_time_spent_women], color='#FF968A')
    ax.set_title('Average Time Spent Comparison - Men vs Women')
    ax.set_ylabel('Average Time Spent')

    # Set monospace font
    plt.rcParams['font.family'] = 'monospace'

    # Display the plot
    st.pyplot(fig)
