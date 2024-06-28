import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import preprocessor
import helper
st.sidebar.title("Whatsapp Chat Analyser")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()  # to convert file from byte data to string
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, 'Overall')
    selected_user = st.sidebar.selectbox('Show Analysis wrt',user_list)
    if st.sidebar.button('Show Analysis'):
        num_messages,words,num_media,links=helper.fetch_stats(selected_user,df)
        st.title('Top Statistics')
        col1, col2, col3, col4 = st.columns(4)
        # st.title('Top Statistics')
        with col1:
            st.header('Total Messages')
            st.title(num_messages)
        with col2:
            st.header('Total Words')
            st.title(words)
        with col3:
            st.header('Total Media Shared')
            st.title(num_media)
        with col4:
            st.header('Total Links Shared')
            st.title(links)

        #monthly timeline
        timeline = helper.monthy_timeline(selected_user,df)
        st.title('Monthly Timeline')
        fig,ax=plt.subplots()
        plt.xticks(rotation=90)
        plt.xlabel('Month')
        plt.ylabel('Count')
        plt.figure(figsize=(60, 48), dpi=100)
        ax.plot(timeline['time'],timeline['message'],color='green')

        st.pyplot(fig)

        #daily timeline
        timeline = helper.daily_timeline(selected_user, df)
        st.title('Daily Timeline')
        fig, ax = plt.subplots()
        plt.figure(figsize=(60, 48), dpi=100)
        plt.xticks(rotation=90)
        plt.xlabel('Days')
        plt.ylabel('Count')

        ax.plot(timeline['only_date'], timeline['message'],color='black')

        st.pyplot(fig)


        #find most active users
        if selected_user == 'Overall':
            st.title('Most Active User')
            xx,new_df=helper.most_active_users(df)

            col1,col2=st.columns(2)
            with col1:
                plt.figure(figsize=(58,48),dpi=100)
                sns.barplot(x='user', y='message_count', data=xx,color='red')
                plt.title('Most Active Users',fontsize=250)
                plt.xlabel('User',fontsize=200)
                plt.ylabel('Message Count',fontsize=200)
                plt.xticks(rotation=90,fontsize=170)
                plt.yticks(fontsize=170)
                st.pyplot(plt)
            with col2:
                st.dataframe(new_df)

        df_wc=helper.create_wordcloud(selected_user,df)
        st.title('Word Cloud')
        fig,ax=plt.subplots()
        plt.figure(figsize=(38, 28), dpi=100)
        ax.imshow(df_wc)
        st.pyplot(fig)

        st.title('Most Common Words(excluding Stop Words)')
        most_common_df=helper.most_common_words(selected_user,df)
        st.dataframe(most_common_df)
        fig,ax=plt.subplots()

        ax.barh(most_common_df[0],most_common_df[1])
        ax.set_xlabel('Count', fontsize=22)
        ax.set_ylabel('Message', fontsize=22)
        plt.title('Most Common Words', fontsize=35)
        plt.xticks(rotation=90, fontsize=12)
        plt.yticks(fontsize=12)


        st.pyplot(fig)

        #activity heat map
        st.title('Weekly Activity Map')
        user_heatmap=helper.activity_heatmap(selected_user,df)
        fig,ax=plt.subplots()

        ax=sns.heatmap(user_heatmap,cmap='magma_r')
        plt.title('Weekly Activity Heatmap')
        plt.xlabel('Period')
        plt.ylabel('Day')

        st.pyplot(fig)



        #activity map

        st.title('Activity Map')
        col1,col2 = st.columns(2)
        with col1:
            st.header('Most busy day')
            busy_day = helper.week_activity_map(selected_user,df)
            fig,ax=plt.subplots()
            ax.barh(busy_day.index,busy_day.values)
            ax.set_xlabel('Activity Count', fontsize=30)
            ax.set_ylabel('Day', fontsize=30)
            plt.xticks(rotation=45,fontsize=17)
            plt.yticks(fontsize=17)
            # plt.xticks( fontsize=0)
            # plt.yticks(fontsize=65)
            st.pyplot(fig)

        with col2:
            st.header('Most busy month')
            busy_month = helper.month_activity_map(selected_user,df)
            fig,ax=plt.subplots()
            ax.barh(busy_month.index,busy_month.values,color='orange')
            ax.set_xlabel('Activity Count', fontsize=30)
            ax.set_ylabel('Month',fontsize=30)
            plt.xticks(rotation=45, fontsize=17)
            plt.yticks(fontsize=17)
            st.pyplot(fig)

        emoji_df= helper.emoji_analysis(selected_user,df)
        st.title('Emoji Analysis')

        st.dataframe(emoji_df)



