import numpy as np
import pandas as pd


def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == int(year)) & (medal_df['region'] == country)]
    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year',
                                                                                    ascending=True).reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                      ascending=False).reset_index()

    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']
    x['Gold'] = x['Gold'].astype(int)
    x['Silver'] = x['Silver'].astype(int)
    x['Bronze'] = x['Bronze'].astype(int)
    return (x)


def medal_tally(df):
    medal_tally = medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year',
                                                           'City', 'Sport', 'Event', 'Medal'])
    medal_tally = medal_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                                ascending=False).reset_index()
    medal_tally['total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']

    return medal_tally


def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return years, country


def data_over_time(df, col):
    nations_over_time = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values('Year')
    nations_over_time.rename(columns={'count': col, 'Year': 'Edition'}, inplace=True)
    return nations_over_time


def most_successful(df, sport):
    temp_df = df.dropna(subset=['Medal'])  # --. Removing rows having Nan Values

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

        x = temp_df['Name'].value_counts().reset_index().merge(df, how='left')[
            ['Name', 'count', 'Sport', 'region']].drop_duplicates('Name')
        x.rename(columns={'count': 'Medals'}, inplace=True)
        return x

    else:
        return df.dropna(subset=['Medal'])['Name'].value_counts().reset_index().merge(df, how='left')[
            ['Name', 'count', 'Sport', 'region']].drop_duplicates()


def yearwise_medal_tally(df, country):
    jump_df = df.dropna(subset=['Medal'])
    jump_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'Event', 'Medal', 'City', 'Sport'], inplace=True)

    new_df = jump_df[jump_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()

    return final_df


def most_successful_athlete(df, country):
    temp_df = df.dropna(subset=['Medal'])  # --. Removing rows having Nan Values

    temp_df = temp_df[temp_df['region'] == country]

    x = temp_df['Name'].value_counts().reset_index().merge(df, how='left')[['Name', 'count', 'Sport']].drop_duplicates(
        'Name')
    x.rename(columns={'count': 'Medals'}, inplace=True)
    return x

