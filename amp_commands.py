import paramiko
import sys
import os
import csv
import re
import time
import ipaddress
import argparse
import pandas as pd
import numpy as np
import logging
import math
import subprocess
import macaddress
from paramiko import SSHClient
from scp import SCPClient
from itertools import zip_longest

# New unified library imports
import config_manager
import amp_library

# Added to auto open results
import webbrowser

# --- Argument Parsing ---
parser = argparse.ArgumentParser(description="FDX-AMP WBFFT Analyzer for multiple measurement points.")
parser.add_argument('--image', type=str, choices=['CS', 'CC', 'SC'], required=True,
                    help='Specify the image type: CS (CommScope), CC (Comcast), or SC (Sercomm).')
parser.add_argument('--measurement', nargs='+', default=['north_port_input', 'south_port_output', 'ds_afe_input'],
                    choices=['north_port_input', 'south_port_output', 'ds_afe_input'],
                    help='Select one or more measurements to perform.')
parser.add_argument('--channels', default=None,
                    help="Optional. String defining channels for power calculation. Ex: '111M-123M(6M),150M(6M)'")
parser.add_argument('--note', help="Optional note to append to all output filenames.")
parser.add_argument('--no-jump', action='store_true',
                    help='Skip the jump server and connect directly to the target device.')
# --- New arguments added ---
parser.add_argument('--mac', type=str, help="Optional. Target device MAC address. Overrides the value in config.")
parser.add_argument('--ip', type=str, help="Optional. Target device IP address. Overrides the value in config and any MAC-based IP lookup.")
parser.add_argument('--addr', type=str, help="Optional. Specify either IP or MAC address of the target device. Overrides the value in config.")
parser.add_argument('--domain', type=str, help="Optional. CM domain for IP lookup script. Overrides the value in config.")

args = parser.parse_args()

try:
    import plotly.graph_objects as go
    import plotly.io as pio
    PLOTLY_AVAILABLE = True
except ImportError:
    logging.error("Plotly library is not installed. Please install it to enable plotting features.")
    PLOTLY_AVAILABLE = False