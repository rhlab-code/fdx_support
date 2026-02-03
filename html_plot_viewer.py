import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import os
import argparse
import webbrowser
import config_manager
import sys
from flask import request

parser = argparse.ArgumentParser(description="View EC HTML Plots")
parser.add_argument('--id_string', type=str, default="No --id_string <id_string>", help="Identifier string for plot file suffix (default: empty)")
parser.add_argument('--image', type=str, choices=['CS', 'CC', 'SC', 'BC', 'CCs'], default='CC',
                    help='Specify the image type: CS (CommScope), CC (Comcast), SC (Sercomm), or BC (Broadcom).')
args = parser.parse_args()
config = config_manager.CONFIGURATIONS.get(getattr(args, "image", None), None)

if not isinstance(args.id_string, str):
    args.id_string = str(args.id_string)
current_dir=os.getcwd()
plot_subdir=config.get("path", "").strip("./")
subdir_list = os.listdir(current_dir)

PLOT_DIR = os.path.join(current_dir, plot_subdir)
COEF_HTML_PATH = os.path.join(PLOT_DIR, f"EC_Coefficients_{args.id_string}.html")
PSD_HTML_PATH = os.path.join(PLOT_DIR, f"EC_PSD_Metrics_{args.id_string}.html")

app = dash.Dash(__name__)

def read_html_file(filepath):
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    return "<div style='color:red;'>File not found: {}</div>".format(filepath)

app.layout = html.Div([
    html.H2(f"EC HTML Plot Viewer: --id_string={args.id_string}"),
    html.Div([
        html.H4("Coefficients Plot"),
        html.Iframe(
            id="coef-html",
            srcDoc=read_html_file(COEF_HTML_PATH),
            style={"width": "100%", "height": "600px", "border": "1px solid #ccc"}
        ),
    ]),
    html.Div([
        html.H4("PSD Plot"),
        html.Iframe(
            id="psd-html",
            srcDoc=read_html_file(PSD_HTML_PATH),
            style={"width": "100%", "height": "600px", "border": "1px solid #ccc"}
        ),
    ]),
    dcc.Interval(
        id='interval-component',
        interval=5*1000,  # Refresh every 5 seconds
        n_intervals=0
    )
])

@app.callback(
    Output('coef-html', 'srcDoc'),
    Output('psd-html', 'srcDoc'),
    Input('interval-component', 'n_intervals')
)
def update_htmls(n):
    coef_html = read_html_file(COEF_HTML_PATH)
    psd_html = read_html_file(PSD_HTML_PATH)
    return coef_html, psd_html

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.server.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'

if __name__ == '__main__':
    webbrowser.open_new_tab("http://localhost:8051/")
    app.run(debug=True, port=8051)

# To trigger shutdown, send a POST request to http://localhost:8051/shutdown
# For example, from another terminal: 
#   curl -X POST http://localhost:8051/shutdown
