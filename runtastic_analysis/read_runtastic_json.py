import json
from time import strftime, localtime
from math import floor, isnan
import os
from os import listdir
from os.path import isfile, join, isdir
import pandas as pd
import datetime

# from read_single_runtastic_json import read_runtastic_json

"""
Debug mode:
1 - Print json files names
2 - Print json files summary
3 - total measurements summary (same as __str__)
4 - Print parsed data dictionary data(export_dict)
5 - Print DataFrame from generated from dictionary data [(]pd.DataFrame(self.export_dict, columns=self.excel_columns)]
6 - Print yearly summary (total distance, duration, average speed & pace, fastest 10Km, 21.1Km, 42.2Km activities)
7 - Print yearly summary parsed data dictionary data (yearly_top_scores))
"""
DEBUG = 0

# PATH = r"C:\Users\USER\Documents\Python\Runtastic_script_My_PC\Jsons_for_new_Script"
# PATH = r'C:\Users\USER\Documents\Python\Runtastic_script_My_PC\export-20240426-000\Sport-sessions\\'  # _output_path
PATH = r'C:\Users\USER\Documents\Python\Runtastic_script_My_PC\export-20250104-000\Sport-sessions\\'
OUTPUT_DIR_LOCATION = r'C:\Users\USER\Documents\Python\Runtastic_script_My_PC\Excel_and_CSV_new\\'  # _output_path

# Jerusalem Marathon
json_file = r"C:\Users\USER\Documents\Python\Runtastic_script_My_PC\Jsons_for_new_Script\2024-03-08_05-01-39-" \
            r"UTC_b0ba3a9b-a1b9-4bc3-b13c-795d5a2b579e.json"


def decimal_to_time(_decimal_time):
    hours = int(floor(_decimal_time / 60000) / 60)
    minutes = floor(_decimal_time / 60000) % 60
    seconds = floor(((_decimal_time / 60000) - int(
        _decimal_time / 60000)) * 60)  # int(_decimal_time / 60000) == _decimal_time // 60000
    return f"{hours:0>2}:{minutes:0>2}:{seconds:0>2}"


def convert_epoch_cols_to_hh_mm_ss(_df):
    _df["max_1km"] = _df["max_1km"].apply(decimal_to_time)
    _df["max_5km"] = _df["max_5km"].apply(decimal_to_time)
    _df["max_10km"] = _df["max_10km"].apply(decimal_to_time)
    _df["max_21_1km"] = _df["max_21_1km"].apply(decimal_to_time)
    _df["max_42_2km"] = _df["max_42_2km"].apply(decimal_to_time)


def change_df_columns_types(_df):
    # _df["duration_decimal_ms"] = _df["duration_decimal_ms"].astype(float)
    _df["distance"] = _df["distance"].astype(float)
    _df["calories"] = _df["calories"].astype(int)
    _df["average_speed"] = _df["average_speed"].astype(float)


class Runtastic_Data_To_Csv:
    def __init__(self, _files_path='', _output_path=''):
        self.json_files_path = _files_path
        self.files_in_dir = ""
        self.output_path = _output_path
        self.date_for_folder = ""
        self.date_for_file = ""
        self.num_of_running_files = 0
        self.sport_type_id = '0'
        self.last_activity_date = 'N/A'
        self.date = '0'
        self.year_month = '0'
        self.start_time = '0'
        self.start_time_dec = 0
        self.end_time = '0'
        self.duration = '0'
        self.duration_decimal = '0'
        self.duration_decimal_ms = '0'
        self.duration_2 = '0'
        self.calories = '0'
        self.distance = '0'
        self.average_speed = '0'
        self.average_pace = '0'
        self.max_speed = '0'
        self.max_1km = '00:00:00'
        self.max_5km = '00:00:00'
        self.max_10km = '00:00:00'
        self.max_10km_dec = 0
        self.fastest_max_10km = 3000000
        self.fastest_10km_date = ''
        self.max_21_1km = '00:00:00'
        self.max_21_1km_dec = 0
        self.fastest_max_21_1km = 6000000
        self.fastest_21_1km_date = ''
        self.max_42_2km = '00:00:00'
        self.max_42_2km_dec = 0
        self.fastest_max_42_2km = 12000000
        self.fastest_42_2km_date = ''
        self.max_heart_rate = '0'
        self.ave_heart_rate = '0'
        self.json_data_content = {}
        #
        self.export_dict = {}
        self.excel_columns = ['start_time', 'end_time', 'duration_decimal', 'duration', 'distance', 'average_pace',
                              'average_speed', 'max_speed', 'max_heart_rate', 'ave_heart_rate', 'calories',
                              'max_1km', 'max_5km', 'max_10km', 'max_21_1km', 'max_42_2km']

        self.excel_columns_raw = self.excel_columns + ['max_10km_dec', 'max_21_1km_dec', 'max_42_2km_dec',
                                                       'start_time_dec', 'duration_decimal_ms', 'year_month']
        for element in self.excel_columns_raw:
            self.export_dict[element] = []
        self.df = pd.DataFrame()
        #
        self.year = '0'
        self.yearly_running_distance = 0
        self.yearly_running_duration = 0
        self.yearly_running_duration_decimal = 0
        self.average_speed_Km_h = ''
        self.average_pace_min_Km = ''
        self.fastest_10Km_1 = ''
        self.fastest_10Km_2 = ''
        self.fastest_10Km_3 = ''
        self.Longest_run_1 = ''
        self.Longest_run_2 = ''
        self.Longest_run_3 = ''
        self.Best_21_1 = ''
        self.fastest_pace = 0
        self.fastest_speed = 0
        self.yearly_top_scores = {}
        self.yearly_top_scores_columns = ["year", "yearly running distance", "yearly running duration",
                                          "average speed [Km/h]", "average pace [min/Km]",
                                          "fastest 10Km 1", "fastest 10Km 2", "fastest 10Km 3",
                                          "Longest run 1", "Longest run 2", "Longest run 3", "Best 21.1"]
        for element in self.yearly_top_scores_columns:
            self.yearly_top_scores[element] = []
        #
        # with open(self.json_file, 'r', encoding="utf8") as json_data:
        #     self.json_data_content = json.load(json_data)

    def create_output_folder(self):
        now = datetime.datetime.now()
        self.date_for_folder = now.strftime('%Y_%m_%d')
        if not os.path.exists(self.output_path + self.date_for_folder):
            os.makedirs(self.output_path + self.date_for_folder)

    def create_files_list(self):
        self.files_in_dir = [f for f in listdir(self.json_files_path) if isfile(join(self.json_files_path, f))]

    def reset_data(self):
        self.sport_type_id = '0'
        self.date = '0'
        self.year_month = '0'
        self.start_time = '0'
        self.start_time_dec = 0
        self.end_time = '0'
        self.duration = '0'
        self.duration_decimal = '0'
        self.duration_decimal_ms = '0'
        self.duration_2 = '0'
        self.calories = '0'
        self.distance = '0'
        self.average_speed = '0'
        self.average_pace = '0'
        self.max_speed = '0'
        self.max_1km = '00:00:00'
        self.max_5km = '00:00:00'
        self.max_10km = '00:00:00'
        self.max_10km_dec = 0
        self.max_21_1km = '00:00:00'
        self.max_21_1km_dec = 0
        self.max_42_2km = '00:00:00'
        self.max_42_2km_dec = 0
        self.max_heart_rate = '0'
        self.ave_heart_rate = '0'

    def time_and_distance(self):
        self.date = strftime('%m-%d-%Y', localtime(self.json_data_content["start_time"] / 1000))
        self.year_month = strftime('%Y-%m', localtime(self.json_data_content["start_time"] / 1000))
        self.start_time = strftime('%Y-%m-%d %H:%M:%S', localtime(self.json_data_content["start_time"] / 1000))
        self.start_time_dec = self.json_data_content["start_time"]
        self.end_time = strftime('%Y-%m-%d %H:%M:%S', localtime(self.json_data_content["end_time"] / 1000))
        self.duration_decimal = '%.2f' % (self.json_data_content["duration"] / 60000)
        self.duration_decimal_ms = self.json_data_content["duration"]
        duration_h = int(floor(self.json_data_content["duration"] / 60000) / 60)
        duration_min = floor(self.json_data_content["duration"] / 60000) % 60
        duration_sec = floor(
            (self.json_data_content["duration"] / 60000 - floor(self.json_data_content["duration"] / 60000)) * 60)
        self.duration = f"{duration_h:0>2}:{duration_min:0>2}:{duration_sec:0>2}"
        self.calories = f'{self.json_data_content["calories"]}'

    def distance_and_heart_rate(self):
        for dicts in self.json_data_content["features"]:
            if "type" in dicts and "initial_values" in dicts['type']:
                duration_h = int(floor(dicts["attributes"]["duration"] / 60000) / 60)
                duration_min = floor(dicts["attributes"]["duration"] / 60000) % 60
                duration_sec = floor(
                    (dicts["attributes"]["duration"] / 60000 - floor(dicts["attributes"]["duration"] / 60000)) * 60)
                self.duration_2 = f"{duration_h:0>2}:{duration_min:0>2}:{duration_sec:0>2}"
                if "distance" in dicts["attributes"]:
                    self.distance = f'{dicts["attributes"]["distance"] / 1000}'
        for dicts in self.json_data_content["features"]:
            if "type" in dicts and "heart_rate" in dicts['type']:
                self.max_heart_rate = f'{dicts["attributes"]["maximum"]}'
                self.ave_heart_rate = f'{dicts["attributes"]["average"]}'

    def speed_and_pace(self):
        for dicts in self.json_data_content["features"]:
            if "type" in dicts and "track_metrics" in dicts['type']:
                speed_factor = 3600 / 1000
                # average_speed
                ave_speed = float(dicts["attributes"]["average_speed"]) * speed_factor
                self.average_speed = f"{('%.2f' % ave_speed):0>5}"
                # average_pace = min_per_km
                minutes = (float(dicts["attributes"]["average_pace"]) * (1000 / 60))
                seconds = floor((minutes - int(minutes)) * 60)
                self.average_pace = f"00:{int(minutes):0>2}:{seconds:0>2}"
                # max_speed. NA for treadmill
                if "max_speed" in dicts["attributes"]:
                    max_speed = float(dicts["attributes"]["max_speed"]) * speed_factor
                    self.max_speed = f"{('%.2f' % max_speed):0>5}"

    def fastest_segments(self):
        for dicts in self.json_data_content["features"]:
            if "type" in dicts and "fastest_segments" in dicts['type']:
                top_speed = dicts["attributes"]["segments"]
                if len(top_speed) > 0:
                    self.max_1km = decimal_to_time(top_speed[0]["duration"])
                if len(top_speed) >= 4:
                    self.max_5km = decimal_to_time(top_speed[3]["duration"])
                if len(top_speed) >= 5:
                    self.max_10km = decimal_to_time(top_speed[4]["duration"])
                    self.max_10km_dec = top_speed[4]["duration"]
                    if top_speed[4]["duration"] < self.fastest_max_10km:
                        self.fastest_max_10km = top_speed[4]["duration"]
                        self.fastest_10km_date = self.date
                if len(top_speed) >= 6:
                    self.max_21_1km = decimal_to_time(top_speed[5]["duration"])
                    self.max_21_1km_dec = top_speed[5]["duration"]
                    if top_speed[5]["duration"] < self.fastest_max_21_1km:
                        self.fastest_max_21_1km = top_speed[5]["duration"]
                        self.fastest_21_1km_date = self.date
                if len(top_speed) >= 7:
                    self.max_42_2km = decimal_to_time(top_speed[6]["duration"])
                    self.max_42_2km_dec = top_speed[6]["duration"]
                    if top_speed[6]["duration"] < self.fastest_max_42_2km:
                        self.fastest_max_42_2km = top_speed[6]["duration"]
                        self.fastest_42_2km_date = self.date
                break   # exit the loop after finding the "fastest_segments"

    def append_data_to_dict(self):
        if self.distance != "0":
            self.export_dict['year_month'].append(self.year_month)
            self.export_dict['start_time'].append(self.start_time)
            self.export_dict['start_time_dec'].append(self.start_time_dec)
            self.export_dict['end_time'].append(self.end_time)
            self.export_dict['duration'].append(self.duration)
            self.export_dict['duration_decimal'].append(self.duration_decimal)
            self.export_dict['duration_decimal_ms'].append(self.duration_decimal_ms)
            self.export_dict['calories'].append(self.calories)
            self.export_dict['distance'].append(self.distance)
            self.export_dict['max_heart_rate'].append(self.max_heart_rate)
            self.export_dict['ave_heart_rate'].append(self.ave_heart_rate)
            self.export_dict['average_speed'].append(self.average_speed)
            self.export_dict['average_pace'].append(self.average_pace)
            self.export_dict['max_speed'].append(self.max_speed)
            self.export_dict['max_1km'].append(self.max_1km)
            self.export_dict['max_5km'].append(self.max_5km)
            self.export_dict['max_10km'].append(self.max_10km)
            self.export_dict['max_10km_dec'].append(self.max_10km_dec)
            self.export_dict['max_21_1km'].append(self.max_21_1km)
            self.export_dict['max_21_1km_dec'].append(self.max_21_1km_dec)
            self.export_dict['max_42_2km'].append(self.max_42_2km)
            self.export_dict['max_42_2km_dec'].append(self.max_42_2km_dec)
            self.num_of_running_files += 1

    def get_data(self):
        self.create_files_list()
        for file in self.files_in_dir:
            self.reset_data()
            with open(self.json_files_path + "\\" + file, 'r', encoding="utf8") as json_data:
                self.json_data_content = json.load(json_data)
            self.sport_type_id = f'{self.json_data_content["sport_type_id"]}'
            if self.sport_type_id == "1":
                self.time_and_distance()
                self.distance_and_heart_rate()
                self.speed_and_pace()
                self.fastest_segments()
                self.append_data_to_dict()
                #
                if DEBUG == 1:
                    print("*" * 30 + f"{file: ^73}" + 30 * "*")
                if DEBUG == 2:
                    print(self.print_data(file))
        self.last_activity_date = self.date     # get the date of the last aactivity
        if DEBUG == 3:
            distance_float = [float(x) for x in self.export_dict['distance']]
            duration_decimal = [float(y) for y in self.export_dict['duration_decimal']]
            print(f"Total distance: \t\t{'%.2f' % (sum(distance_float)):>5}")
            total_duration = sum(distance_float)
            hours = int(floor(total_duration) / 60)
            minutes = floor(total_duration) % 60
            seconds = floor((total_duration - int(total_duration)) * 60)
            print(f"Total duration: \t\t{hours:0>2}:{minutes:0>2}:{seconds:0>2}")
            print(f"Total average pace: \t{'%.2f' % (60 * (sum(distance_float) / sum(duration_decimal))):>5}")
            # print(f"Total average speed:\t{'%.2f' % (sum(duration_decimal)/sum(distance_float)):>5}")
            ave_speed_dec = (sum(duration_decimal) / sum(distance_float))
            minutes = int(ave_speed_dec)
            seconds = '%2.0f' % ((ave_speed_dec % minutes) * 60)
            print(f"Total average speed:\t{minutes :>2}:{seconds :0>2}")
            print(f"\n{'  Fastest runs:  ':*^45}")
            fastest_max_10km_time = decimal_to_time(self.fastest_max_10km)
            print(f"Fastest 10Km:\t\t\t{fastest_max_10km_time} @ {self.fastest_10km_date}")
            fastest_max_21_1km_time = decimal_to_time(self.fastest_max_21_1km)
            print(f"Fastest 21.1Km:\t\t\t{fastest_max_21_1km_time} @ {self.fastest_21_1km_date}")
            fastest_max_42_2km_time = decimal_to_time(self.fastest_max_42_2km)
            print(f"Fastest 42.2Km:\t\t\t{fastest_max_42_2km_time} @ {self.fastest_42_2km_date}")
            print(f"{'':*^45}\n")

        if DEBUG == 4:
            for key, data in self.export_dict.items():
                print(key, data, len(data))
        df = pd.DataFrame(self.export_dict, columns=self.excel_columns)
        if DEBUG == 5:
            print(df)

    def print_data(self, _file_name):
        if self.sport_type_id == "1":
            return "*" * 30 + f"{_file_name: ^73}" + 30 * "*" \
                   + "\nstart_time\t\t" + self.start_time \
                   + "\nend_time\t\t" + self.end_time \
                   + "\nduration\t\t" + self.duration \
                   + "\ncalories\t\t" + self.calories \
                   + "\ndistance [Km]\t" + self.distance \
                   + "\nave_heart_rate\t" + self.ave_heart_rate \
                   + "\nmax_heart_rate\t" + self.max_heart_rate \
                   + "\naverage_speed\t" + self.average_speed \
                   + "\naverage_pace\t" + self.average_pace \
                   + "\nmax_speed\t\t" + self.max_speed \
                   + "\n1km     -->\t\t" + self.max_1km \
                   + "\n5km     -->\t\t" + self.max_5km \
                   + "\n10km    -->\t\t" + self.max_10km \
                   + "\n21_1km  -->\t\t" + self.max_21_1km \
                   + "\n42_2km  -->\t\t" + self.max_42_2km
        else:
            return "Not a running activity"

    def create_raw_dataframe_form_list(self):
        self.df = pd.DataFrame(self.export_dict, columns=self.excel_columns_raw)
        change_df_columns_types(self.df)

    def export_to_csv(self):
        now = datetime.datetime.now()
        self.date_for_file = now.strftime('%Y-%m-%d_T_%H_%M_%S')
        export_df = pd.DataFrame(self.export_dict, columns=self.excel_columns)
        change_df_columns_types(export_df)
        export_df.to_csv(self.output_path + self.date_for_folder + r'/' + self.date_for_file + '_Runtastic_Boaz.csv',
                         index=False, header=True)
        # print("=====", self.output_path + self.date_for_folder + r'/' + self.date_for_file + '_Runtastic_Boaz.csv')
        print("Number of 'running' files =", f'{self.num_of_running_files:^18}')
        print("Generated Runtastic CSV path:\t", self.output_path[:-1] + self.date_for_folder +
              '\nCSV File Name:\t\t\t\t\t', self.date_for_file + '_Runtastic_Boaz.csv')
        print(120 * '-')

    @staticmethod
    def start_time_message():
        now = datetime.datetime.now()
        print(120 * '-')
        print(now.strftime('%Y-%m-%d_@_%H:%M:%S'), 'Start processing')
        print(120 * '-')

    @staticmethod
    def end_time_message():
        now = datetime.datetime.now()
        print(now.strftime('%Y-%m-%d_@_%H:%M:%S'), 'CSV is ready')
        print(120 * '-')

    @staticmethod
    def end_time_data_summary_message():
        now = datetime.datetime.now()
        print(now.strftime('%Y-%m-%d_@_%H:%M:%S'), 'Finished processing')
        print(120 * '-')

    def execute(self, mode=0):
        """
        :param mode:
        0 - Generate both detailed activities data & yearly distance and top results
        1 - All Detailed activities data
        2 - Generate yearly distance and top results
        :return: None
        """

        self.start_time_message()
        self.create_output_folder()
        self.get_data()
        self.create_raw_dataframe_form_list()
        if mode == 0:
            self.get_year_distance()
            self.export_to_csv()
        elif mode == 1:
            self.export_to_csv()
        else:
            self.get_year_distance()
        self.end_time_message()

    def append_data_to_yearly_top_scores_dict(self):
        self.yearly_top_scores["year"].append(self.year)
        self.yearly_top_scores["yearly running distance"].append(self.yearly_running_distance)
        self.yearly_top_scores["yearly running duration"].append(self.yearly_running_duration)
        self.yearly_top_scores["average speed [Km/h]"].append(self.average_speed_Km_h + ' Km/h')
        self.yearly_top_scores["average pace [min/Km]"].append(self.average_pace_min_Km + ' min/Km')
        self.yearly_top_scores["fastest 10Km 1"].append(self.fastest_10Km_1 + ' min')
        self.yearly_top_scores["fastest 10Km 2"].append(self.fastest_10Km_2 + ' min')
        self.yearly_top_scores["fastest 10Km 3"].append(self.fastest_10Km_3 + ' min')
        self.yearly_top_scores["Longest run 1"].append(self.Longest_run_1 + ' Km')
        self.yearly_top_scores["Longest run 2"].append(self.Longest_run_2 + ' Km')
        self.yearly_top_scores["Longest run 3"].append(self.Longest_run_3 + ' Km')
        self.yearly_top_scores["Best 21.1"].append(self.Best_21_1 + ' m')

    def get_year_distance(self):
        current_year = "2014"
        now = datetime.datetime.now().strftime('%Y')
        while int(current_year) <= int(now):
            year_distance = self.df[self.df["start_time"].str.contains(current_year)][["distance"]].astype(float)
            # year_best_10k_top_3 = self.df[(self.df["start_time"].str.contains(current_year)) &
            #                               (self.df["distance"].astype(float) > 10)][
            #     ["duration_decimal"]].astype(float)["duration_decimal"].nsmallest(3)
            year_best_10k_top_3 = self.df[(self.df["start_time"].str.contains(current_year)) &
                                          (self.df["distance"].astype(float) > 10)]
            year_best_10k_top_3 = year_best_10k_top_3[["duration_decimal"]].astype(float)["duration_decimal"]
            year_best_10k_top_3 = year_best_10k_top_3.nsmallest(3)
            year_best_10k_top_3_list = list(year_best_10k_top_3.reset_index()['duration_decimal'])
            temp = len(year_best_10k_top_3_list)
            for i in range(3 - temp):
                year_best_10k_top_3_list.append(0)
            year_best_21_1 = self.df[(self.df["start_time"].str.contains(current_year)) &
                                     (self.df["distance"].astype(float) > 21.1)][
                ["duration_decimal"]].astype(float)["duration_decimal"].min()
            if str(year_best_21_1) == "nan":
                year_best_21_1 = 0
            year_duration = self.df[self.df["start_time"].str.contains(current_year)][
                ["duration_decimal"]].astype(float)

            self.fastest_speed = self.df[self.df["start_time"].str.contains(current_year)][
                ["average_speed"]].astype(float)["average_speed"].max()
            self.fastest_pace = 60 / self.fastest_speed
            longest_run_top_3 = self.df[self.df["start_time"].str.contains(current_year)][
                ["distance"]].astype(float)["distance"].nlargest(3)
            #
            longest_run_top_3_list = list(longest_run_top_3.reset_index()['distance'])
            temp = len(longest_run_top_3_list)
            for i in range(3 - temp):
                longest_run_top_3_list.append(0)
            self.year = current_year
            self.yearly_running_distance = year_distance['distance'].sum()
            self.yearly_running_duration = decimal_to_time(year_duration['duration_decimal'].sum() * 60000)
            self.yearly_running_duration_decimal = year_duration['duration_decimal'].sum()
            if year_duration['duration_decimal'].sum() != 0 or year_distance['distance'].sum() != 0:
                self.average_speed_Km_h = '%.2f' % (
                            year_distance['distance'].sum() / (year_duration['duration_decimal'].sum() / 60))
                self.average_pace_min_Km = decimal_to_time(
                    (year_duration['duration_decimal'].sum() / year_distance['distance'].sum()) * 60000)[3:]
            else:
                self.average_speed_Km_h = '00.00'
                self.average_pace_min_Km = '00:00:00'[3:]
            self.Longest_run_1 = '%.2f' % longest_run_top_3_list[0]
            self.Longest_run_2 = '%.2f' % longest_run_top_3_list[1]
            self.Longest_run_3 = '%.2f' % longest_run_top_3_list[2]
            self.fastest_10Km_1 = decimal_to_time(year_best_10k_top_3_list[0] * 60000)[3:]
            self.fastest_10Km_2 = decimal_to_time(year_best_10k_top_3_list[1] * 60000)[3:]
            self.fastest_10Km_3 = decimal_to_time(year_best_10k_top_3_list[2] * 60000)[3:]
            self.Best_21_1 = decimal_to_time(year_best_21_1 * 60000)
            self.append_data_to_yearly_top_scores_dict()
            current_year = str(int(current_year) + 1)
            # Print year summary:
            if DEBUG == 6:
                self.print_year_summary()
        # pandas dataframe for csv export
        self.export_year_summary_to_csv()
        if DEBUG == 7:
            print(self.yearly_top_scores)
        # self.pandas_learn()

    def print_year_summary(self):
        print(f"{'current_year:':40}{self.year}")
        print(f"{'Total running distance: ':40}{'%.2f' % self.yearly_running_distance}")
        print(f"{'Total running duration: ':40}{self.yearly_running_duration}")
        if self.yearly_running_duration_decimal != 0 or self.yearly_running_distance != 0:
            average_speed = self.yearly_running_distance / (self.yearly_running_duration_decimal / 60)
            print(f"{'Yearly average speed [Km/h]: ':40}{'%.2f' % average_speed}")
            average_pace = decimal_to_time(
                (self.yearly_running_duration_decimal / self.yearly_running_distance) * 60000)
            print(f"{'Yearly average pace [min/Km]':40}{average_pace[3:]:>5}")
        else:
            print(f"{'Yearly average speed [Km/h]: ':40}{'00.00'}")
            print(f"{'Yearly average pace [min/Km]:':40}{'00:00'}")
        if str(self.fastest_speed) == 'nan':
            print(f"{'Fastest speed of the year [Km/h]: ':40}{'00.00'}")
        else:
            print(f"{'Fastest speed of the year [Km/h]: ':40}{'%.2f' % self.fastest_speed:0<5}")
        if str(self.fastest_pace) == 'nan':
            self.fastest_pace = 0
        print(f"{'Fastest pace of the year [min/Km]: ':40}{decimal_to_time(self.fastest_pace * 60000)[3:]:>5}")
        print(f"{'Top 3 longest runs of the year 1: ':40}{self.Longest_run_1} Km")
        print(f"{'Top 3 longest runs of the year 2: ':40}{self.Longest_run_2} Km")
        print(f"{'Top 3 longest runs of the year 3: ':40}{self.Longest_run_3} Km")
        print(f"{'Top 3 fastest 10Km runs of the year 1: ':40}{self.fastest_10Km_1} min")
        print(f"{'Top 3 fastest 10Km runs of the year 2: ':40}{self.fastest_10Km_2} min")
        print(f"{'Top 3 fastest 10Km runs of the year 3: ':40}{self.fastest_10Km_3} min")
        print(f"{'Best 21.1 running activity of the year: ':40}{self.Best_21_1} min")
        print("*" * 70)

    def pandas_learn(self):
        print('^' * 100)
        # pandas: change type of one column within dataframe [and not affecting other rows]
        print("dtype before:", self.df["distance"].dtype)
        self.df["distance"] = self.df["distance"].astype(float)
        print("dtype after: ", self.df["distance"].dtype)
        # pandas: find index values of nlargest and print rows based on index # values
        ind_val = self.df[self.df["start_time"].str.contains('2024')]["distance"].astype(float).nlargest(3).index.values
        print(ind_val)
        # pandas: get rows based on index values
        print(self.df.loc[ind_val])  # [["start_time", "distance"]])
        # pandas: to deleted column from dataframe
        df_w_deleted_col = self.df.loc[ind_val].reset_index().drop('index', axis=1)
        print(df_w_deleted_col)
        longest_run = self.df[self.df["start_time"].str.contains('2024')][["distance"]].astype(float)["distance"].max()
        print("longest_run:", longest_run)
        print('^' * 100)

    def export_year_summary_to_csv(self, transpose=0):
        """

        :param transpose: transpose columns-rows of the generated yearly results and top results csv
        :return: None; generates csv
        """
        now = datetime.datetime.now()
        self.date_for_file = now.strftime('%Y-%m-%d_T_%H_%M_%S')
        year_summary_df = pd.DataFrame(self.yearly_top_scores, columns=self.yearly_top_scores_columns)
        if transpose == 1:
            year_summary_df = year_summary_df.transpose().reset_index()  # transpose table columns-rows
        year_summary_df.to_csv(self.output_path + self.date_for_folder + r'/' + self.date_for_file +
                               '_Runtastic_year_summary_Boaz.csv', index=False, header=True)
        print("Generated Runtastic CSV path:\t", self.output_path[:-1] + self.date_for_folder +
              '\nCSV File Name:\t\t\t\t\t', self.date_for_file + '_Runtastic_year_summary_Boaz.csv')
        print(120 * '-')

    # def per_year_distance(self, _year):
    #     year_distance = self.df[self.df["start_time"].str.contains(str(_year))][["distance"]].astype(float)
    #     total_running_km = year_distance['distance'].sum()
    #     return total_running_km
    #     # print("*-*" * 20, total_running_km, "*-*" * 20)
    #
    # def per_year_best_10k(self, _year, _num_of_runs):
    #     year_best_10ks = self.df[(self.df["start_time"].str.contains(str(_year))) &
    #                                   (self.df["distance"].astype(float) > 10)]
    #     year_best_10ks = year_best_10ks[["duration_decimal"]].astype(float)["duration_decimal"]
    #     year_best_10ks = year_best_10ks.nsmallest(_num_of_runs)
    #     year_best_10ks_list = list(year_best_10ks.reset_index()['duration_decimal'])
    #     temp = len(year_best_10ks_list)
    #     for i in range(_num_of_runs - temp):
    #         year_best_10ks_list.append(0)
    #     for i in range(len(year_best_10ks_list)):
    #         year_best_10k = decimal_to_time(year_best_10ks_list[i] * 60000)
    #         if year_best_10k[1] != "0":
    #             year_best_10ks_list[i] = year_best_10k[1:]
    #         else:
    #             year_best_10ks_list[i] = year_best_10k[3:]
    #     return year_best_10ks_list

    def __str__(self):
        if self.sport_type_id != "00":
            distance_float = [float(x) for x in self.export_dict['distance']]
            duration_decimal = [float(y) for y in self.export_dict['duration_decimal']]
            total_duration_dec = sum(duration_decimal)
            hours = int(floor(total_duration_dec) / 60)
            minutes = floor(total_duration_dec) % 60
            seconds = floor((total_duration_dec - int(total_duration_dec)) * 60)
            total_duration_time = f"{int(hours / 24)} days and {(hours % 24):0>2}:{minutes:0>2}:{seconds:0>2} --> " + \
                                  f"{hours:0>2}:{minutes:0>2}:{seconds:0>2}"
            average_pace = f"{'%.2f' % (60 * (sum(distance_float) / sum(duration_decimal))):>5}"
            ave_speed_dec = (sum(duration_decimal) / sum(distance_float))
            minutes = int(ave_speed_dec)
            seconds = '%2.0f' % ((ave_speed_dec % minutes) * 60)
            average_speed = f"{minutes :>2}:{seconds :0>2}"
            fastest_max_10km_time = decimal_to_time(self.fastest_max_10km)
            fastest_max_21_1km_time = decimal_to_time(self.fastest_max_21_1km)
            fastest_max_42_2km_time = decimal_to_time(self.fastest_max_42_2km)
            #
            return f"Total distance: \t\t{'%.2f' % (sum(distance_float)):>5} Km\n" \
                   + f"Total duration: \t\t{total_duration_time}\n" \
                   + f"Total average pace: \t{average_pace} Km/h\n" \
                   + f"Total average speed:\t{average_speed} min/Km\n" \
                   + f"{'  Fastest runs:  ':*^45}\n" \
                   + f"Fastest 10Km:\t\t\t{fastest_max_10km_time} @ {self.fastest_10km_date}\n" \
                   + f"Fastest 21.1Km:\t\t\t{fastest_max_21_1km_time} @ {self.fastest_21_1km_date}\n" \
                   + f"Fastest 42.2Km:\t\t\t{fastest_max_42_2km_time} @ {self.fastest_42_2km_date}\n" \
                   + f"{45 * '*'}"
        else:
            return "Error"


# class runtastic_data_filter(Runtastic_Data_To_Csv):
#     pass

if __name__ == "__main__":
    analyze_data = Runtastic_Data_To_Csv(_files_path=PATH, _output_path=OUTPUT_DIR_LOCATION)
    analyze_data.execute(mode=0)

    print(analyze_data)

    # read_runtastic_json(json_file)
