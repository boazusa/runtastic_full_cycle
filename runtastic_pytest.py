# Main Python Pytest script.

import time
from datetime import datetime
import pytest
from Runtastic_Selenium import Selenium_Runtastic, args_parser
from runtastic_analysis import runtastic_data_filter, Runtastic_Data_To_Csv, OUTPUT_DIR_LOCATION



def run_pytest():
    current_time = time.time()
    date = f"{datetime.fromtimestamp(float(current_time)).strftime('%Y-%m-%d_%H_%M_%S')}"
    pytest.main(['runtastic_analysis/Test_Runtastic_Pytest.py', "-v", "--showlocals", "--self-contained-html",
                 f"--html=reports/{date}_Test_Runtastic_Pytest_report.html"])  # ,
    # "--cov=runtastic_backend_functions", "--cov=read_runtastic_json", "--cov-report=html"])


if __name__ == '__main__':
    run_pytest()

