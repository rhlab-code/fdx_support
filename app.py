# --- Dash imports ---
from dash import Dash, dcc, html, Input, State, Output, callback
import dash_ag_grid as dag
import pandas as pd
import plotly.express as px
import subprocess
import sys

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Load dataset ---
#df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')
df = pd.read_csv('./WBFFT/WBFFT_Combined_Results_2001_558_6031_1c_3408_5385_73ef_fe58.csv')
external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = Dash(__name__, external_stylesheets=external_stylesheets)

# Requires Dash 2.17.0 or later
app.layout = html.Div([
    html.H1("FDX Amp Info"),
    html.H3("subheading"),
    html.Div([
        "",
        dcc.Input(id='input-macip', value='', type='text', placeholder='Enter MACIP Address'),
    ]),
    html.Button(id='submit-button-state', n_clicks=0, children='Submit'),
    html.Div(id='fetch-output'),
    
])
@callback(Output('fetch-output', 'children'),
              Input('submit-button-state', 'n_clicks'),
              State('input-macip', 'value'))

def update_output(n_clicks, input1):
    #return f'''
    #    The Button has been pressed {n_clicks} times,
    #    Input 1 is "{input1}",
    #'''
    cmd = [sys.executable, "ds.py", "--image", "CC", "--addr", input1]
    process = subprocess.run(cmd, check=True)
    try:
        return f'''
        {process}
        '''
    except subprocess.CalledProcessError as e:
        print(f"ds.py exited with return code {e.returncode}")
    except FileNotFoundError:
        print("ds.py not found. Ensure ds.py is in the same directory.")
    
if __name__ == '__main__':
    app.run(debug=True)