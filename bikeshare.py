import time
import pandas as pd
import numpy as np
import decimal # https://stackoverflow.com/questions/4518641/how-do-i-round-a-floating-point-number-up-to-a-certain-decimal-place

## Mode() Source --> https://docs.python.org/3.4/library/statistics.html

#Combines all three city .csvs to a single DF
## Quick workaround to allow both case sensitive option to work :( Not ideal fix :(
CITY_DATA = { 	'Washington': 'washington.csv',
				'Chicago': 'chicago.csv',
				'New York City': 'new_york_city.csv',
                'washington': 'washington.csv',
				'chicago': 'chicago.csv',
				'new york city': 'new_york_city.csv',	}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
		(str) city - name of the city to analyze
    """

    print('\nWelcome! Let\'s explore some data from US bikeshare and see what we can learn! \n \n ^_^')

    while True:
      month = input("\n To begin with our investigation. \nWhich month would you like to filter by? \nJanuary, February, March, April, May, June or type 'all' if you do not have any preference?\n").lower()
      if month not in ('january', 'february', 'march', 'april', 'may', 'june', 'all'):
        print("Sorry, I was unable to locate that month :( please type the entire month like: \n \nJune \n \nand try again. Thankyou! :)")
        continue
      else:
        break

    while True:
      day = input("\nAre you looking for any day in particular? If so, please enter the day as follows: Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or type 'all' if you wish to view all days of the week\n").lower()
      if day not in ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all'):
        print("Sorry, I was unable to locate that day :( please type the entire day like: \n \nSunday \n \nand try again. Thankyou! :)")
        continue
      else:
        break

    while True:
      city = input("\nWhich city would you like to filter by? New York City, Chicago or Washington to see statistics on your chosen city?\n").lower()
      if city not in ('washington','chicago','new york city'):
        print("Sorry, I was unable to locate that city :( please type the entire city like: \n \nWashington \n \nand try again. Thankyou! :)")
        continue
      else:
        break

    print('*_*'*50)
    return month, day, city


def load_data(month, day, city):

    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

	##must call main city df first
    # declare all three . csvsinto a dataframe
    df = pd.read_csv(CITY_DATA[city])

	# convert the Start Time column to a datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

	# source month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name


    # month filter
    if month != 'all':
   	 	# use the index of the months list to get the corresponding int ## data sets only go between Jan and June :(
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

    	# filter by month to create the new dataframe
        df = df[df['month'] == month]

    # day filter
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays stats on the MOST frequent times of travel."""

    print('\nCalculating The MOST Frequent Times of Travel...\n')
    start_time = time.time()

#display the MOST Popular month
    Popular_month = df['month'].mode()[0]
    print('Wow! The MOST Popular month is:\n', Popular_month)

#display the MOST Popular week
    Popular_day = df['day_of_week'].mode()[0]
    print('Wow! The MOST Popular day is:\n', Popular_day)

#display the MOST Popular hour
    df['hour'] = df['Start Time'].dt.hour
    Popular_hour = df['hour'].mode()[0]
    print('Wow! The MOST Popular hour is:\n', Popular_hour)

    """Displays stats on the LEAST frequent times of travel.""" ##could not locate the opposite of mode() :(

    print('\nCalculating The LEAST Frequent Times of Travel...\n')

# display the LEAST Popular month
    LEAST_Popular_month = df['month'].value_counts().idxmin()
    print("Wow! The LEAST Popular month is :\n", LEAST_Popular_month)

# display the LEAST Popular day of week
    LEAST_Popular_day_of_week = df['day_of_week'].value_counts().idxmin()
    print("Wow! The LEAST Popular day of week is:\n", LEAST_Popular_day_of_week)

# display the LEAST Popular Start hour
    LEAST_Popular_start_hour = df['hour'].value_counts().idxmin()
    print("Wow! The LEAST Popular Start hour is:\n", LEAST_Popular_start_hour)
    print("\nThat was quick! This query only took %s seconds! We can thank numpy for that ^_-" % (round(time.time() - start_time,2)),"\n")
    print('*_*'*50)

def Stationn_stats(df):
    """Displays stats on the MOST Popular Stations and trip."""
    print('\nCalculating The MOST Popular Stations and Trip...\n')
    start_time = time.time()

# display MOST Popular Start Station
    Start_Stationn = df['Start Station'].value_counts().idxmax()
    print('Wow! The MOST Popular used Start Station is:\n', Start_Stationn)

# display MOST Popular End Station
    End_Stationn = df['End Station'].value_counts().idxmax()
    print('Wow! The MOST Popular used End Station is:\n', End_Stationn)

#display MOST Popular trip by Start and End Stations
    Trip_Stationns = df.groupby(['Start Station', 'End Station']).count()
    print('Wow! The MOST Popular trip by Start Station and End Station is:\n', Start_Stationn, " & ", End_Stationn)

    """Displays stats on the LEAST Popular Stations and trip."""
    print('\nCalculating The LEAST Popular Stations and Trip...\n')

# display LEAST Popular Start Station
    Start_Stationn = df['Start Station'].value_counts().idxmin()
    print('Wow! The LEAST Popular used Start Station is:\n', Start_Stationn)

# display LEAST Popular End Station
    End_Stationn = df['End Station'].value_counts().idxmin()
    print('Wow! The LEAST Popular used End Station is:\n', End_Stationn)

#display LEAST Popular trip by Start and End Stations
    Trip_Stationns = df.groupby(['Start Station', 'End Station']).count().idxmin()
    print('Wow! The LEAST Popular trip by Start Station and End Station is:\n', Start_Stationn, " & ", End_Stationn)

    print("\nThat was quick! This query only took %s seconds! We can thank numpy for that ^_-" % (round(time.time() - start_time,2)),"\n")
    print('*_*'*50)


def trip_duration_stats(df):
    """Displays stats on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

#display travel time
    Total_Travel_Time = sum(df['Trip Duration'])
    print('Wow! The Total travel time is:\n',round(Total_Travel_Time/86400,2), " Days")

#display mean travel time
    Mean_Travel_Time = df['Trip Duration'].mean()
    print('Wow! The Mean travel time is:\n',round(Mean_Travel_Time/60,2), " Minutes")

#display max trip travel time
    Max_Travel_Time = df['Trip Duration'].max()
    print('Wow! The Max trip travel time:\n',round(Max_Travel_Time/60,2), " Minutes")

#display min travel time
    Min_Travel_Time = df['Trip Duration'].min()
    print('Wow! The Min trip travel time is:\n', round(Min_Travel_Time/60,2), " Minutes")

    print("\nThat was quick! This query only took %s seconds! We can thank numpy for that ^_-" % (round(time.time() - start_time,2)),"\n")
    print('*_*'*50)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

#Display volume of user types

    user_types = df['User Type'].value_counts()
    print('\nPLEASE NOTE: Washington DataSet DOES NOT contain data on Gender or Birthyear\n \nUser Types:\n',user_types)

#Display volume split of gender types

    try:
      gender_types = df['Gender'].value_counts()
      print('\nGender Types:\n',gender_types)
    except KeyError:
      print("\nGender Types:\nNo data available for this month.")

 #Display earliest, MOST recent, and MOST Popular year of birth

    try:
      Earliest_Year = df['Birth Year'].min()
      print('Wow! The Earliest Birth Year is:\n',int(Earliest_Year))
    except KeyError:
      print("\nEarliest Birth Year:\nNo data available for this month.")

    try:
      MOST_Recent_Year = df['Birth Year'].max()
      print('Wow! The MOST Recent Birth Year is:\n',int(MOST_Recent_Year))
    except KeyError:
      print("\nMOST Recent Birth Year:\nNo data available for this month.")

    try:
      MOST_Popular_Year = df['Birth Year'].value_counts().idxmax()
      print('Wow! The MOST Popular Birth Year is:\n',int(MOST_Popular_Year))
    except KeyError:
      print("\nMOST Popular Birth Year:\nNo data available for this month.")

    try:
      LEAST_Popular_Year = df['Birth Year'].value_counts().idxmin()
      print('Wow! The LEAST Popular Birth Year is:\n',int(LEAST_Popular_Year))
    except KeyError:
      print("\nLEAST Popular Birth Year:\nNo data available for this month.")

    print("\nThat was quick! This query only took %s seconds! We can thank numpy for that ^_-" % (round(time.time() - start_time,2)),"\n")
    print('*_*'*50)

    # Allow user to review 5 rows of raw data at a time
def raw_data(df):
    user_input = input('Would you like to review some of the raw data?\n Please enter Y is so or N if not.\n')
    line_number = 0

    while 1 == 1 :
        if user_input.lower() != 'n':
            print(df.iloc[line_number : line_number + 5])
            line_number += 5
            user_input = input('Would you like to review some of the raw data?\n Please enter Y is so or N if not.\n')
        else:
            break


def main():
    while True:
      month, day, city = get_filters()
      df = load_data(month, day, city)

      time_stats(df)
      Stationn_stats(df)
      trip_duration_stats(df)
      user_stats(df)
      raw_data(df)

      restart = input('\nWould you like to restart? Enter Y if so or N to abort.\n')
      if restart.upper() != 'Y':
        break

if __name__ == "__main__":
	main()
