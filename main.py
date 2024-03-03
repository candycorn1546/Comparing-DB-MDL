from webbrowser import open_new_tab

import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import pandas as pd
from dash.dash_table import DataTable

title = f"Datas between MyDramaList and Douban" # Title of the webpage
app = dash.Dash(__name__, external_stylesheets=['https://fonts.googleapis.com/css2?family=Coming+Soon&display=swap'])

df = pd.read_csv('Final.csv') # read the csv file

df['Difference in Ratings'] = df['Rating_mdl'] - df['Rating_douban'] # difference in ratings
df['Absolute Difference in Ratings'] = round(df['Difference in Ratings'].abs(), 3) # absolute difference in ratings
df['Difference in Number of Raters'] = df['Number of Raters_mdl'] - df['Number of Raters_douban'] # difference in number of raters
df['Absolute Difference in Number of Raters'] = round(df['Difference in Number of Raters'].abs(), 2) # absolute difference in number of raters


def filter_data(query): # function to filter the data
    if query: # if query is not empty
        return df[df.apply(lambda row: any(query.lower() in str(cell).lower() for cell in row), axis=1)] # filter the data
    else:
        return df # return the original data


average_ratings = df.groupby('Year').agg({ # group by year
    'Rating_mdl': 'mean',
    'Rating_douban': 'mean'
}).reset_index()

app.layout = html.Div(children=[ # layout of the webpage

    html.Div(id='url', style={'display': 'none'}), # hidden div to open the URL in a new tab

    html.H1(children=title,     # Title of the webpage
            style={'font-family': 'Coming Soon, cursive', 'text-align': 'center', 'margin-top': '20px',
                   'margin-bottom': '20px'}),

    # Search bar
    html.Div([
        dcc.Input(
            id='search-input',
            type='text',
            placeholder='Search...',
            style={'width': '100%', 'padding': '10px 12px', 'border': '1px solid #ccc', 'border-radius': '4px'}
        ),
        html.I(className="fas fa-search",
               style={'position': 'relative', 'left': '-30px', 'top': '5px', 'color': '#aaa'})
    ], style={'position': 'relative'}), # Relative position for search icon

    # DataTable
    html.Div(id='table-container'),

    # Add some space
    html.Div(style={'margin-top': '100px'}),

    # Scatter plot for Rating vs. Number of Raters
    html.Div([
        dcc.Graph(
            id='rating-vs-raters-scatter',
            figure={
                'data': [
                    go.Scatter(
                        x=df['Rating_mdl'],
                        y=df['Number of Raters_mdl'],
                        mode='markers',
                        marker=dict(color='skyblue'),
                        text=df['English Title'],
                        name='MyDramaList'
                    ),
                    go.Scatter(
                        x=df['Rating_douban'],
                        y=df['Number of Raters_douban'],
                        mode='markers',
                        marker=dict(color='orange'),
                        text=df['English Title'],
                        name='Douban'
                    )
                ],
                'layout': go.Layout(
                    title='Rating vs. Number of Raters',
                    xaxis={'title': 'Rating'},
                    yaxis={'title': 'Number of Raters'},
                    margin={'l': 40, 'b': 40, 't': 40, 'r': 40},
                    hovermode='closest'
                )
            }
        )
    ]),

    html.Div(style={'margin-top': '100px'}), # Add some space

    # Line plot for trend analysis
    html.Div([
        dcc.Graph(
            id='trend-analysis-line',
            figure={
                'data': [
                    go.Scatter(
                        x=average_ratings['Year'],
                        y=average_ratings['Rating_mdl'],
                        mode='lines',
                        marker=dict(color='skyblue'),
                        name='MyDramaList'
                    ),
                    go.Scatter(
                        x=average_ratings['Year'],
                        y=average_ratings['Rating_douban'],
                        mode='lines',
                        marker=dict(color='orange'),
                        name='Douban'
                    )
                ],
                'layout': go.Layout(
                    title='Trend Analysis of Ratings Over the Years',
                    xaxis={'title': 'Year'},
                    yaxis={'title': 'Average Rating'},
                    margin={'l': 40, 'b': 40, 't': 40, 'r': 40},
                    hovermode='closest'
                )
            }
        )
    ])
])


# Callback to update DataTable based on search query
@app.callback(
    Output('table-container', 'children'),
    [Input('search-input', 'value')]
)
# Update the table based on search query
def update_table(search_query):
    filtered_df = filter_data(search_query)
    return DataTable(
        id='table',
        columns=[
            {'name': 'Title', 'id': 'English Title'},
            {'name': 'Native Title', 'id': 'Native Title'},
            {'name': 'Country', 'id': 'Country'},
            {'name': 'MDL Rating', 'id': 'Rating_mdl'},
            {'name': 'MDL Number of Raters', 'id': 'Number of Raters_mdl'},
            {'name': 'Douban Rating', 'id': 'Rating_douban'},
            {'name': 'Douban Number of Raters', 'id': 'Number of Raters_douban'},
            {'name': 'Difference in Ratings', 'id': 'Absolute Difference in Ratings'},  # New column
            {'name': 'Difference in Number of Raters', 'id': 'Absolute Difference in Number of Raters'}  # New column
        ],
        data=filtered_df.to_dict('records'),
        style_table={'overflowY': 'auto', 'height': '400px'},  # Set height for scroll
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold'
        },
        style_cell={
            'minWidth': '50px', 'width': '100px', 'maxWidth': '200px',
            'whiteSpace': 'normal',
            'textAlign': 'center'
        },
        sort_action='native',  # Sorting
        sort_mode='multi',  # Multi-column sorting
        tooltip_data=[
            {
                column: {'value': str(value), 'type': 'markdown'}
                for column, value in row.items()
            } for row in filtered_df.to_dict('records')
        ],
        tooltip_duration=None  # Display tooltip indefinitely
    )


@app.callback(
    Output('url', 'children'),
    [Input('rating-vs-raters-scatter', 'clickData')]
)
def display_click_data(clickData):
    if clickData:
        point_index = clickData['points'][0]['pointIndex']
        source = clickData['points'][0]['curveNumber']
        if source == 1:
            english_title = df.iloc[point_index]['English Title']
            douban_id = df[df['English Title'] == english_title]['ID'].iloc[0]
            if douban_id:
                url = f"https://movie.douban.com/subject/{douban_id}/"
                return open_new_tab(url)
        else:
            english_title = df.iloc[point_index]['English Title']
            url = df[df['English Title'] == english_title]['URL'].iloc[0]
            return open_new_tab(url)


if __name__ == '__main__':
    app.run_server(debug=True)
