"""CSC110 Fall 2021 Final Project Submission

Instructions (READ THIS FIRST!)
===============================

A module for our CSC110 Fall Final Project Submission includes functions that reads from
the csv files under the data folder, and draws a tree map.

Copyright and Usage Information
===============================

This file is Copyright (c) 2021 Jay Lee, Andy Feng, and Jamie Yi
"""

import plotly.express as px
import pandas as pd
import csv


def read_csv_file_return_dict(filename: str) -> dict[str, str]:
    """skhwjfn"""

    with open(filename) as file:
        reader = csv.reader(file)
        next(reader)
        dictionary = {}

        for row in reader:
            process_row(row, dictionary)

    return dictionary


def process_row(row: list[str], state_colour: dict[str, str]) -> None:
    """Convert a row to a mapping of a state and its colour
    """
    state_colour[row[0]] = row[1]


def draw_total_aapi_hate_crime_2020_tree_map() -> None:
    """
    Draws a tree map showing the hierarchy for cities in United States based on the states the
    city belongs to and the political party for each state. The size of each rectangle in the
    tree map represents the total number of AAPI hate crimes reported in 2020 for that area/region.

    """
    df_hate_crime = pd.read_csv('../data/hate_crime_data.csv')
    dic = read_csv_file_return_dict('../data/state_colour_data.csv')

    df_hate_crime['colour'] = df_hate_crime['Population']
    df_hate_crime['party'] = df_hate_crime['Population']

    for row in range(len(df_hate_crime)):
        df_hate_crime['colour'][row] = dic[df_hate_crime['US State'][row]]
        if df_hate_crime['colour'][row] == 'crimson':
            df_hate_crime['party'][row] = 'Republican'
        else:
            df_hate_crime['party'][row] = 'Democratic'

    fig = px.treemap(df_hate_crime, path=[px.Constant('USA'), 'party', 'US State', 'US City'],
                     values='Total Hate Crimes 2020', color='colour',
                     title='Total Number of AAPI Hate Crimes in United States, 2020')
    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
    fig.show()
