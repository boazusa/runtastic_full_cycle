
import datetime
import os
import time
import pandas as pd
from . import read_runtastic_json
from . import runtastic_backend_functions
import pytest

PATH = r'C:\Users\USER\Documents\Python\Runtastic_script_My_PC\export-20250104-000\Sport-sessions\\'
OUTPUT_DIR_LOCATION = r'C:\Users\USER\Documents\Python\Runtastic_script_My_PC\Excel_and_CSV_new\\'  # _output_path

def get_last_download_path():
    # Get the current script directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Move one directory up
    parent_dir = os.path.dirname(current_dir)
    # Construct the relative file path
    last_run_file = os.path.join(parent_dir, r"control\last_download_path.txt")
    #
    print(last_run_file)
    if os.path.exists(last_run_file):
        with open(last_run_file, "r") as f:
            return str(f.read().strip())
    return None


@pytest.fixture(scope="session")
def runtastic_fixture():
    path = get_last_download_path()
    if not path:
        path = PATH
    test = runtastic_backend_functions.runtastic_data_filter(_files_path=path, _output_path=OUTPUT_DIR_LOCATION)
    test.create_main_dataframe()
    return test


def test_raw_dataframe(runtastic_fixture):
    assert len(runtastic_fixture.df.columns) == len(runtastic_fixture.excel_columns_raw)
    assert runtastic_fixture.df.shape[1] == 22
    assert runtastic_fixture.df.shape[0] > 1000


@pytest.mark.parametrize("year", ["2022", "2023", "2024"])
def test_yearly_activities(runtastic_fixture, year):
    assert len(runtastic_fixture.df[runtastic_fixture.df["start_time"].str.contains(str(year))]) > 150

def test_total_distance(runtastic_fixture):
    assert float(runtastic_fixture.total_distance()) > 10000, f'expected more than 10000Km of total run, but ' \
                                                            f'got {runtastic_fixture.total_distance()}Km'

@pytest.mark.parametrize("year, distance", [["2022", 1800], ["2023", 2000], ["2024", 2400]])
def test_yearly_distance(runtastic_fixture, year, distance):
    assert float(runtastic_fixture.per_year_distance(year)) > distance, f'expected more than {distance}Km ' \
                                                                        f'of total run in {year}, but got ' \
                                                                        f'{runtastic_fixture.per_year_distance(year)}Km'

def test_per_year_calories(runtastic_fixture):
    assert runtastic_fixture.per_year_calories(2017) == 0  # no running activity was done on 2017
    assert runtastic_fixture.per_year_calories(2024) > runtastic_fixture.per_year_calories(2023)
    assert runtastic_fixture.per_year_calories(2023) > 150000, f'expected more than 150000 total Cals in 2023, but' \
                                                               f' got {runtastic_fixture.per_year_calories(2023)}Cals'

def test_per_year_speed(runtastic_fixture):
    assert runtastic_fixture.per_year_speed(2024) > 12, f'average speed in 2024 is expected to be > 12 Km/h but' \
                                                        f' received {runtastic_fixture.per_year_speed(2024) > 12} Km/h'

@pytest.mark.parametrize("year, num", [(2020, 3), (2021, 10), (2022, 5), (2023, 20), (2024, 3), (2025, 9)])
def test_per_year_longest_running(runtastic_fixture, year, num):
    max_yearly_run_activities = len(runtastic_fixture.df[runtastic_fixture.df["start_time"].str.contains(str(year))])
    assert len(runtastic_fixture.per_year_longest_running(year, num)) in [num, max_yearly_run_activities]
    assert len(runtastic_fixture.per_year_longest_running(year, num)[0]) == 3

@pytest.mark.parametrize("year, num", [(2024, 3), (2025, 10)])
def test_per_year_longest_distance(runtastic_fixture, year, num):
    # per_year_longest_running_dis_sorted = runtastic_fixture.per_year_longest_running(year, num)
    # per_year_longest_running_dis_sorted.sort(key=lambda x: x[0])
    # assert per_year_longest_running_dis_sorted[-1][0] > 42.19
    assert sorted(runtastic_fixture.per_year_longest_running(year, num), key=lambda x: x[0])[-1][0] > 42.19

@pytest.mark.parametrize("start, end, num", [(2020, 2022, 3), (2021, 2022,  10), (2023, 2023, 5), (2019, 2024, 20)])
def test_per_every_year_longest_running(runtastic_fixture, start, end, num):
    rows = runtastic_fixture.per_every_year_longest_running(_start_year=start, _end_year=end, _num_of_runs=num)
    rows_num = len(rows)
    columns = len(rows[0])
    assert rows_num == (end - start + 1) * num
    assert columns == 3


attribute_test_list = [["2022", "2024", 'Distance', 3, 2],  # expected_row = 2024 - 2022 + 1 = 3
             ["2018", "2024", 'Calories', 7, 2],
             ["2019", "2019", 'Speed', 1, 2],
             ["2014", "2024", 'Distance', 11, 2],
             ["2014", "2024", 'N/A', 11, 2],                # undefined attribute is defaulted to Distance
             ["2014", "2024", 'Calories', 11, 2],
             ["2014", "2024", 'Speed', 11, 2],
             ["now", "now", 'Speed', 1, 2]]                 # expected_row = current year - current year + 1 = 1

@pytest.mark.parametrize("start, end, attribute, expected_row, expected_col", attribute_test_list)
def  test_per_every_year_attribute(runtastic_fixture, start, end, attribute, expected_row, expected_col):
    df = runtastic_fixture.per_every_year_attribute(_start_year=start, _end_year=end, _attribute=attribute)
    assert df.shape[0] == expected_row
    assert df.shape[1] == expected_col


duration_test_list = [["2018", "2024", 7, 3],
                      ["2019", "2019", 1, 3],
                      ["2014", "2024", 11, 3],
                      ["now", "now", 1, 3]]

@pytest.mark.parametrize("start, end, expected_row, expected_col", duration_test_list)
def test_per_every_year_duration(runtastic_fixture, start, end, expected_row, expected_col):
    arr = runtastic_fixture.per_every_year_duration(_start_year=start, _end_year=end)
    assert len(arr) == expected_row
    assert len(arr[0]) == expected_col


fastest_running_list = [["2017", 7, "max_10km_dec"],                # year, activities #, category length
                        ["2019", 1, "max_10km_dec"],
                        ["2014", 11, "max_21_1km_dec"],
                        ["2024", 11, "max_21_1km_dec"],
                        ["2025", 1, "max_42_2km_dec"]]

@pytest.mark.parametrize("year, num_of_act, distance", fastest_running_list)
def test_per_year_fastest_running(runtastic_fixture, year, num_of_act, distance):
    arr = runtastic_fixture.per_year_fastest_running(_year=year, _num_of_runs=num_of_act, running_distance=distance)
    assert len(arr) == num_of_act
    assert len(arr[0]) == 5


fastest_running_time_list = [["2022", 1, "max_10km_dec", 2400],     # year, activities #, category length, time (sec)
                             ["2023", 1, "max_10km_dec", 2400],
                             ["2024", 1, "max_10km_dec", 2400],
                             ["2023", 1, "max_21_1km_dec", 5400],
                             ["2025", 1, "max_21_1km_dec", 5400],
                             ["2025", 1, "max_42_2km_dec", 10800]]

@pytest.mark.parametrize("year, num_of_act, distance, seconds", fastest_running_time_list)
def test_per_year_fastest_running_times(runtastic_fixture, year, num_of_act, distance, seconds):
    arr = runtastic_fixture.per_year_fastest_running(_year=year, _num_of_runs=num_of_act, running_distance=distance)
    assert (int(arr[0][4]) / 1000) < seconds, f"On {year}, the fastest " \
                                              f"{distance.replace('max_', '').replace('_dec', '')} " \
                                              f"was < {runtastic_backend_functions.decimal_to_time(1000 * seconds)} " \
                                              f"minutes, but the test reported " \
                                              f"{runtastic_backend_functions.decimal_to_time(arr[0][4])} minutes"


marathon_running_list = [["2017", 7, 0], ["2019", 1, 0], ["2024", 11, 2]]

@pytest.mark.parametrize("year, num_of_act, expected_len", marathon_running_list)
def test_per_year_fastest_fastest_42k(runtastic_fixture, year, num_of_act, expected_len):
    arr = runtastic_fixture.per_year_fastest_42k_list(year, num_of_act)
    assert len(arr) == expected_len
    if expected_len != 0:
        assert len(arr[0]) == 5

def test_verify_running_activities_csv_file_was_generated(runtastic_fixture):
    runtastic_fixture.execute(1)
    output_file = runtastic_fixture.output_path + runtastic_fixture.date_for_folder + r'/' + \
                  runtastic_fixture.date_for_file + '_Runtastic_Boaz.csv'
    assert os.path.isfile(output_file), f"{output_file} wasn't generated"
    time.sleep(0.5)
    os.remove(output_file)

def test_verify_running_yearly_summary_csv_file_was_generated(runtastic_fixture):
    runtastic_fixture.execute(2)
    output_file = runtastic_fixture.output_path + runtastic_fixture.date_for_folder + r'/' + \
                  runtastic_fixture.date_for_file + '_Runtastic_year_summary_Boaz.csv'
    assert os.path.isfile(output_file), f"{output_file} wasn't generated"
    time.sleep(0.5)
    os.remove(output_file)

def test_plots_pdf_generation(runtastic_fixture):
    time.sleep(1)
    msg = runtastic_fixture.save_plot_to_pdf()
    msg_lst = msg.split("'")
    output_file = msg_lst[2][14:] + '/' + msg_lst[1]
    time.sleep(0.1)
    assert os.path.isfile(output_file)
    time.sleep(0.5)
    os.remove(output_file)

# @pytest.mark.parametrize("attribute", ['Distance', 'calories', 'Speed'])
# def test_plot_per_every_year_attribute(runtastic_fixture, attribute):
#     time.sleep(1)
#     msg = runtastic_fixture.plot_per_every_year_attribute(_attribute=attribute)
#     file_name = msg.split("'")[1]
#     output_file = msg[80:] + '/' + file_name
#     time.sleep(0.1)
#     assert os.path.isfile(output_file)
#     time.sleep(0.5)
#     os.remove(output_file)
#
# def test_plot_per_every_year_duration(runtastic_fixture):
#     time.sleep(1)
#     msg = runtastic_fixture.plot_per_every_year_duration()
#     file_name = msg.split("'")[1]
#     output_file = msg[80:] + '/' + file_name
#     time.sleep(0.1)
#     assert os.path.isfile(output_file)
#     time.sleep(0.5)
#     os.remove(output_file)
#
#
# @pytest.mark.parametrize("distance", ["max_10km_dec", "max_21_1km_dec", "max_42_2km_dec"])
# def test_plot_per_year_fastest_running(runtastic_fixture, distance):
#     time.sleep(1)
#     msg = runtastic_fixture.plot_per_year_fastest_running(running_distance=distance)
#     file_name = msg.split("'")[1]
#     output_file = msg[80:] + '/' + file_name
#     time.sleep(0.1)
#     assert os.path.isfile(output_file)
#     time.sleep(0.5)
#     os.remove(output_file)
#
# def test_plot_per_every_year_longest_running(runtastic_fixture):
#     time.sleep(1)
#     msg = runtastic_fixture.plot_per_every_year_longest_running()
#     file_name = msg.split("'")[1]
#     output_file = msg[80:] + '/' + file_name
#     time.sleep(0.1)
#     assert os.path.isfile(output_file)
#     time.sleep(0.5)
#     os.remove(output_file)


if __name__ == '__main__':
    pytest.main(['Test_Runtastic_Pytest.py', "-v", "--showlocals",  "--self-contained-html",
                 "--html=reports/Test_Runtastic_Pytest_report.html",
                 "--cov=runtastic_backend_functions", "--cov=read_runtastic_json", "--cov-report=html"])


    #
    # test = runtastic_backend_functions.runtastic_data_filter(_files_path=PATH, _output_path=OUTPUT_DIR_LOCATION)
    # test.create_main_dataframe()
    #

