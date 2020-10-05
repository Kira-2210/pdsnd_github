import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("Please let me know which city´s data you´re interested to explore!\n" \
        "Enter Chicago, New York City or Washington:\n")
        if city.lower() not in ("washington", "new york city", "chicago"):
            print("Ooops. You entered a city which data is not available for or made a " \
            "typo in the city name. \nPlease start again.\n")
        else:
            print("Got it!\n")
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("Now choose the month you want to know more about.\n" \
        "Enter a month from January to June. If you don´t want to filter for a month, enter all:\n")
        if month.lower() not in ("january", "february", "march", "april", "may", "june", "all"):
            print("Ooops. This month is not available. Please try again.\n")
        else:
            print("Got it!\n")
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Now you can choose if you´re interested in data from a specific day of the week.\n" \
        "Enter the day of the week, if you don´t want to filter for a day, enter all:\n")
        if day.lower() not in ("monday", "tuesday", "wednesday", "thursday",
        "friday", "saturday", "sunday", "all"):
            print("Ooops. Looks like you made a typo when entering the day of the week. " \
            "Please try again.\n")
        else:
            print("Thanks, now the data you´ve chosen will be analyzed for you!\n")
            break

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city.lower()])

    df["Start Time"] = pd.to_datetime(df["Start Time"])
    df["month"] = df["Start Time"].dt.month
    df["day_of_week"] = df["Start Time"].dt.day_name()
    df["hour"] = pd.DatetimeIndex(df["Start Time"]).hour
    df["start_to_end"] = df["Start Station"] + " to " + df["End Station"]

    if month.lower() != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month.lower()) + 1
        df = df[df["month"] == month]

    if day.lower() != 'all':
        df = df[df["day_of_week"] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df["month"].mode()[0]
    print("\nMost common month: {}".format(popular_month))

    # display the most common day of week
    popular_day_of_week = df["day_of_week"].mode()[0]
    print("\nMost common day of week: {}:".format(popular_day_of_week))

    # display the most common start hour
    popular_hour = df["hour"].mode()[0]
    print("\nMost common start hour: {}".format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start = df["Start Station"].mode()[0]
    print("\nMost popular start station:", popular_start)

    # display most commonly used end station
    popular_end = df["End Station"].mode()[0]
    print("\nMost popular end station:", popular_end)

    # display most frequent combination of start station and end station trip
    popular_combo = df["start_to_end"].mode()[0]
    print("\nThe most popular combination of stations is:", popular_combo)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df["Trip Duration"].sum()
    total_travel_time_rounded = round(total_travel_time, 2)
    print("\nThe total travel time in your selected month(s) and day(s) is",
    total_travel_time_rounded, "seconds")

    # display mean travel time
    avg_travel_time = df["Trip Duration"].mean()
    avg_travel_time_rounded = round(avg_travel_time, 2)
    print("\nThe average travel duration in your selected month(s) and day(s) is",
    avg_travel_time_rounded, "seconds")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df["User Type"].value_counts().to_string()
    print("The users in your selected month(s) and day(s) are:\n", user_types)

    # Display counts of gender
    if "Gender" in df.columns:
        gender = df["Gender"].value_counts().to_string()
        print("The gender of the users in your selected month(s) and day(s) is:\n", gender)

    # Display earliest, most recent, and most common year of birth
    if "Birth Year" in df.columns:
        earliest_year = df["Birth Year"].min()
        recent_year = df["Birth Year"].max()
        most_common_year = df["Birth Year"].mode()[0]
        print("In your selected month(s) and day(s), the oldest user was born " \
        "in {} \nand the youngest user was born in {}. \nThe most common birth year was {}."
        .format(int(earliest_year), int(recent_year), int(most_common_year)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data_display(df):
    """Displays 5 rows of raw data upon request"""

    first_line = 0
    last_line = 5

    while True:
        raw_data = input("Would you now like to see 5 lines of raw data? Please enter yes or no\n")
        if raw_data.lower() not in ("yes", "no"):
            print("Oops. This is not a valid entry")
        elif raw_data.lower() == "no":
            print("Alright!")
            break
        else:
            print(df[df.columns[0:]].iloc[first_line:last_line],
            "\nHere you go. You can now choose to see more raw data if you would like to.")
            first_line += 5
            last_line += 5

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data_display(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
