import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set_theme(style='dark')

cleaned_day_df = pd.read_csv("cleaned_day_df.csv")

# convert the 'dteday' column to datetime
cleaned_day_df["dteday"] = pd.to_datetime(cleaned_day_df["dteday"])

# Get the minimum and maximum dates
min_date = cleaned_day_df["dteday"].min()
max_date = cleaned_day_df["dteday"].max()

# Ensure a valid initial value range
initial_start_date = min_date
initial_end_date = max_date

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    
    # Mengambil start_date & end_date dari date_input
    date_range = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[initial_start_date, initial_end_date]
    )

if len(date_range) == 2:
    start_date, end_date = date_range
    
    main_df = cleaned_day_df[(cleaned_day_df["dteday"] >= str(start_date)) & 
                (cleaned_day_df["dteday"] <= str(end_date))]

    # Calculate the total rentals for summer and winter
    summer_rentals = main_df[main_df['season'] == 3]['cnt'].sum()
    winter_rentals = main_df[main_df['season'] == 1]['cnt'].sum()

    # Create a bar chart
    plt.figure(figsize=(8, 6))
    plt.bar(['Summer', 'Winter'], [summer_rentals, winter_rentals], color=['skyblue', 'lightcoral'])
    plt.title('Total Bike Rentals in Summer vs. Winter')
    plt.ylabel('Total Rentals')
    plt.xlabel('Season')
    plt.show()

    # Calculate the percentage change
    percentage_change = ((summer_rentals - winter_rentals) / winter_rentals) * 100
    print(f"Percentage change in rentals between summer and winter: {percentage_change:.2f}%")

    st.subheader("Total Bike Rentals in Summer vs Winter")
    st.pyplot(plt)

    st.write("Percentage Change in Rentals between Summer and Winter" + ": " + f"{percentage_change:.0f}%")

    # Create a boxplot to compare bike rentals on weekdays vs. weekends
    plt.figure(figsize=(8, 6))
    sns.boxplot(x='workingday', y='cnt', data=main_df)
    plt.title('Bike Rentals on Weekdays vs. Weekends')
    plt.xlabel('Working Day (0: Weekend, 1: Weekday)')
    plt.ylabel('Total Rentals')
    plt.show()

    # Calculate the average rentals for weekdays and weekends
    weekday_avg = main_df[main_df['workingday'] == 1]['cnt'].mean()
    weekend_avg = main_df[main_df['workingday'] == 0]['cnt'].mean()

    st.subheader("Average Bike Rentals on Weekdays vs Weekends")
    st.pyplot(plt)

    st.write(f"Average bike rentals on weekdays: {weekday_avg:.0f}")
    st.write(f"Average bike rentals on weekends: {weekend_avg:.0f}")

    def manual_clustering(cnt):
        if cnt < 2000:
            return 1
        elif 2000 <= cnt < 4000:
            return 2
        else:
            return 3

    main_df['cluster'] = main_df['cnt'].apply(manual_clustering)
    main_df['temp'] = (main_df['temp'] * 41) - 8

    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='temp', y='cnt', hue='cluster', data=main_df, palette="viridis", s=50)
    plt.title("Manual Clustering of Bike Rentals")
    plt.xlabel("Temperature in Celcius")
    plt.ylabel("Count of Rentals in a Day")
    plt.show()

    st.subheader("Manual Clustering of Bike Rentals")
    st.pyplot(plt)
else:
    # Show Loading when no date range length is not 2
    st.write("Loading...")