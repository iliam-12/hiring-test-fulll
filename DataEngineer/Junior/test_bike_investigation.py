import unittest
import pandas as pd
import numpy as np
from bike_investigation import time_stats, station_stats, trip_duration_stats, user_stats

#############################
#        TESTS OVERVIEW     #
#############################

# ===========================
#   TIME STATISTICS TESTS
# ===========================
# - test_time_stats: Verify the accuracy of time statistics calculations.
# - test_time_stats_missing_data: Ensure proper handling of missing time data.
# - test_time_stats_unrecognized_date_field: Check for errors with unrecognized date fields.

# =============================
#   STATION STATISTICS TESTS
# =============================
# - test_station_stats: Validate the correctness of station statistics.
# - test_station_stats_missing_data: Test the response to missing station data.
# - test_station_stats_unrecognized_station: Handle cases of unrecognized station entries.

# ==================================
#   TRIP DURATION STATISTICS TESTS
# ==================================
# - test_trip_duration_stats: Assess the calculations related to trip durations.
# - test_trip_duration_stats_missing_data: Ensure the system can manage missing trip duration data.
# - test_trip_duration_stats_unrecognized_trip_duration: Verify error handling for unrecognized trip durations.

# =================================
#        USER STATISTICS TESTS
# =================================
# - test_user_stats: Evaluate the accuracy of user statistics computations.
# - test_user_stats_missing_data: Check the system’s response to missing user data.
# - test_user_stats_unrecognized_data: Manage cases of unrecognized user data.

# ===========================
#        NO COLUMN TESTS
# ===========================
# - test_time_stats_column: Validate behavior when no columns are present for time stats.
# - test_station_stats_column: Ensure proper handling when no columns are available for station stats.
# - test_trip_duration_stats_column: Check response to missing columns in trip duration stats.
# - test_user_stats_column: Assess behavior when user stats columns are absent.

#############################


class TestBikeShareData(unittest.TestCase):

    ### TIME STATS ###

    def test_time_stats(self):
        data = {
            'Start Time': ['2017-01-01 09:07:57', '2017-01-02 09:07:57', '2017-01-03 00:07:57'],
            'End Time': ['2017-01-01 09:20:53', '2017-01-02 09:20:53', '2017-01-03 00:20:53'],     
        }

        # TO DO : create a pandas DataFrame from the data dictionary
        df = pd.DataFrame(data)

        result = time_stats(df)

        self.assertEqual(result['mostCommonMonth'], ['january'])

        # TO DO : add more tests for the other keys in the result dictionary
        self.assertEqual(sorted(result['mostCommonDay']), sorted(['sunday', 'monday', 'tuesday']))
        self.assertEqual(result['mostCommonStartHour'], [9])

    def test_time_stats_missing_data(self):
        data_nan = {
            'Start Time': [None, pd.NaT, '2017-01-01', '2017-01-01 09:07:57', '2017-01-02 09:07:57', '2017-01-03 00:07:57', '2017-01-04 00:20:53'],
        }
        df = pd.DataFrame(data_nan)

        result = time_stats(df)

        self.assertEqual(result['mostCommonMonth'], ["january"])
        self.assertEqual(sorted(result['mostCommonDay']), sorted(["monday", "sunday", "tuesday", "wednesday"]))
        self.assertEqual(result['mostCommonStartHour'], [0, 9])

    def test_time_stats_unrecognized_date_field(self):
        data_unrecognized = {
            'Start Time': ['2017-01-01 09:07:57', 'UNRECOGNIZED_VALUE', "111111", "2017-01-01"],
        }
        df = pd.DataFrame(data_unrecognized)
        
        result = time_stats(df)

        self.assertEqual(result['mostCommonMonth'], ['january'])
        self.assertEqual(sorted(result['mostCommonDay']), ['sunday'])
        self.assertEqual(result['mostCommonStartHour'], [9])

    # TO DO : base on the above test, create tests for station_stats, trip_duration_stats and user_stats function. Make sure you cover common corner cases.  
    ### STATION STATS ###

    def test_station_stats(self):
        data = {
            'Start Station': ['A', 'B', 'C', 'A'],
            'End Station': ['B', 'A', 'B', 'B']
        }
        df = pd.DataFrame(data)

        result = station_stats(df)
        
        self.assertEqual(result['mostCommonStartStation'], ['A'])
        self.assertEqual(result['mostCommonEndStation'], ['B'])
        self.assertEqual(result['mostCommonTrip'], ['A -> B'])
    
    def test_station_stats_missing_data(self):
        data_nan = {
            'Start Station': ['A', 'B', 'C', 'A', None, ''],
            'End Station': ['B', 'A', 'B', 'B', 'C', None]
        }
        df = pd.DataFrame(data_nan)

        result = station_stats(df)

        self.assertEqual(result['mostCommonStartStation'], ['A'])
        self.assertEqual(result['mostCommonEndStation'], ['B'])
        self.assertEqual(result['mostCommonTrip'], ['A -> B'])

    def test_station_stats_unrecognized_station(self):
        data_unrecognized = {
            'Start Station': ['A', 'B', 123],
            'End Station': ['B', None, {1:2}]
        }
        df = pd.DataFrame(data_unrecognized)

        result = station_stats(df)

        self.assertEqual(result['mostCommonStartStation'], ['A', 'B'])
        self.assertEqual(result['mostCommonEndStation'], ['B'])
        self.assertEqual(result['mostCommonTrip'], ['A -> B'])

    ### TRIP DURATION STATS ###

    def test_trip_duration_stats(self):
        data = {
            'Trip Duration': [100, 200, 300, 400]
        }
        df = pd.DataFrame(data)

        result = trip_duration_stats(df)

        self.assertEqual(result['totalTravelTime'], 1000)
        self.assertEqual(result['averageTravelTime'], 250)
    
    def test_trip_duration_stats_missing_data(self):
        data_nan = {
            'Trip Duration': [100, 200, 300, None, np.nan, '']
        }
        df = pd.DataFrame(data_nan)

        result = trip_duration_stats(df)

        self.assertEqual(result['totalTravelTime'], 600)
        self.assertEqual(result['averageTravelTime'], 200)

    def test_trip_duration_stats_unrecognized_trip_duration(self):
        data_unrecognized = {
            'Trip Duration': [-100, 100, 200, 'UNRECOGNIZED_VALUE']
        }
        df = pd.DataFrame(data_unrecognized)

        result = trip_duration_stats(df)

        self.assertEqual(result['totalTravelTime'], 300)
        self.assertEqual(result['averageTravelTime'], 150)

    ### USER STATS ###

    def test_user_stats(self):
        data = {
            'User Type': ['Subscriber', 'Customer', 'Subscriber'],
            'Gender': ['Male', 'Male', 'Female'],
            'Birth Year': ["1915", 1989, 2001]
        }
        df = pd.DataFrame(data)

        result = user_stats(df)

        self.assertEqual(result['userTypeCounts'], {'Subscriber': 2, 'Customer': 1})
        self.assertEqual(result['genderCounts'], {'Male': 2, 'Female': 1})
        self.assertEqual(result['earliestYearOfBirth'], 1915),
    
    def test_user_stats_missing_data(self):
        data = {
            'User Type': [None, 'Subscriber', 'Customer', 'Subscriber'],
        }
        df = pd.DataFrame(data)
        
        result = user_stats(df)
        
        self.assertEqual(result['userTypeCounts'], {'Subscriber': 2, 'Customer': 1})
        self.assertEqual(result['genderCounts'], {})
        self.assertEqual(result['earliestYearOfBirth'], None),        
    
    def test_user_stats_unrecognized_data(self):
        data = {
            'User Type': ["1", 11111, "test", 'Subscriber', 'Customer', 'Subscriber', 'Customer'],
            'Gender': [1, "Unicorn", "Non-binary", "Goat", 'Male', 'Male', 'Female'],
            'Birth Year': ["9999", "abc", "1911", 1915, 1989, 2001, 2005]
        }
        df = pd.DataFrame(data)
    
        result = user_stats(df)

        self.assertEqual(result['userTypeCounts'], {'Subscriber': 2, 'Customer': 2})
        self.assertEqual(result['genderCounts'], {'Male': 2, 'Female': 1})
        self.assertEqual(result['earliestYearOfBirth'], 1911),    


    ### NO COLUMN ###

    def test_time_stats_column(self):
        data = {
            # No 'Start Time' column
        }
        df = pd.DataFrame(data)

        result = time_stats(df)

        self.assertEqual(result, {})

    def test_station_stats_column(self):
        data = {
            # No 'Start Station' column
            # No 'End Station' column
        }
        df = pd.DataFrame(data)

        result = station_stats(df)

        self.assertEqual(result, {})

    def test_trip_duration_stats_column(self):
        data = {
            # No 'Trip Duration' column
        }
        df = pd.DataFrame(data)

        result = trip_duration_stats(df)

        self.assertEqual(result, {})

    def test_user_stats_column(self):
        data = {
            # No 'User Type' column
            # No 'Gender' column
            # No 'Birth Year' column
        }
        df = pd.DataFrame(data)

        result = user_stats(df)

        self.assertEqual(result['userTypeCounts'], {})
        self.assertEqual(result['genderCounts'], {})
        self.assertEqual(result['earliestYearOfBirth'], None)


if __name__ == '__main__':
    unittest.main()