import streamlit as st
import pandas as pd
import preprocessor,helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
import scipy

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df = preprocessor.preprocess(df,region_df)

st.sidebar.title('Olympics Analysis')
st.sidebar.image('https://images.app.goo.gl/KybbCkyP37MwQy9b6')
user_menu = st.sidebar.radio(
    'Select an option',
    ('Medal Tally', 'Overall Analysis','Country-wise analysis')
)



if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years , country = helper.country_year_list(df)
    selected_year = st.sidebar.selectbox('Select a year',years) #Creates a dropdown for choosing an year
    selected_country = st.sidebar.selectbox('Select a Country', country)  # Creates a dropdown for choosing a country
    medal_tally =helper.fetch_medal_tally(df,selected_year,selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
       st.title("Overall Tally of Olympics till 2016")
    if selected_year != 'Overall' and selected_country == 'Overall':
       st.title(" Overall Medal Tally  of Olympics in year " + str(selected_year) )
    if selected_year == 'Overall' and selected_country != 'Overall':
       st.title(" Olympics wise analysis of " + selected_country)
    if selected_year != 'Overall' and selected_country != 'Overall':
       st.title(" Medal Tally of " + selected_country + " in "+ str(selected_year))

    st.table(medal_tally)


elif user_menu == 'Overall Analysis':
        editions = df['Year'].unique().shape[0] - 1
        cities = df['City'].unique().shape[0]
        sports = df['Sport'].unique().shape[0]
        events = df['Event'].unique().shape[0]
        athletes = df['Name'].unique().shape[0]
        nations = df['region'].unique().shape[0]

        st.title("Top Statistics")
        col1,col2,col3 = st.columns(3)
        with col1:
            st.header("Editions")
            st.title(editions)
        with col2:
            st.header("Hosts")
            st.title(cities)
        with col3:
            st.header("Sports")
            st.title(sports)

        col1, col2, col3 = st.columns(3)  # Beta_columns have been changed on streamlit to columns
        with col1:
            st.header("Events")
            st.title(events)
        with col2:
            st.header("Nations")
            st.title(nations)
        with col3:
            st.header("Athletes")
            st.title(athletes)

        nations_over_time = helper.data_over_time(df,'region')
        fig = px.line(nations_over_time, x="Edition", y="region")
        st.title("Participating Nations over the years")
        st.plotly_chart(fig)

        events_over_time = helper.data_over_time(df,'Event')
        fig = px.line(events_over_time, x="Edition", y="Event")
        st.title("No. of Events taking place over the years")
        st.plotly_chart(fig)

        athletes_over_time = helper.data_over_time(df,'Name')
        fig = px.line(athletes_over_time, x="Edition", y="Name")
        st.title("No. of Athletes taking part over the years")
        st.plotly_chart(fig)

        st.title("No. of events taking place for every sport over the years")
        fig: object
        fig,ax= plt.subplots(figsize=(20,20))
        x =df.drop_duplicates(['Year','Sport','Event'])
        ax = sns.heatmap(x.pivot_table(index='Sport' , columns='Year' , values = 'Event' , aggfunc='count').fillna(0).astype('int'),annot=True)
        st.pyplot(fig)

        st.title("Most successful Athletes")
        sport_list = df['Sport'].unique().tolist()
        sport_list.sort()
        sport_list.insert(0,'Overall')

        selected_sport = st.selectbox('Select a Sport',sport_list)
        x = helper.most_successful(df,selected_sport)
        st.table(x)

elif user_menu == 'Country-wise analysis':

        st.sidebar.title(" Country-wise analysis  ")

        country_list = df['region'].dropna().unique().tolist()
        country_list.sort()

        selected_country = st.sidebar.selectbox('Select a Country',country_list)

        country_df = helper.yearwise_medal_tally(df,selected_country)
        fig= px.line(country_df,x='Year',y='Medal')
        st.title(" Medal Tally of " + selected_country + " over the years ")
        st.plotly_chart(fig)

        st.title("Top 10 canidates of "+selected_country)
        top10_df = helper.most_successful_athlete(df,selected_country)
        st.table(top10_df)



