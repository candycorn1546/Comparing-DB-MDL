import dash
from dash import dcc, html
import plotly.graph_objs as go
import pandas as pd
from dash.dash_table import DataTable


# Read data from CSV
df = pd.read_csv('Final.csv')

# Calculate the difference in ratings
df['Difference in Ratings'] = df['Rating_mdl'] - df['Rating_douban']
df['Absolute Difference in Ratings'] = round(df['Difference in Ratings'].abs(), 3)
df['Difference in Number of Raters'] = df['Number of Raters_mdl'] - df['Number of Raters_douban']
df['Absolute Difference in Number of Raters'] = round(df['Difference in Number of Raters'].abs(),2)

# Get unique year
title = f"Datas between MyDramaList and Douban"

app = dash.Dash(__name__, external_stylesheets=['https://fonts.googleapis.com/css2?family=Coming+Soon&display=swap'])

def filter_data(query):
    if query:
        return df[df['English Title'].str.contains(query, case=False)]
    else:
        return df

# App layout
# Group data by year and calculate average ratings for MyDramaList and Douban
average_ratings = df.groupby('Year').agg({
    'Rating_mdl': 'mean',
    'Rating_douban': 'mean'
}).reset_index()


app.layout = html.Div(children=[
    # Title
    html.H1(children=title,
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
    ], style={'position': 'relative'}),

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

    html.Div(style={'margin-top': '100px'}),

    # Line plot for Trend Analysis
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

# Your callback function and app.run_server() call remain the same

# Your callback function and app.run_server() call remain the same

# Your callback function and app.run_server() call remain the same




# Callback to update DataTable based on search query
@app.callback(
    dash.dependencies.Output('table-container', 'children'),
    [dash.dependencies.Input('search-input', 'value')]
)
def update_table(search_query):
    filtered_df = filter_data(search_query)
    return DataTable(
        id='table',
        columns=[
            {'name': 'Title', 'id': 'English Title'},
            {'name': 'Native Title', 'id': 'Native Title'},
            {'name': 'Country', 'id': 'Country'},
            {'name': 'Rating_mdl', 'id': 'Rating_mdl'},
            {'name': 'Number of Raters_mdl', 'id': 'Number of Raters_mdl'},
            {'name': 'Rating_douban', 'id': 'Rating_douban'},
            {'name': 'Number of Raters_douban', 'id': 'Number of Raters_douban'},
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

if __name__ == '__main__':
    app.run_server(debug=True)
