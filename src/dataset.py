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

acc_df = pd.DataFrame()
gyr_df = pd.DataFrame()

acc_set = 1
gyr_set = 1

for f in files:
    participant = f.split("/")[-1].split("-")[0]
    label = f.split("/")[-1].split("-")[1]
    category = f.split("/")[-1].split("-")[2].rstrip("123").rstrip("_MetaWear_2019")

    df = pd.read_csv(f)

    df["participant"] = participant
    df["label"] = label
    df["category"] = category

    if "Accelerometer" in f:
        df["set"] = acc_set
        acc_df = pd.concat([acc_df, df])
        acc_set += 1

    if "Gyroscope" in f:
        df["set"] = gyr_set
        gyr_df = pd.concat([gyr_df, df])
        gyr_set += 1


acc_df[acc_df["set"] == 1].head()
acc_df.iloc[40]

# --------------------------------------------------------------
# Working with datetimes
# --------------------------------------------------------------

acc_df.info()
# epoch and time are int/object
# need to convert

pd.to_datetime(df["epoch (ms)"], unit="ms")
pd.to_datetime(df["time (01:00)"]).dt.month

# setting index for time series analysis
acc_df.index = pd.to_datetime(acc_df["epoch (ms)"], unit="ms")
gyr_df.index = pd.to_datetime(gyr_df["epoch (ms)"], unit="ms")

# get rid of the other time columns, no need

acc_df.drop(columns=["epoch (ms)", "time (01:00)", "elapsed (s)"], inplace=True)
gyr_df.drop(columns=["epoch (ms)", "time (01:00)", "elapsed (s)"], inplace=True)


# --------------------------------------------------------------
# Turn into function
# --------------------------------------------------------------
files = glob("../../demo-project/src/data/raw/MetaMotion/*.csv")


def read_data_from_files(files):
    acc_df = pd.DataFrame()
    gyr_df = pd.DataFrame()

    acc_set = 1
    gyr_set = 1

    for f in files:
        participant = f.split("/")[-1].split("-")[0]
        label = f.split("/")[-1].split("-")[1]
        category = f.split("/")[-1].split("-")[2].rstrip("123").rstrip("_MetaWear_2019")

        df = pd.read_csv(f)

        df["participant"] = participant
        df["label"] = label
        df["category"] = category

        if "Accelerometer" in f:
            df["set"] = acc_set
            acc_df = pd.concat([acc_df, df])
            acc_set += 1

        if "Gyroscope" in f:
            df["set"] = gyr_set
            gyr_df = pd.concat([gyr_df, df])
            gyr_set += 1

    acc_df.index = pd.to_datetime(acc_df["epoch (ms)"], unit="ms")
    gyr_df.index = pd.to_datetime(gyr_df["epoch (ms)"], unit="ms")

    acc_df.drop(columns=["epoch (ms)", "time (01:00)", "elapsed (s)"], inplace=True)
    gyr_df.drop(columns=["epoch (ms)", "time (01:00)", "elapsed (s)"], inplace=True)

    return acc_df, gyr_df


acc_df, gyr_df = read_data_from_files(files)


# --------------------------------------------------------------
# Merging datasets
# --------------------------------------------------------------

data_merged = pd.concat([acc_df.iloc[:, :3], gyr_df], axis=1)

data_merged.dropna()

data_merged.columns = [
    "acc_x",
    "acc_y",
    "acc_z",
    "gyr_x",
    "gyr_y",
    "gyr_z",
    "participant",
    "label",
    "category",
    "set",
]
# --------------------------------------------------------------
# Resample data (frequency conversion)
# --------------------------------------------------------------

# Accelerometer:    12.500HZ
# Gyroscope:        25.000Hz

sampling = {
    "acc_x": "mean",
    "acc_y": "mean",
    "acc_z": "mean",
    "gyr_x": "mean",
    "gyr_y": "mean",
    "gyr_z": "mean",
    "participant": "last",
    "label": "last",
    "category": "last",
    "set": "last",
}


data_merged[:1000].resample("200ms").agg(
    {
        "acc_x": "mean",
        "acc_y": "mean",
        "acc_z": "mean",
        "gyr_x": "mean",
        "gyr_y": "mean",
        "gyr_z": "mean",
        "participant": "first",
        "label": "first",
        "category": "first",
        "set": "first",
    }
)

# creates list of dataframes, each dataframe is a day
days = [g for n, g in data_merged.groupby(pd.Grouper(freq="D"))]

days[0]

data_resampled = pd.concat(
    [d.resample("200ms").agg(sampling).dropna() for d in days], axis=0
)

data_resampled["set"] = data_resampled["set"].astype(int)
# --------------------------------------------------------------
# Export dataset
# --------------------------------------------------------------

data_resampled.to_pickle("../../demo-project/src/data/interim/01_data_processed.pkl")
