# all of the imports and packages 
import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html 
from dash.dependencies import Input, Output
# Load the data
df = pd.read_csv('/Users/mikeyjensen/Downloads/poi_metrics.csv')
print(df.head())


y_columns = [col for col in df.columns if col != 'session' and col != 'pitch_speed_mph']



# Initialize the Dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True)

# Layout 

server = app.server

app.layout = html.Div([
    # Dropdown for selecting the y-axis column
    html.Div([
        dcc.Dropdown(
            id="y-axis-dropdown",
            options=[{"label": col, "value": col} for col in y_columns],
            value=y_columns[0],  # Default value
            clearable=False,
            style={'width': '50%', 'padding': '10px', 'font-size': '18px', 'font-weight': 'bold'}  # Dropdown styling
        ),
    ], style={'width': '100%', 'textAlign': 'center', 'margin': '20px'}),

   # Dropdown for selecting the session
    html.Div([
        dcc.Dropdown(
            id="session-dropdown",
            options=[{"label": str(session), "value": session} for session in df['session'].unique()],
            value=df['session'].unique()[0],  # Default value
            clearable=False,
            style={'width': '50%', 'padding': '10px', 'font-size': '18px', 'font-weight': 'bold'}  # Dropdown styling
        ),
    ], style={'width': '100%', 'textAlign': 'center', 'margin': '20px'}),
    
    # Graph to display the plot
    html.Div([
        dcc.Graph(id="scatter-plot", style={'height': '80vh', 'width': '100%'})
    ], style={'padding': '20px'}),
])


@app.callback(
    Output("scatter-plot", "figure"),  # Ensure the id is 'scatter-plot' (lowercase)
    [Input("y-axis-dropdown", "value"), Input("session-dropdown", "value")]  # Ensure the dropdown id matches (lowercase)
)
def update_graph(selected_y_column, selected_session):

    filtered_df = df[df['session'] == selected_session]
    #create the scatter plot 
    fig = px.scatter(filtered_df, x = 'pitch_speed_mph', y = selected_y_column,
                     title = f"{selected_y_column} vs. Pitch Speed",
                     labels = {'pitch_speed_mph': 'Pitch Speed (MPH)', selected_y_column: selected_y_column},
                     template = 'plotly_dark') # Dark theme
    
      # Set axis labels explicitly
    fig.update_layout(
        xaxis_title='Pitch Speed (MPH)',
        yaxis_title= selected_y_column,

    # Title styling
        title_font=dict(family="Roboto", size=24, color="white"),
        
        # X and Y axis styling
        xaxis=dict(title_font=dict(family="Roboto", size=18, color="white")),
        yaxis=dict(title_font=dict(family="Roboto", size=18, color="white")),
        
        # General layout styling
        plot_bgcolor='rgba(0, 0, 0, 0)',  # Transparent background for plot
        paper_bgcolor='rgb(50, 50, 50)',  # Dark background for the whole chart
        font=dict(family="Roboto", size=14, color="white"),  # Font style for text
        
        # Grid and line styling
        xaxis_showgrid=True,  # Show grid on x-axis
        yaxis_showgrid=True,  # Show grid on y-axis
        xaxis_gridcolor='rgba(255, 255, 255, 0.2)',  # Light gridline color
        yaxis_gridcolor='rgba(255, 255, 255, 0.2)',  # Light gridline color
        
        # Hover effects and marker styling
        hovermode='closest',  # Hover over the nearest point
        hoverlabel=dict(bgcolor="black", font_size=14, font_family="Arial", font_color="white"),  # Hover label styles
        
        # Smooth transition effect for plotting
        transition_duration=500  # Smooth transition when switching data
    )
        
    
    return fig

if __name__ == "__main__":
    app.run(debug=True)
