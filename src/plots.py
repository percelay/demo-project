import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_pickle("../../demo-project/src/data/interim/01_data_processed.pkl")
df.head()


# plotting first set

set_df = df[df["set"] == 1]
plt.plot(set_df["acc_x"], label="acc_x", alpha=0.5)
plt.plot(set_df["acc_y"], label="acc_y", alpha=0.5)
plt.legend()
plt.show()

# making index back to normal to show counts
# not as readable kinda - just for understanding
plt.plot(set_df["acc_y"].reset_index(drop=True))

# plot all sets

df["label"].unique()

for label in df["label"].unique():
    subset = df[df["label"] == label]
    subset["label"].unique()
    fig, ax = plt.subplots()
    plt.plot(subset["acc_y"].reset_index(drop=True), label=label)
    plt.legend()
    plt.show()

# creating fractional view to see the data better

for label in df["label"].unique():
    subset = df[df["label"] == label]
    subset["label"].unique()
    fig, ax = plt.subplots()
    plt.plot(subset[:100]["acc_y"].reset_index(drop=True), label=label)
    plt.legend()
    plt.show()

# standard matplotlib style parameters
import matplotlib as mpl  # noqa: E402

# figure style
mpl.style.use("seaborn-v0_8-deep")
# figure size
mpl.rcParams["figure.figsize"] = (20, 5)
# correct resolution when exporting
mpl.rcParams["figure.dpi"] = 100


# want to compare medium and heavy sets

category_df = (
    df.query('label == "squat"').query('participant == "A"').reset_index(drop=True)
)


fig, ax = plt.subplots()
category_df.groupby(["category"])["acc_y"].plot()
ax.set_ylabel("acc_y")
ax.set_xlabel("acc_x")
plt.legend()

# they moving faster on medium weight reps than heavy ones ^


# comparing participants bench presses - looks good - e did more reps - b did least

participant_df = (
    df.query('label == "bench"').sort_values("participant").reset_index(drop=True)
)

fig, ax = plt.subplots()
participant_df.groupby(["participant"])["acc_y"].plot()
ax.set_ylabel("acc_y")
ax.set_xlabel("acc_x")
plt.legend()


# plotting on multiple axes

label = "squat"
participant = "A"
all_axis_df = (
    df.query("label == @label")
    .query("participant == @participant")
    .reset_index(drop=True)
)

fig, ax = plt.subplots()
all_axis_df[["acc_x", "acc_y", "acc_z"]].plot(ax=ax)
ax.set_ylabel("acc_y")
ax.set_xlabel("acc_x")
plt.legend()


# building loop to plot all participants and labels
for label in df["label"].unique():
    for participant in df["participant"].unique():
        all_axis_df = (
            df.query("label == @label")
            .query("participant == @participant")
            .reset_index(drop=True)
        )
        if len(all_axis_df) > 0:
            fig, ax = plt.subplots()
            all_axis_df[["acc_x", "acc_y", "acc_z"]].plot(ax=ax)
            ax.set_ylabel("acc_y")
            ax.set_xlabel("acc_x")
            plt.legend()
            plt.show()


for label in df["label"].unique():
    for participant in df["participant"].unique():
        all_axis_df = (
            df.query("label == @label")
            .query("participant == @participant")
            .reset_index(drop=True)
        )
        if len(all_axis_df) > 0:
            fig, ax = plt.subplots()
            all_axis_df[["gyr_x", "gyr_y", "gyr_z"]].plot(ax=ax)
            ax.set_ylabel("gyr_y")
            ax.set_xlabel("gyr_x")
            plt.legend()
            plt.show()


# combining

label = "row"
participant = "A"
combined_plot = (
    df.query("label == @label")
    .query("participant == @participant")
    .reset_index(drop=True)
    .reset_index(drop=True)
)

fig, ax = plt.subplots(nrows=2, sharex=True, figsize=(20, 10))
combined_plot[["acc_x", "acc_y", "acc_z"]].plot(ax=ax[0])
combined_plot[["gyr_x", "gyr_y", "gyr_z"]].plot(ax=ax[1])

ax[0].legend(
    loc="upper center", bbox_to_anchor=(0.5, 1.3), ncol=3, fancybox=True, shadow=True
)
ax[1].legend(
    loc="upper center", bbox_to_anchor=(0.5, 1.3), ncol=3, fancybox=True, shadow=True
)

ax[1].set_xlabel("samples")


# create loop to plot all participants and labels with the compined plots


for label in df["label"].unique():
    for participant in df["participant"].unique():
        combined_plot = (
            df.query("label == @label")
            .query("participant == @participant")
            .reset_index(drop=True)
            .reset_index(drop=True)
        )
        if len(combined_plot) > 0:
            fig, ax = plt.subplots(nrows=2, sharex=True, figsize=(20, 10))
            combined_plot[["acc_x", "acc_y", "acc_z"]].plot(ax=ax[0])
            combined_plot[["gyr_x", "gyr_y", "gyr_z"]].plot(ax=ax[1])

            ax[0].legend(
                loc="upper center",
                bbox_to_anchor=(0.5, 1.3),
                ncol=3,
                fancybox=True,
                shadow=True,
            )
            ax[1].legend(
                loc="upper center",
                bbox_to_anchor=(0.5, 1.3),
                ncol=3,
                fancybox=True,
                shadow=True,
            )

            ax[1].set_xlabel("samples")

            plt.savefig(
                f"../../demo-project/reports/figures/{label.title()}({participant}).png"
            )
            plt.close()

#
