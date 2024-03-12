import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
from scipy.stats import binom, t

# Read the CSV statistics
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
                   initial_sidebar_state="expanded")

# Sidebar to switch between sections
selected_section = st.sidebar.selectbox("Select Section", ["Statistics", "Random 100 People", "Women Social Media Less Than 2 Hours", "Z-Score Social Media Less Than 3 Hours", "Social Media Over 5 Hours", "Margin of Error and Confidence Interval", "Compare Social Media Use Between Sex and Age"])

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
    
    # Calculate the number of people whose time spent is less than the mean
    num_for_p = len(random_sample[random_sample['time_spent'] < mean_time_spent])
    
    # Total number of people in the sample
    total_people = len(random_sample)
    
    # Calculate the probability p
    p = num_for_p / total_people
    
    # Calculate the number of trials (n)
    n = 100
    
    # Calculate the mean of the binomial distribution
    mean = n * p
    
    # Calculate the standard deviation of the binomial distribution
    std_dev = np.sqrt(n * p * (1 - p))
    
    # Find the probability of a random variable exceeding its mean
    prob_greater_than_mean = 1 - binom.cdf(mean, n, p)
    
    st.write(f"💡 Mean of the Binomial distribution: {mean:.2f}")
    st.write(f"💡 Standard deviation of the Binomial distribution: {std_dev:.2f}")
    st.write(f"💡 Probability of a random variable exceeding its mean: {prob_greater_than_mean:.2f}")

    # Display the random sample
    st.write("👇 Randomly Selected 100 People:")
    st.write(random_sample)
    
elif selected_section == "Women Social Media Less Than 2 Hours":
    st.header('❤️ Women Social Media Usage - Less Than 2 Hours')

    # Filter the dataset to include only women
    women_data = df[df['gender'] == 'female']

    # Calculate the number of women whose time spent is less than 2 hours
    num_less_than_2_hours = len(women_data[women_data['time_spent'] < 2])

    # Total number of women in the dataset
    total_women = len(women_data)

    # Calculate the probability p
    p = num_less_than_2_hours / total_women

    # Calculate the mean and variance of the binomial distribution
    mean, var = binom.stats(1000, p)

    # Generate the probability distribution function
    x = np.arange(0, 1000+1)
    distribution = [binom.pmf(r, 1000, p) for r in x]

    st.write(f"💡 Mean of the Binomial distribution for the sample: {mean:.2f}")
    st.write(f"💡 Variance of the Binomial distribution for the sample: {var:.2f}")

    # Plot the probability mass function
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(x, distribution, marker='o', linestyle='-')
    ax.set_title('Probability Mass Function of Binomial Distribution')
    ax.set_xlabel('Number of Women Using Social Media Less Than 2 Hours')
    ax.set_ylabel('Probability')
    st.pyplot(fig)

elif selected_section == "Z-Score Social Media Less Than 3 Hours":
    st.header('❤️ Social Media Usage - Less Than 3 Hours')

    # Filter the dataset to include only individuals who spend less than 3 hours on social media
    less_than_3_hours_data = df[df['time_spent'] < 3]

    # Calculate the number of individuals spending less than 3 hours on social media
    num_less_than_3_hours = len(less_than_3_hours_data)

    # Calculate the total number of individuals
    total_individuals = len(df)

    # Population parameters
    population_mean = df['time_spent'].mean()
    population_std_dev = df['time_spent'].std()

    # Define the threshold value
    threshold = 3

    # Calculate the z-score using population parameters
    z_score = (threshold - population_mean) / population_std_dev

    # Calculate the probability using the z-score
    probability_less_than_3_hours = stats.norm.cdf(z_score)

    st.write(f"💡 Population Mean: {population_mean:.2f}")
    st.write(f"💡 Population Standard Deviation: {population_std_dev:.2f}")
    st.write(f"💡 Z-score: {z_score:.2f}")
    st.write(f"💡 Probability of Spending Less Than 3 Hours on Social Media: {probability_less_than_3_hours:.2%}")



elif selected_section == "Social Media Over 5 Hours":
    st.header('❤️ Social Media Usage - Over 5 Hours')

    # Randomly select 100 people
    random_sample_100 = df.sample(n=100, random_state=42)

    # Count the number of individuals spending over 5 hours on social media in the random sample
    num_social_media_over_5_hours_sample = len(random_sample_100[random_sample_100['time_spent'] > 5])

    # Calculate the probability of people using social media for over 5 hours in the random sample
    probability_over_5_hours_sample = num_social_media_over_5_hours_sample / 100

    # Count the number of individuals spending over 5 hours on social media in the entire dataset
    num_social_media_over_5_hours = len(df[df['time_spent'] > 5])

    # Total number of individuals in the dataset
    total_individuals = len(df)

    # Calculate the overall probability of people using social media for over 5 hours
    probability_over_5_hours = num_social_media_over_5_hours / total_individuals

    st.write("👇 Randomly Selected 100 People:")
    st.write(random_sample_100)

    st.write(f"💡 Number of People Using Social Media for Over 5 Hours (Random Sample): {num_social_media_over_5_hours_sample}")
    st.write(f"💡 Probability of People Using Social Media for Over 5 Hours (Random Sample): {probability_over_5_hours_sample:.2%}")

    st.write(f"💡 Number of People Using Social Media for Over 5 Hours (Overall): {num_social_media_over_5_hours}")
    st.write(f"💡 Probability of People Using Social Media for Over 5 Hours (Overall): {probability_over_5_hours:.2%}")

elif selected_section == "Margin of Error and Confidence Interval":
    st.header('❤️ Margin of Error and Confidence Interval')

    # Randomly select 500 people
    random_sample = df.sample(n=500, random_state=42)

    # Display CSV data
    st.write("👇 Randomly Selected 500 People:")
    st.write(random_sample)

    # Calculate Margin of Error and Confidence Interval
    confidence_level = 0.9999  # 99.99% confidence level
    standard_error = std_dev_time_spent / np.sqrt(500)  # Assuming a population size of 500
    t_value = t.ppf((1 + confidence_level) / 2, df=499)  # Degrees of freedom = n - 1

    margin_of_error = t_value * standard_error
    moe_percent = (margin_of_error / mean_time_spent) * 100
    lower_ci = mean_time_spent - margin_of_error
    upper_ci = mean_time_spent + margin_of_error

    st.write(f"💡 Margin of Error: {moe_percent:.2f}%")
    st.write(f"💡 Confidence Interval: [{lower_ci:.2f}, {upper_ci:.2f}]")
    st.write("💡 Because of Sample Pool is so small so MOE will rise ")

elif selected_section == "Compare Social Media Use Between Sex and Age":
    st.header('❤️ Compare Social Media Use Between Sex and Age')

    # Define the age groups
    age_groups = pd.cut(df['age'], bins=np.arange(18, 66, 5), right=False)

    # Group data by gender and age
    grouped_data = df.groupby(['gender', age_groups])

    # Calculate the average time spent for each group
    avg_time_spent = grouped_data['time_spent'].mean().reset_index()

    # Pivot the data to have gender as columns and age groups as rows
    pivot_data = avg_time_spent.pivot(index='age', columns='gender', values='time_spent')

    # Plot a bar chart to visualize the comparison
    fig, ax = plt.subplots(figsize=(10, 6))
    pivot_data.plot(kind='bar', ax=ax, color=['Pink', 'SkyBlue','#FF968A'])
    ax.set_title('Average Time Spent Comparison - Social Media Use Between Men and Women and Age')
    ax.set_ylabel('Average Time Spent')
    ax.set_xlabel('Age Group')
    ax.legend(title='Gender')

    # Set monospace font
    plt.rcParams['font.family'] = 'monospace'

    # Display the plot
    st.pyplot(fig)
    st.write("💡 From the graph above you can see women and non-binary are using Social Media more than men arn group of 18-23 and 38-43 are using Social Media most.")
