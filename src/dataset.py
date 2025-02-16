import pandas as pd
from glob import glob

# --------------------------------------------------------------
# Read single CSV file
# --------------------------------------------------------------

single_file_accel = pd.read_csv(
    "../../demo-project/src/data/raw/MetaMotion/A-bench-heavy2-rpe8_MetaWear_2019-01-11T16.10.08.270_C42732BE255C_Accelerometer_12.500Hz_1.4.4.csv"
)

single_file_gyro = pd.read_csv(
    "../../demo-project/src/data/raw/MetaMotion/A-bench-heavy2-rpe8_MetaWear_2019-01-11T16.10.08.270_C42732BE255C_Gyroscope_25.000Hz_1.4.4.csv"
)
# --------------------------------------------------------------
# List all data in data/raw/MetaMotion
# --------------------------------------------------------------

files = glob("../../demo-project/src/data/raw/MetaMotion/*.csv")
len(files)

# --------------------------------------------------------------
# Extract features from filename
# --------------------------------------------------------------

data_path = "../../demo-project/src/data/raw/MetaMotion/"
f = files[0]

# split and take in the first text chunk (Participant key)
participant = f.split("/")[-1].split("-")[0]
# the exercise
label = f.split("/")[-1].split("-")[1]
# intensity - takes away the last character if its 1,2,3
category = f.split("/")[-1].split("-")[2].rstrip("123").rstrip("_MetaWear_2019")

df = pd.read_csv(f)
df["participant"] = participant
df["label"] = label
df["category"] = category

# --------------------------------------------------------------
# Read all files
# --------------------------------------------------------------

acc_df = []
gyr_df = []

acc_set = 1
gyr_set = 1

for f in files:
    participant = f.split("/")[-1].split("-")[0]
    label = f.split("/")[-1].split("-")[1]
    category = f.split("/")[-1].split("-")[2].rstrip("123").rstrip("_MetaWear_2019")
    print(category)
    df = pd.read_csv(f)
    df["participant"] = participant
    df["label"] = label
    df["category"] = category

# --------------------------------------------------------------
# Working with datetimes
# --------------------------------------------------------------


# --------------------------------------------------------------
# Turn into function
# --------------------------------------------------------------


# --------------------------------------------------------------
# Merging datasets
# --------------------------------------------------------------


# --------------------------------------------------------------
# Resample data (frequency conversion)
# --------------------------------------------------------------

# Accelerometer:    12.500HZ
# Gyroscope:        25.000Hz


# --------------------------------------------------------------
# Export dataset
# --------------------------------------------------------------
