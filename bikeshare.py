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
    
    # get user input for city (chicago, new york city, washington).
    
    while True:
        city = input('Among Chicago, New York City and Washington, which city do you want to see the data for:\n')      
        if not city.lower() in CITY_DATA.keys():
            print('Sorry, please enter only city names with format from the above list\n')
        else:
            break
    # get user input for month
    month_option = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    while True:
        month = input('Which month from first half of the year to filter by? Type \'All\' for no month filter:\n')
        if not month.lower() in month_option:
            print('Sorry, please enter full month name from first half of the year, or \'All\' for no month filter\n')
        else:
            break
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day_option = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    while True:
        day = input('Which day of week to filter the data by? Type \'All\' for no day filter:\n')
        if not day.lower() in day_option:
            print('Sorry, please enter full day of the week name, or \'All\' for no day filter\n')
        else:
            break

    print(
        '\nRight away, loading {city} data with month ({month}) and day of week ({dow}) of your choice.'.format(
            city=city.title(),
            month=month.title(),
            dow=day.title(),
        )
    )
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
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    
    if month.lower() != 'all':
        
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month_filter = months.index(month.lower()) + 1
        df = df[df['month'] == month_filter]
        
    if day.lower() != 'all':
        df = df[df['day_of_week'] == day.title()]
        
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    print('Most common month : ', popular_month)

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('Most common day : ', popular_day)

    # display the most common start hour
    df['start_hour'] = df['Start Time'].dt.hour
    popular_start_hour = df['start_hour'].mode()[0]
    print('Most common start hour : ', popular_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most common start station : ', popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most common end station : ', popular_end_station)

    # display most frequent combination of start station and end station trip
    df['start_end'] = df['Start Station'] + ' to ' + df['End Station']
    frequent_start_end = df['start_end'].mode()[0]
    print('Most frequent combination of start and end station: ', frequent_start_end)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total trips
    total_trips = df['Trip Duration'].count()
    print('Total trips in chosen filters: {}'.format(total_trips))
    
    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total trip duration: {} seconds, or {} hours'.format(total_travel_time, total_travel_time/3600))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Average trip duration: {} seconds, or {} hours'.format(mean_travel_time, mean_travel_time/3600))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # display counts of user types
    user_types_count = df['User Type'].value_counts()
    print('User type:\n',user_types_count,'\n')

    if city.lower() != 'washington':
        # display counts of gender
        gender_count = df['Gender'].value_counts()
        print('Gender:\n', gender_count,'\n')

        # display earliest, most recent, and most common year of birth
        min_birth = df['Birth Year'].min()
        max_birth = df['Birth Year'].max()
        common_birth = df['Birth Year'].mode()[0]
        print('Earliest birth year: ', min_birth)
        print('Most recent birth year: ', max_birth)
        print('Most common birth year: ', common_birth)

    else:
        print('There\'s no gender and birth year information for Washington city')
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# create generator for raw data
def get_raw(df, step):
    total_rows = df.shape[0]
    for i in range(0, total_rows, step):
        yield df[i:i+step]


# prompt user input and print 5 rows at a time        
def display_data(df):
    for r in get_raw(df, 5):
        prompt = input('\nWould you like to see some raw data? Enter yes or no.\n')
        if prompt.lower() != 'yes':
            break
        print(r)

# run all functions and prompt user to start over
def run():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_data(df)
        
        restart = input('\nWould you like to start over? Input yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == '__main__':
    run()
