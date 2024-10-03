import numpy as np
import pandas as pd
import inquirer
import time, os, calendar
import calendar

current_directory = os.getcwd()

CITY_DATA = {
    "chicago": os.path.join(current_directory, "chicago.csv"),
    "new york city": os.path.join(current_directory, "new_york_city.csv"),
    "washington": os.path.join(current_directory, "washington.csv"),
}
# Not very usefull but still cool to defined the data types
DTYPES = {
    'Trip Duration': np.float64,
    'Start Station': str,
    'End Station': str,
    'User Type': str,
    'Gender': str,
    'Birth Year': np.float64,
}
VALID_GENDERS = ["Male", "Female"]
VALID_USER_TYPES = ["Subscriber", "Customer"]

def get_filters() -> tuple:
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print("Hello! Let's explore some bikeshare data!")

    # TO DO: get user input for city (chicago, new york city, washington).
    city_question = [
    inquirer.List('city',
                    message="Which city would you like to explore ?",
                    choices=['chicago', 'new york city', 'washington'],
                ),
    ]
    city = inquirer.prompt(city_question)["city"]

    # TO DO: get user input for month (all, january, february, ... , june)
    month_question = [
    inquirer.List('month',
                    message="Which month would you like to focus on ?",
                    choices=["all", "january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
                    # Continue after June for scalability purposes. Even though you mentioned that you selected the first six months of 2017, I believe it’s better to predefine every possible future choice.
                ),
    ]
    month = inquirer.prompt(month_question)["month"]

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day_of_week_question = [
    inquirer.List('day_of_week',
                    message="Which month would you like to focus on ?",
                    choices=["all", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
                ),
    ]
    day = inquirer.prompt(day_of_week_question)["day_of_week"]

    print("-" * 40)
    return city, month, day


def load_data(city: str, month: str, day: str) -> pd.DataFrame:
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    df = pd.read_csv(CITY_DATA[city], dtype=DTYPES, parse_dates=['Start Time', 'End Time'])

    if month != 'all':
        month = list(calendar.month_name).index(month.title())
        df = df[df['Start Time'].dt.month == month]

    if day != 'all':
        df = df[df['Start Time'].dt.day_name() == day.title()]

    return df


def time_stats(df: pd.DataFrame) -> dict:
    """Displays statistics on the most frequent times of travel."""

    print("\nCalculating The Most Frequent Times of Travel...\n")
    start_time = time.time()
    results = {}

    if df.empty or 'Start Time' not in df.columns:
        print("The DataFrame is empty or missing 'Start Time' column.")
        return results

    df['Start Time'] = pd.to_datetime(df['Start Time'], format='%Y-%m-%d %H:%M:%S', errors='coerce')
    df['Start Time'] = df['Start Time'].dropna()

    # TO DO: Display the most common month
    most_common_months = df['Start Time'].dt.month.mode()
    if not most_common_months.empty:
        results['mostCommonMonth'] = [calendar.month_name[int(month)].lower() for month in most_common_months]
    else:
        results['mostCommonMonth'] = []
    print("The most common month(s) is/are:", results['mostCommonMonth'])

    # TO DO: Display the most common day of week
    most_common_days = df['Start Time'].dt.day_name().mode()
    if not most_common_days.empty:
        results["mostCommonDay"] = [day_of_week.lower() for day_of_week in most_common_days]
    else:
        results["mostCommonDay"] = []
    print("The most common day(s) of the week is/are: ", results["mostCommonDay"])

    # TO DO: Display the most common start hour
    most_common_hours = df['Start Time'].dt.hour.mode()
    if not most_common_hours.empty:
        results["mostCommonStartHour"] = [int(hour) for hour in most_common_hours.tolist()]
    else:
        results["mostCommonStartHour"] = []
    print("The most common start hour(s) is/are: ", results["mostCommonStartHour"])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)

    return results


def station_stats(df: pd.DataFrame) -> None:
    """Displays statistics on the most popular stations and trip."""

    print("\nCalculating The Most Popular Stations and Trip...\n")
    start_time = time.time()
    results = {}

    def validate_address(value):
        # we can imagine Nominatim API to validate the address
        return isinstance(value, str) and bool(value.strip())

    # TO DO: Display most commonly used start station
    if "Start Station" in df.columns:
        df['Start Station'] = df['Start Station'].dropna().apply(lambda x: x if validate_address(x) else None)
        results["mostCommonStartStation"] = df['Start Station'].mode().to_list()
        print("The most common start station is: ", results["mostCommonStartStation"])

    # TO DO: Display most commonly used end station
    if "End Station" in df.columns:
        df['End Station'] = df['End Station'].dropna().apply(lambda x: x if validate_address(x) else None)
        results["mostCommonEndStation"] = df['End Station'].mode().to_list()
        print("The most common end station is: ", results["mostCommonEndStation"])

    # TO DO: Display most frequent combination of start station and end station trip
    if "Start Station" in df.columns and "End Station" in df.columns:
        results["mostCommonTrip"] = (df['Start Station'] + " -> " + df['End Station']).mode().to_list()
        print("The most common trip is: ", results["mostCommonTrip"])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)

    return results

def trip_duration_stats(df: pd.DataFrame) -> None:
    """Displays statistics on the total and average trip duration."""

    print("\nCalculating Trip Duration...\n")
    start_time = time.time()
    results = {}

    if df.empty or "Trip Duration" not in df.columns:
        print("The DataFrame is missing 'Trip Duration' column.")
        return results

    df['Trip Duration'] = pd.to_numeric(df['Trip Duration'], errors='coerce')
    df['Trip Duration'] = df['Trip Duration'].dropna()
    df['Trip Duration'] = df[df['Trip Duration'] > 0]

    # TO DO: Display total travel time
    results['totalTravelTime'] = df['Trip Duration'].sum()
    print("The total travel time is: ", f"~{round(results['totalTravelTime'] / 3600, 2)} hours")

    # TO DO: Display mean travel time
    results['averageTravelTime'] = df['Trip Duration'].mean()
    print("The mean travel time is: ", f"~{round(results['averageTravelTime'] / 60, 2)} mins")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)
    
    return results


def user_stats(df: pd.DataFrame) -> None:
    """Displays statistics on bikeshare users."""

    print("\nCalculating User Stats...\n")
    start_time = time.time()
    results = {}

    # TO DO: Display counts of user types
    if 'User Type' in df.columns:
        results['userTypeCounts'] = df[df['User Type'].isin(VALID_USER_TYPES)]['User Type'].value_counts(dropna=True).to_dict()
        print("The counts of user types are: ", results["userTypeCounts"])
    else:
        results['userTypeCounts'] = {}

    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        results['genderCounts'] = df[df['Gender'].isin(VALID_GENDERS)]['Gender'].value_counts(dropna=True).to_dict()
        print("The counts of gender are: ", results['genderCounts'])
    else:
        results['genderCounts'] = {}

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        df["Birth Year"] = df["Birth Year"].dropna()
        df['Birth Year'] = pd.to_numeric(df['Birth Year'], errors='coerce')
        results['earliestYearOfBirth'] = int(df['Birth Year'].min())
        print("The earliest year of birth is: ", results['earliestYearOfBirth'])
    else:
        results['earliestYearOfBirth'] = None

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)

    return results

def main() -> None:
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input("\nWould you like to restart? Enter yes or no.\n")
        if restart.lower() != "yes":
            break


if __name__ == "__main__":
    main()
