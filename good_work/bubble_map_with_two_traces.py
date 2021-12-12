"""CSC110 Fall 2021 Final Project Submission

Instructions (READ THIS FIRST!)
===============================

A module for our CSC110 Fall Final Project Submission includes functions that reads from
the csv files under the data folder, and displays a bubble map with color-coded bubbles
corresponding to a state's political leaning and size proportionate to the increase in hate crimes

Copyright and Usage Information
===============================

This file is Copyright (c) 2021 Jay Lee, Andy Feng, and Jamie Yi
"""


import pandas
import plotly.graph_objects as go
import csv
import pandas as pd


def draw_bubble_map_with_percentage_proportions() -> None:
    """Draw the bubble map"""
    traces = separate_red_and_blue()
    labels = ('Republican', 'Democratic')

    fig = go.Figure()

    # Iterating through the two traces (Dataframes) in traces
    for i in range(len(traces)):
        # fig.add_trace takes go.Scattergeo objects as a parameter
        fig.add_trace(go.Scattergeo(
            # Longitude parameter
            lon=traces[i]['lon'],
            # Latitude parameter
            lat=traces[i]['lat'],
            # The text parameter for a given bubble is the name of the city plus the city's percent
            # increase in anti AAPI hate crimes
            text=(traces[i]['US City'] + ', ' + traces[i]['Change Anti-Asian Hate Crimes'] +
                  ' increase'),
            # The marker parameter takes a dictionary as a parameter, with the specific keys
            # corresponding to some attribute of the bubble itself
            marker=dict(
                size=traces[i]['size'].to_numpy(dtype=int),
                color=traces[i]['colour'],
                line_color='rgb(40,40,40)',
                line_width=0.5,
                sizemode='area'
            ),
            # name is for the names of all the data points in the set collectively, so since I have
            # two Dataframes for the two political parties, the name will correspond to the
            # Dataframe's political party
            name=labels[i]))

    # Update the figure with the newly added properties above
    fig.update_layout(
        title_text='Percentage Increase in anti-AAPI Hate Crimes in American Cities'
                   '<br>(Click legend to toggle traces)',
        showlegend=True,
        geo=dict(
            scope='usa',
            landcolor='rgb(217, 217, 217)',
        )
    )

    # Display the bubble map
    fig.show()


def separate_red_and_blue() \
        -> tuple[pandas.DataFrame, pandas.DataFrame]:
    """Return the rows of hate_crime_data.csv separated into two dataframes, one for only 'crimson'
    (Republican) states and one for only 'royalblue' (Democratic) states
    """

    hate_crime_data_df = process_hate_crime_csv()

    # Create two empty Dataframes with the same columns as hate_crime_data_df
    hate_crimes_red = pandas.DataFrame(columns=tuple(hate_crime_data_df.columns))
    hate_crimes_blue = pandas.DataFrame(columns=tuple(hate_crime_data_df.columns))

    for i in range(len(hate_crime_data_df)):
        if hate_crime_data_df.iloc[i]['colour'] == 'crimson':
            hate_crimes_red = hate_crimes_red.append(hate_crime_data_df.iloc[i])

    for i in range(len(hate_crime_data_df)):
        if hate_crime_data_df.iloc[i]['colour'] == 'royalblue':
            hate_crimes_blue = hate_crimes_blue.append(hate_crime_data_df.iloc[i])

    return (hate_crimes_red, hate_crimes_blue)


def process_hate_crime_csv() -> pandas.DataFrame:
    """Make a dataframe representing hate_crime_data.csv, and then add columns representing the
    city's latitude, longitude, colour (political leaning), and relative size of its 'bubble' on
    the bubble map.
    """

    # This block creates a dictionary mapping a state's name to its political leaning colour
    with open('../data/state_colour_data.csv') as file:
        reader = csv.reader(file)
        headers = next(reader)
        state_colour = {}
        for row in reader:
            process_row(row, state_colour)

    coordinates = pd.read_csv('../data/uscities.csv')
    hate_crime_data_df = pd.read_csv('../data/hate_crime_data.csv')

    # In order to work with specific slices (single elements) of a Dataframe, I must instantiate
    # The new columns first (like in Java), so here I assign them a placeholder dummy column
    hate_crime_data_df['colour'] = hate_crime_data_df['US City']
    hate_crime_data_df['lat'] = hate_crime_data_df['US City']
    hate_crime_data_df['lon'] = hate_crime_data_df['US City']
    hate_crime_data_df['size'] = hate_crime_data_df['US City']

    # Searches coordinates for cities that are also in hate_crime_data_df, and then assigns the
    # Corresponding latitudes and longitudes from coordinates to the matching city in hate_crime_data_df
    for i in range(len(hate_crime_data_df)):
        for j in range(len(coordinates)):
            # Making sure both the state and city are matching
            if str(hate_crime_data_df['US City'][i]).strip() == coordinates['city'][j]:
                if hate_crime_data_df['US State'][i] == coordinates['state_id'][j]:
                    # Whenever any value is trying to be set to be a copy of a slice
                    # (single element) of a Dataframe, pandas will throw a warning, the code will
                    # still run nonetheless
                    hate_crime_data_df['lat'][i] = float(coordinates['lat'][j])
                    hate_crime_data_df['lon'][i] = float(coordinates['lng'][j])

    # Assigns each city in hate_crime_data_df it's proper colour(ie, political leaning) by indexing the
    # dictionary state_colour
    for i in range(len(hate_crime_data_df)):
        # this line will throw a warning, but the code still works as indented
        hate_crime_data_df['colour'][i] = state_colour[hate_crime_data_df['US State'][i]]

    # Reformatting the column so there are only percentages (check the Computational Overview) on
    # what the elif statement is
    for i in range(len(hate_crime_data_df)):
        if hate_crime_data_df['Change Anti-Asian Hate Crimes'][i] == 'Unchanged':
            hate_crime_data_df['Change Anti-Asian Hate Crimes'][i] = '0%'
        elif hate_crime_data_df['Change Anti-Asian Hate Crimes'][i] == '-':
            hate_crime_data_df['Change Anti-Asian Hate Crimes'][i] = str(
                hate_crime_data_df['2020 Anti-Asian'][i] * 100) + '%'

    # The size of the bubble should be equal to the percentage increase in hate crimes, if there is
    # a decrease or no change, the size of the bubble will be set to 5
    for i in range(len(hate_crime_data_df)):
        hate_crime_data_df['size'][i] = int(str(hate_crime_data_df['Change Anti-Asian Hate Crimes'][i]).strip('%'))
        if hate_crime_data_df['size'][i] <= 0:
            hate_crime_data_df['size'][i] = 5

    return hate_crime_data_df


def process_row(row: list[str], state_colour: dict[str, str]) -> None:
    """Convert a row to a mapping of a its first column element and its second column element
    """
    state_colour[row[0]] = row[1]
