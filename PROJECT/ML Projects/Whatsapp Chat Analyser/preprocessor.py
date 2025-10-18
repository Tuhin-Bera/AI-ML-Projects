import re
import pandas as pd

def preprocess(chat):
    pattern = r"^(\d{2}\/\d{2}\/\d{4}), (\d{2}:\d{2}) - (.*)$"
    data = []

    for line in chat.split("\n"):
        match = re.match(pattern, line.strip())
        if match:
            date, time, content = match.groups()

            if ": " in content:  # Normal message
                sender, message = content.split(": ", 1)
            else:  # System message
                sender = "System"
                message = content

            data.append([date, time, sender, message])

    # Create DataFrame
    df = pd.DataFrame(data, columns=["Date", "Time", "Sender", "Message"])

    ## removing System from the dataset
    df = df[df["Sender"] != "System"].copy()

    # Merge Date & Time into Datetime
    df["Datetime"] = pd.to_datetime(df["Date"] + " " + df["Time"], dayfirst=True, errors="coerce")

    # Extract year, month, day, hour, minute
    df["Year"] = df["Datetime"].dt.year
    df["Month_num"] = df["Datetime"].dt.month    ## lastly added
    df["Month"] = df["Datetime"].dt.month_name()
    df["only_date"] = df["Datetime"].dt.date     ## lastly added
    df["Day"] = df["Datetime"].dt.day
    df["day_name"] = df["Datetime"].dt.day_name()  ## lastly added
    df["Hour"] = df["Datetime"].dt.hour
    df["Minute"] = df["Datetime"].dt.minute

    period = []
    for hour in df["Hour"]:
        if hour == 23:
            period.append(str(hour) + "-" + "00")
        elif hour == 0:
            period.append("00-1")
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df["Period"] = period

    # Keep only required columns
    df = df[["Datetime", "Sender", "Message", "Year", "Month_num", "Month", "only_date",  "Day", "day_name", "Hour", "Minute", "Period"]].reset_index(drop=True)

    return df

