# Import required libraries
import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the SpaceX launch data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a Dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    html.H1(
        'SpaceX Launch Records Dashboard',
        style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}
    ),

    # TASK 1: Launch Site Dropdown
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'},
            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
        ],
        value='ALL',
        placeholder="Select a Launch Site here",
        searchable=True
    ),
    html.Br(),

    # TASK 2: Pie chart to show total successful launches
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    # TASK 3: Payload Range Slider
    html.P("Payload range (Kg):"),
    dcc.RangeSlider(
        id='payload-slider',
        min=0,
        max=10000,
        step=1000,
        marks={0: '0', 1000: '1000', 2000: '2000', 3000: '3000', 4000: '4000',
               5000: '5000', 6000: '6000', 7000: '7000', 8000: '8000', 9000: '9000', 10000: '10000'},
        value=[min_payload, max_payload]
    ),
    html.Br(),

    # TASK 4: Scatter chart to show correlation between payload and success
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# TASK 2: Callback for pie chart based on dropdown
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def update_pie_chart(entered_site):
    if entered_site == 'ALL':
        # All sites: show total success launches per site
        df_all = spacex_df.groupby('Launch Site')['class'].sum().reset_index()
        fig = px.pie(
            df_all,
            values='class',
            names='Launch Site',
            title='Total Successful Launches by Site'
        )
        return fig
    else:
        # Specific site: show success vs failure counts
        df_site = spacex_df[spacex_df['Launch Site'] == entered_site]
        df_counts = df_site['class'].value_counts().reset_index()
        df_counts.columns = ['class', 'count']
        fig = px.pie(
            df_counts,
            values='count',
            names='class',
            title=f'Success vs Failure for site {entered_site}'
        )
        return fig

# TASK 4: Callback for scatter chart based on dropdown and payload slider
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [
        Input(component_id='site-dropdown', component_property='value'),
        Input(component_id='payload-slider', component_property='value')
    ]
)
def update_scatter_chart(selected_site, payload_range):
    low, high = payload_range  # unpack slider values
    # Filter by payload range
    df_filtered = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) & 
                            (spacex_df['Payload Mass (kg)'] <= high)]
    
    if selected_site == 'ALL':
        fig = px.scatter(
            df_filtered,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title='Payload vs. Outcome for All Sites',
            hover_data=['Launch Site']
        )
        return fig
    else:
        df_site = df_filtered[df_filtered['Launch Site'] == selected_site]
        fig = px.scatter(
            df_site,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title=f'Payload vs. Outcome for site {selected_site}',
            hover_data=['Launch Site']
        )
        return fig

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8050, debug=True)
