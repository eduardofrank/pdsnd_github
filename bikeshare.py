import time
from datetime import datetime
import pandas as pd
import numpy as np

pd.set_option('display.max_columns', None)

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
    Checks have been provided for month and day
    All inputs have been normalized
    Exceptions have been placed to catch ValueErrors
    KeyboardInterrupt is allowed
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city = input('Type in a city. Choose from Chicago, New York City or Washington: ').strip().lower()  # Normalize input for consistency
            if city in CITY_DATA:
                print(f"Great! Data for {city.title()} is available.\n")
                break
            else:
                raise ValueError(f"Sorry, not in dict.")
        except ValueError:
            print(f"\nSorry, '{city.title()}' is not available.\nChoose from 'Chicago', 'New York City' or 'Washington'. Please try again.\n")
    # get user input for month (all, january, february, ... , june)
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all'] # a list to check against
    while True:
        try:
            month = input("Choose any month from 'January' to 'June', or type 'All' for the whole six months.: ").strip().lower()  # Normalize input for consistency
            if month in months:
                print("Thank you")
                break
            else:
                raise ValueError(f"Sorry, not in list.")
        except ValueError:
            print(f"\nSorry, '{month}' is not available.\nChoose from 'January', 'February', 'March', 'April', 'May' or 'June'.\nYou may also type 'All' for no particular month.\n")
    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all'] # a list to check against
    while True:
        try:
            day = input("Choose any day of the week from 'Monday' to 'Sunday', or type 'All' for all days of the week.: ").strip().lower()  # Normalize input for consistency
            if day in days:
                print("Thank you")
                break
            else:
                raise ValueError(f"Sorry, not in list.")
        except ValueError:
            print(f"\nSorry, '{day}' is not available.\nChoose from 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday' or 'Sunday'.\nYou may also type 'All' for no particular day of the week.\n")
    print(f"Your filters are '{city.title()}', '{month.title()} and '{day.title()}'")
    #print('-'*80)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day

    The script takes the provided city and reads the data into 'df'.
    Start and End Times are not really dates, but strings in date format. 
    to_datetime helps with the conversion to real date format for all values in the 'Start Time' column.
    Two new columns are added to the DataFrame, 'month' and 'day_of_week' that wil be used to query from them.
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city], index_col=0)
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df.loc[df['day_of_week'] == day.title()]
    
    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel.
    To improve reporting, this function takes month and day as arguments
    Most common month and most common day are subject to a conditional statement based on the selections for month and day
    """

    print('\nWhat are the Most Frequent Times to hop on a bike?')
    start_time = time.time()

    # display the most common month
    # display the most common day of week
    # display the most common start hour
    if month != 'all' and day != 'all':
        print(f"The most frequent hour to initiate a ride on a {day.title()} in {month.title()} is at {df['Start Time'].dt.hour.mode()[0]}.")
    elif month != 'all' and day == 'all':
        # "You selected the month of {month.title()}. No particular day of the week was selected for this analysis."
        print(f"The most common day of the week: {df['Start Time'].dt.day_name().mode()[0]}.")
        print(f"The most common hour: {df['Start Time'].dt.hour.mode()[0]}")
    elif month == 'all' and day != 'all':
        # "For this analysis, the week day {day.title()} was selected for all months."
        print(f"The most common month: {df['Start Time'].dt.month_name().mode()[0]}.")
        print(f"The most common hour: {df['Start Time'].dt.hour.mode()[0]}")
    elif month == 'all' and day == 'all':
        # "No particular month or day of the week were selected for this analysis."
        print(f"The most common month: {df['Start Time'].dt.month_name().mode()[0]}")
        print(f"The most common day of the week: {df['Start Time'].dt.day_name().mode()[0]}.")
        print(f"The most common hour: {df['Start Time'].dt.hour.mode()[0]}")

    

    print("This took %s seconds." % (time.time() - start_time))
    #print('-'*80)


def station_stats(df):
    """Displays statistics on the most popular stations and trip.
    """

    print('\nMost common Start and End Stations and their score of departures and arrivals')
    start_time = time.time()

    # display most commonly used start station
    common_start = df['Start Station'].mode()[0]
    start_count = df['Start Station'].value_counts().max()
    print(f"The most frequent Start Station: {common_start}   Departures: {start_count}.")
    # display most commonly used end station
    common_end = df['End Station'].mode()[0]
    end_count = df['End Station'].value_counts().max()
    print(f"The most frequent End Station: {common_end}   Arrivals: {end_count}.")

    print("This took %s seconds." % (time.time() - start_time))

    print('\nWhat is the most common Start and End Station combination?')
    start_time = time.time()
    # display most frequent combination of start station and end station trip
    combinations = df.apply(lambda row: (row['Start Station'], row['End Station']), axis=1)
    most_frequent_combination = combinations.mode().iloc[0]
    print(f"{' - '.join(most_frequent_combination)}   Count: {combinations.value_counts()[most_frequent_combination]}")
    
    print("This took %s seconds." % (time.time() - start_time))

    print('\nWhat is the most common Station for round trips?\nHow long is the average round trip?')
    start_time = time.time()
    # display the most frequent Station for round trips
    round_trip_df = df[df['Start Station'] == df['End Station']]
    round_trip_combinations = round_trip_df.apply(lambda row: (row['Start Station'], row['End Station']), axis=1)
    most_frequent_rt = round_trip_combinations.mode().iloc[0]
    rt_count = round_trip_combinations.value_counts().max()
    average_duration = round_trip_df['Trip Duration'].mean()
    print(f"{most_frequent_rt[0]}   Count: {rt_count}. Average Trip Duration: {average_duration:.2f} seconds.")
        
    print("This took %s seconds." % (time.time() - start_time))
    #print('-'*80)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nWhat is the average Trip Duration?')
    start_time = time.time()
    # display mean travel time
    print(f"The mean travel time is: {df['Trip Duration'].mean():.2f} seconds")

    # display total travel time
    print(f"The total time for rides in the filtered period: {df['Trip Duration'].sum():.2f} seconds")

    print("This took %s seconds." % (time.time() - start_time))
    #print('-'*80)


def user_stats(df, city):
    """Displays statistics on bikeshare users.
    The display of Gender and Birth Year,available only for Chicago and New York City, is subject to a conditional statement based on the city selected.
    """

    print('\nCalculating User Stats...')
    start_time = time.time()

    # Display counts of user types
    print("User Break Up:")
    user_type = df['User Type'].value_counts()
    for index, value in user_type.items():
        print(f"{index} {value}")

    # Display counts of gender
    if city != 'washington':
        male = df['Gender'].value_counts()['Male']
        female = df['Gender'].value_counts()['Female']
        print(f"Male:{male}   Female: {female}.")
        # Display earliest, most recent, and most common year of birth
        print(f"The most common Birth Year among users is {int(df['Birth Year'].mode()[0])}")
        print(f"The earliest Birth Year is {int(df['Birth Year'].min())}\nThe most recent one is {int(df['Birth Year'].max())}.")


    print("This took %s seconds." % (time.time() - start_time))
    print('-'*80)


def restart():
    """ Handles the question of restart or not
    """
    while True:
        response = input('Would you like to restart? Enter yes or no.\n')
        if response.lower() == 'yes':
            break
        elif response.lower() == 'no':
            break
        else:
            print("Type yes or no")
    return response


def chunk_gen(df):
    """ Handles the data for tho be shown on screen
    """
    def see_data():
        """ Handles the question of displaying any data
        """
        while True:
            response = input('Would you like to see the raw data five entries at a time? Enter yes or no.\n') # prompt to show or not the raw data
            if response.lower() == 'yes':
                break
            elif response.lower() == 'no':
                break
            else:
                print("Type yes or no")
        return response
    def more_data():
        """ Handles the question of displaying more data or not
        """
        while True:
            response = input('Would you like to see five more entries? Enter yes or no.\n') # prompt to display more data or not
            if response.lower() == 'yes':
                break
            elif response.lower() == 'no':
                break
            else:
                print("Type yes or no")
        return response
    def chunker(iterable, size):
        """ Yields the chunks of size-rows of data to be shown on screen
        """
        for i in range(0, len(iterable), size):
            yield iterable.iloc[i:i+size]

    display_data = see_data()
    if display_data == 'yes':
        chunk_generator = chunker(df, 5) # call the generator function and passes 5 as the size or number of lines from df.

        while True:    
            chunk = next(chunk_generator)
            print(chunk)
            print_more = more_data()
            if print_more.lower() != 'yes':
                break

def main():
    """ This is the function that calls all other functions.
    """
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        # descriptive statistics
        station_stats(df)
        time_stats(df, month, day)
        trip_duration_stats(df)
        user_stats(df, city)
        # displays the data
        chunk_gen(df)
        # prompt to restart
        re_start = restart()
        if re_start.lower() != 'yes':
            break


if __name__ == "__main__":
	main()