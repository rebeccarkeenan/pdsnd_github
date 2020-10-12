import time
import calendar
import datetime 
import pandas as pd
import numpy as np

CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York City': 'new_york_city.csv',
              'Washington': 'washington.csv' }


month_mapping = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('\nHello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    options = list(CITY_DATA.keys())
    while True:
      city = input(f'Please input city name. Options are {options}. \n')
      if city not in list(CITY_DATA.keys()):
        print(f'Please choose one of the following: {options}')
        continue
      else:
        break

    # get user input for month (all, january, february, ... , june)
    months_list = ['January', 'February', 'March', 'April', 'May', 'June', 'All']
    while True:
      month = input(f'Which month are you interested in? Choose one of the following: {months_list} \n')
      if month not in ['January', 'February', 'March', 'April', 'May', 'June', 'All']:
        print(f'Please choose one of the following: {months_list} \n')
        continue
      else:
        break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    days_list = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'All']
    while True:
      day = input(f'Which day are you interested in? Choose one of the following: {days_list} \n')
      if day not in days_list:
        print(f'Which day are you interested in? Choose one of the following: {days_list} \n')
        continue
      else:
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

    # Create dataframe 
    df = pd.read_csv(CITY_DATA[city])

    # Convert Start and End Times to datetime format
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # Dataframes for month, day of week, day, and hour
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # Month filter
    if month != 'All':
        months_list = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months_list.index(month) + 1 

        df = df[df['month'] == month]

    # Day of Week filter
    if day != 'All':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating the most frequent times of travel...\n')
    start_time = time.time()

    # display the most common month
    df['month'] = df['Start Time'].dt.month
    most_common_month = df['month'].mode()[0]
    print('Most Common Month: ', month_mapping[most_common_month])

    # display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]
    print('Most Common Day: ', most_common_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_common_start_hr = df['hour'].mode()[0]
    print('Most Common Hour: ', most_common_start_hr)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    return df


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating the Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_st = df['Start Station'].value_counts().idxmax()
    print('Most Common Start Station: ', most_common_start_st)


    # display most commonly used end station
    most_common_end_st = df['End Station'].value_counts().idxmax()
    print('Most Common End Station: ', most_common_end_st)


    # display most frequent combination of start station and end station trip
    combination_stations = df.groupby(['Start Station', 'End Station']).count()
    print('Most Common Stations used in Combination: ', most_common_start_st, ' and ', most_common_end_st)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total Travel Time: ', total_travel_time/86400, ' days')


    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean Travel Time: ', mean_travel_time/60, ' minutes')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    count_user_types = df['User Type'].value_counts()
    print('User Types:\n', count_user_types)

    # Display counts of gender
    try:
      count_gender = df['Gender'].value_counts()
      print('Gender Types:\n', count_gender)
    except KeyError:
      print('Data unavailable.')

    # Display earliest, most recent, and most common year of birth
    try:
      earliest_birth_yr = df['Birth Year'].min()
      print('Earliest Birth Year:', earliest_birth_yr)
    except KeyError:
      print('Data unavailable.')

    try:
      most_recent_yr = df['Birth Year'].max()
      print('Most Recent Year: ', most_recent_yr)
    except KeyError:
      print('Data unavailable.')

    try:
      most_common_yr = df['Birth Year'].value_counts().idxmax()
      print('Most Common Year: ', most_common_yr)
    except KeyError:
      print('Data unavailable.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data_display(df):
    
    data = 0
    while True:
       display = input('Would you like to see the first 5 lines of raw data? Choose Yes or No.\n')
       if display == 'No':
            return
       elif display == 'Yes':
        data += 5
        print(df.iloc[data:data+5])
       else:
        print('Choose Yes or No.\n') 


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