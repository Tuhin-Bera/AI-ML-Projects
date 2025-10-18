from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji


extract = URLExtract()



def fetch_stats(selected_user, df):

    #########################################   make it clear and shorter -->
    # if selected_user == "Overall":
    #     # 1. Number of messages
    #     num_messages = df.shape[0]
    #     # 2. Number of words
    #     words = []
    #     for message in df["Message"]:
    #         words.extend(message.split())
    #
    #     return num_messages, len(words)
    #
    # else:
    #     new_df = df[df["Sender"] == selected_user]
    #     num_messages = new_df.shape[0]
    #
    #     words = []
    #     for message in new_df["Message"]:
    #         words.extend(message.split())
    #
    #     return num_messages, len(words)
    ############################################


    ## New format
    if selected_user != "Overall":
        df = df[df["Sender"] == selected_user]

    ## 1. fetch the number of messages
    num_messages = df.shape[0]
    ## 2. fetch the number of words
    words = []
    for message in df["Message"]:
        words.extend(message.split())

    ## 3. fetch the number of media messages
    num_media_messages = df[df["Message"] == "<Media omitted>"].shape[0]

    ## 4. fetch the number of links
    links = []
    for message in df["Message"]:
        links.extend(extract.find_urls(message))

    return num_messages, len(words), num_media_messages, len(links)


def most_busy_user(df):

    # Count top 5 senders
    x = df["Sender"].value_counts().head(5)
    df = round((df["Sender"].value_counts() / df.shape[0]) * 100, 2).reset_index()
    return x, df


def create_word_cloud(selected_user, df):
    f = open("stop_hinglish.txt", "r")
    stop_words = f.read()

    if selected_user != "Overall":
        df = df[df["Sender"] == selected_user]

    temp = df[df["Message"] != "<Media omitted>"]

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color="white")
    temp["Message"] = temp["Message"] = temp["Message"].apply(remove_stop_words)
    df_wc = wc.generate(temp["Message"].str.cat(sep=" "))

    return df_wc

def most_common_words(selected_user, df):
    f = open("stop_hinglish.txt", "r")
    stop_words = f.read()

    if selected_user != "Overall":
        df = df[df["Sender"] == selected_user]

    temp = df[df["Message"] != "<Media omitted>"]

    words = []
    for message in temp["Message"]:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20), columns=["word", "count"])
    return most_common_df


def emoji_helper(selected_user, df):
    if selected_user != "Overall":
        df = df[df["Sender"] == selected_user]

    import emoji
    emojis = []
    for message in df["Message"]:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emo = Counter(emojis).most_common(len(Counter(emojis)))
    emoji_df = pd.DataFrame(emo, columns=["emoji", "count"])

    return emoji_df

def monthly_timeline(selected_user, df):
    if selected_user != "Overall":
        df = df[df["Sender"] == selected_user]

    timeline = df.groupby(["Year", "Month_num", "Month"]).count()["Message"].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline["Month"][i] + "-" + str(timeline["Year"][i]))

    timeline["Time"] = time

    return timeline


def daily_timeline(selected_user, df):
    if selected_user != "Overall":
        df = df[df["Sender"] == selected_user]
    daily_timeline = df.groupby("only_date").count()["Message"].reset_index()

    return daily_timeline

def week_activity_map(selected_user, df):
    if selected_user != "Overall":
        df = df[df["Sender"] == selected_user]
    return df.groupby("day_name").count()["Message"].reset_index().sort_values(by="Message", ascending=False)


def month_activity_map(selected_user, df):
    if selected_user != "Overall":
        df = df[df["Sender"] == selected_user]
    return df.groupby("Month").count()["Message"].reset_index().sort_values(by="Message", ascending=False)

def activity_heatmap(selected_user, df):
    if selected_user != "Overall":
        df = df[df["Sender"] == selected_user]

    user_heatmap = df.pivot_table(index="day_name", columns="Period", values="Message", aggfunc="count").fillna(0)

    return user_heatmap