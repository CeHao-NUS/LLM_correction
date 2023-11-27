
import json
import yaml
import os
import pickle


EXP_DIR = './temp/exp/exp_results.pkl'
ASSIT_DIR = './temp/assist_results/assist_results.txt'
IMAGE_BASE_DIR = './temp/images/'

from datetime import datetime
# Get the current date and time
current_datetime = datetime.now()
# Format as month-day-hour-minute-second
START_TIME = current_datetime.strftime("%m-%d-%H-%M-%S")

# ================ save with time =================
def get_current_time():
    current_datetime = datetime.now()
    # Format as month-day-hour-minute-second
    return current_datetime.strftime("%H-%M-%S")


def save_path_time(file_path):
    directory_parts = file_path.rsplit('/', 1)
    base_path = directory_parts[0]
    filename = directory_parts[1]
    
    # file_name_parts = filename.rsplit('.', 1)
    
    new_directory = os.path.join(base_path, START_TIME)
    if not os.path.exists(new_directory):
        os.makedirs(new_directory)
        print('new_directory', new_directory)
    
    new_file_path = os.path.join(new_directory, get_current_time() + '_' + filename)
    # print('new_file_path', new_file_path)
    return new_file_path

# ================ JSON ================
# JSON file reader
def read_json_file(file_path):
    with open(file_path, 'r') as json_file:
        return json.load(json_file)

# JSON file writer
def write_json_file(file_path, data):
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file)

# convert string to JSON
def convert_str_to_json(str):
    return json.loads(str)

# ================ txt ================
# txt file reader
def read_txt_file(file_path):
    with open(file_path, 'r') as txt_file:
        return txt_file.read()
    
# txt file writer
def write_txt_file(file_path, data):
    with open(file_path, 'w') as txt_file:
        txt_file.write(data)

# ================ yaml ================
# yaml file reader
def read_yaml_file(file_path):
    with open(file_path, 'r') as yaml_file:
        return yaml.safe_load(yaml_file)
    
# yaml file writer
def write_yaml_file(file_path, data):
    with open(file_path, 'w') as yaml_file:
        yaml.safe_dump(data, yaml_file)

# ================ pickle ================
# pickle file reader
def read_pickle_file(file_path):
    with open(file_path, 'rb') as pickle_file:
        return pickle.load(pickle_file)
    
# pickle file writer
def write_pickle_file(file_path, data):
    with open(file_path, 'wb') as pickle_file:
        pickle.dump(data, pickle_file)

# ================ dir ================
def mkdir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

