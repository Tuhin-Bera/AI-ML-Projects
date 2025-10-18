import streamlit as st
import pandas as pd
import numpy as np
import  preprocessor, helper
from io import StringIO
import matplotlib.pyplot as plt
import seaborn as sns




st.sidebar.title("Whatsapp Chat Analyzer")



uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:

    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    chat = bytes_data.decode("utf-8", errors="ignore")
    # st.text(chat)
    df = preprocessor.preprocess(chat)

    # st.dataframe(df)     ## you can print the chat-data

    ## fitch unique user
    user_list = df["Sender"].unique().tolist()
    # user_list.remove("System")       ##Already done
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show Analysis WRT", user_list)

    if st.sidebar.button("Analyze"):

        ## Stats Area
        num_messages, words, num_media_messages, num_links  = helper.fetch_stats(selected_user, df)

        st.title("Top statistics")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col2:
            st.header("Total Words")
            st.title(words)

        with col3:
            st.header("Total Media Shared")
            st.title(num_media_messages)

        with col4:
            st.header("Total Links")
            st.title(num_links)


        ## Monthly-Timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline["Time"], timeline["Message"], color="green")
        plt.xticks(rotation=45)
        st.pyplot(fig)

        ## Daily-Timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline["only_date"], daily_timeline["Message"], color="black")
        plt.xticks(rotation=45)
        st.pyplot(fig)

        ## Activity map
        st.title("Activity Map")
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most Busy Day")
            busy_day = helper.week_activity_map(selected_user, df)

            fig, ax = plt.subplots()
            ax.bar(busy_day["day_name"], busy_day["Message"], color="red")
            plt.xticks(rotation=45)
            st.pyplot(fig)

        with col2:
            st.header("Most Busy Month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month["Month"], busy_month["Message"], color="orange")
            plt.xticks(rotation=45)
            st.pyplot(fig)

        ## Weekly activity Heatmap
        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap, cmap="plasma")
        plt.xticks(rotation=45)
        st.pyplot(fig)


        ## Finding the busiest user in the group
        if selected_user == "Overall":
            st.title("Overall Busy Statistics")
            x, new_df = helper.most_busy_user(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color="#855262")
                plt.xticks(rotation=45)
                st.pyplot(fig)
                plt.show()

            with col2:
                st.dataframe(new_df)

        ## WordCloud
        st.title("Most Common Messages -> WordCloud")
        df_wc = helper.create_word_cloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)



        ## Most common words
        most_common_df = helper.most_common_words(selected_user, df)

        st.title("Most Common Words")
        fig, ax = plt.subplots()
        ax.barh(most_common_df["word"], most_common_df["count"], color="#855262")
        plt.xticks(rotation=45)
        st.pyplot(fig)

        # st.dataframe(most_common_df)   ## i am not showing the table anymore



        ## emoji analysis
        emoji_df = helper.emoji_helper(selected_user, df)
        st.title("Emoji Analysis")
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df["count"], labels=emoji_df["emoji"], autopct="%.0f%%")
            st.pyplot(fig)

