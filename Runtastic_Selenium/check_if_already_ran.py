import time
import os

EXPORT_LAST_RUN_FILE = "control/export_last_run.txt"
DOWNLOAD_LAST_RUN_FILE = "control/download_last_run.txt"
LAST_DOWNLOAD_PATH = "control/last_download_path.txt"
THRESHOLD = 3 * 24 * 60 * 60  # 3 days in seconds


def has_run_recently(last_run_file):
    if os.path.exists(last_run_file):
        with open(last_run_file, "r") as f:
            last_run = float(f.read().strip())
        return (time.time() - last_run) < THRESHOLD
    return False


def update_last_run(last_run_file=EXPORT_LAST_RUN_FILE):
    if not os.path.exists("control"):
        os.makedirs("control")
    with open(last_run_file, "w") as f:
        f.write(str(time.time()))


def remove_last_run_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"{file_path} was removed")
    else:
        print(f"{file_path} does not exist")


def save_last_download_path(_path):
    if not os.path.exists("control"):
        os.makedirs("control")
    with open(LAST_DOWNLOAD_PATH, "w") as f:
        f.write(_path)

def my_function():
    if has_run_recently(EXPORT_LAST_RUN_FILE):
        print("Function already ran in the last 3 days. Skipping execution.")
        return

    print("Executing function...")
    # Your function logic here

    update_last_run()  # Store the last execution time


if __name__ == "__main__":
    my_function()
