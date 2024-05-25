#!/usr/bin/env python
# coding: utf-8



import pandas as pd


def read_data(start_date, end_date, input_string, country):

    df = pd.read_csv("Data/News.csv") #read csv
    df["date"] = df["date"].str[:10] #take out date from date column
    df['date'] = pd.to_datetime(df['date']) #convert to date format

    df['country.name'] = df['country.name'].fillna("Global") #replace nan as "Global"

    #Drop unnessary columns
    df.drop(columns=['country'], inplace=True) 
    df.drop(columns=['country.__typename'], inplace=True)
    df.drop(columns=['country.id'], inplace=True)


    #Correct links
    df['slug'] = 'https://www.telecompaper.com/news/' + df['slug'].astype(str)

    #replace \u0027 as '
    df['title'] = df['title'].str.replace(r"\\u0027", "'")
    df['title'] = df['title'].str.replace(r'\\u002B', " ")
    df['title'] = df['title'].str.replace(r'\\u0026', " ")
    df['abstract'] = df['abstract'].str.replace(r'\\u0027', "'")
    df['abstract'] = df['abstract'].str.replace(r'\\u00A0', " ")
    df['abstract'] = df['abstract'].str.replace(r'\\u0022', " ")
    df['abstract'] = df['abstract'].str.replace(r'\\u002B', " ")
    df['abstract'] = df['abstract'].str.replace(r'\\u0026', " ")
    


    # filter country
    selected_rows = df
    if country!= "All":
        selected_rows = df[df['country.name'].str.contains(country)]
    else:
        selected_rows = df

        

    # Split the string into words
    keywords_list = input_string.split()


    # Function to check if any keyword is present in the abstract
    def contains_keyword(abstract, keywords):
        for keyword in keywords:
            if keyword not in abstract:
                return False
        return True

    # Filter rows based on keywords
    if input_string=='':
        filtered_df = selected_rows
    else:
        filtered_df = selected_rows[selected_rows['abstract'].apply(lambda x: contains_keyword(x, keywords_list))]



    #filter rows based on dates
    filtered_date_df = filtered_df[filtered_df['date'].between(str(start_date), str(end_date))]
    filtered_date_df=filtered_date_df.sort_values(by=['date'], ascending=False)


    #change column names
    new_column_names = {
        'date': 'date',
        'title': 'Title',
        'slug': 'Link',
        'abstract': 'Abstract', 
        'country.name': 'Country'}

    filtered_date_df = filtered_date_df.rename(columns=new_column_names)
    
    new_sequence = ['date', 'Title', 'Abstract', 'Country', 'Link']
    filtered_date_df = filtered_date_df[new_sequence]
    
    return (filtered_date_df)


def read_data_dev_telecom(start_date, end_date, input_string, country):
    df = pd.read_csv("Data/dev_news_date_1.csv") #read csv
    df['Country'] = "" #adding blank column - Country
    df['Abstract'] = df['Abstract'].fillna('')

    df['Date'] = pd.to_datetime(df['Date'], format='mixed') #convert to date format

    # filter country
    selected_rows = df
    if country!= "All":
        selected_rows = df[df['Country'].str.contains(country)]
    else:
        selected_rows = df
    

    # Split the string into words
    keywords_list = input_string.split()


    # Function to check if any keyword is present in the abstract
    def contains_keyword(abstract, keywords):
        for keyword in keywords:
            if keyword not in abstract:
                return False
        return True

    # Filter rows based on keywords
    if input_string=='':
        filtered_df = selected_rows
    else:
        filtered_df = selected_rows[selected_rows['Abstract'].apply(lambda x: contains_keyword(x, keywords_list))]



    #filter rows based on dates
    filtered_date_df = filtered_df[filtered_df['Date'].between(str(start_date), str(end_date))]
    filtered_date_df=filtered_date_df.sort_values(by=['Date'], ascending=False)


    #change column names
    new_column_names = {
        'Date': 'date',
        'Title': 'Title',
        'Links': 'Link',
        'Abstract': 'Abstract', 
        'Country': 'Country'}

    filtered_date_df = filtered_date_df.rename(columns=new_column_names)
    
    new_sequence = ['date', 'Title', 'Abstract', 'Country', 'Link']
    filtered_date_df = filtered_date_df[new_sequence]
    
    return (filtered_date_df)




def country_lists():
    read_file = open('Data/country_list.txt', 'r')
    lines = read_file.readlines()
    return lines
    #df = pd.read_csv("Data/News.csv") #read csv
    #df['country.name'] = df['country.name'].fillna("Global") #replace nan as "Global"
    #unique_countries = df['country.name'].unique().tolist()
    #return(unique_countries)
