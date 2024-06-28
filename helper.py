from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import string
import emoji

extract=URLExtract()
def fetch_stats(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    num_messages = df.shape[0]  # no. of messages
    # no. of words
    words = []
    for message in df['message']:
        words.extend(message.split())  # splits the message string into words and appends each word to the words list.

    # no. of media
    num_media=df[df['message'] == '<Media omitted>\n'].shape[0]
    # no. of links we use url extract library
    links=[]
    for message in df['message']:
        links.extend(extract.find_urls(message)) # .extend used to append each element to end of list
        # extract.find takes all url from a message
    return num_messages, len(words),num_media,len(links)

def most_active_users(new_df):
    df=new_df[new_df['user'] != 'group_notification']
    x=df['user'].value_counts().head().reset_index()
    x.columns=['user','message_count']
    df=round((df['user'].value_counts()/df.shape[0])*100,2).reset_index()
    df.columns=['name','percent']
    return x,df

def create_wordcloud(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    df=df[df['message'] != '<Media omitted>\n']
    df = df[df['message'] != 'null\n']
    df = df[df['message'] != 'You deleted this message\n']
    df = df[df['message'] != 'This message was deleted\n']


    wc=WordCloud(width=500, height=500, background_color='white')
    df_wc=wc.generate(df['message'].str.cat(sep=' '))
    return df_wc

def most_common_words(selected_user,df):
    f=open('stop_hinglish.txt','r')
    stop_words=f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    temp=df[df['user'] != 'group_notification']
    temp=temp[temp['message'] != '<Media omitted>\n']
    temp = temp[temp['message'] != 'null\n']
    temp = temp[temp['message'] != 'You deleted this message\n']
    temp = temp[temp['message'] != 'This message was deleted\n']

    words=[]
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words and word not in string.punctuation:
                words.append(word)

    most_common_df=pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def emoji_analysis(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis=[]
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
    emoji_counts = Counter(emojis).most_common(len(Counter(emojis)))
    emoji_df = pd.DataFrame(emoji_counts, columns=['emojis', 'count'])
    emoji_df.index += 1
    return emoji_df

def monthy_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    timeline=df.groupby(['year','month_num','month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i]+'-'+str(timeline['year'][i]))
    timeline['time']=time
    return timeline

def daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    daily_timeline=df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline

def week_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    days_order = ['Sunday', 'Saturday', 'Friday', 'Thursday', 'Wednesday', 'Tuesday', 'Monday']
    day_counts = df['day_name'].value_counts().reindex(days_order, fill_value=0)
    return day_counts



def month_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    months_order = ['December', 'November', 'October', 'September', 'August', 'July', 'June', 'May', 'April', 'March', 'February', 'January']


    month_counts = df['month'].value_counts().reindex(months_order, fill_value=0)
    return month_counts

def activity_heatmap(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


    user_heatmap=df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
    user_heatmap = user_heatmap.reindex(day_order)
    return user_heatmap

