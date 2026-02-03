# IP Lookup Helper (Patched v2.2)
# Based on user's original script to query Thanos for CM/CPE IP by MAC.
# Changes:
#   - Use sys.executable for subprocess calls (avoid wrong interpreter)
#   - Stronger diagnostics on subprocess failures
#   - Safe JSON parsing (handles None/non-JSON)
#   - Robust IPv4/IPv6 validators
#   - Optional second attempt passing --bearer <token> to thanos2.py (if supported)
#   - Clearer messaging around python-dotenv install vs .env presence

import subprocess
import json
import ipaddress
import sys
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Load environment variables from .env file ---
try:
    from dotenv import load_dotenv
    load_dotenv()  # Will search for .env in current and parent directories
except ImportError:
    print("python-dotenv is not installed. Install with: pip install python-dotenv")


def run_script_and_get_result(script_path, arguments=[]):
    logging.debug(f"Running script for result: {script_path} with arguments: {arguments}")
    """
    Runs a Python script in a subprocess and returns the output.

    Args:
      script_path: The path to the Python script to execute.
      arguments: A list of arguments to pass to the script.

    Returns:
      A string containing the stdout of the script, or None if an error occurred.
    """
    try:
        command = [sys.executable, script_path] + arguments
        process = subprocess.run(command, capture_output=True, text=True)
        if process.returncode == 0:
            return process.stdout.strip()
        else:
            print(f"[{os.path.basename(script_path)}] rc={process.returncode}")
            if process.stderr:
                print(f"[stderr]: {process.stderr.strip()[:500]}")
            if process.stdout:
                print(f"[stdout]: {process.stdout.strip()[:500]}")
            return None
    except FileNotFoundError:
        print(f"Script not found: {script_path}")
        return None


def run_script(script_path, arguments=[]):
    logging.debug(f"Running script: {script_path} with arguments: {arguments}")
    """Runs a Python script in a subprocess and logs errors if any."""
    try:
        command = [sys.executable, script_path] + arguments
        process = subprocess.run(command, capture_output=True, text=True)
        if process.returncode != 0:
            logging.warning(f"Error running script {script_path} (rc={process.returncode})")
            if process.stderr:
                logging.warning(f"[stderr]: {process.stderr.strip()[:500]}")
            if process.stdout:
                logging.debug(f"[stdout]: {process.stdout.strip()[:500]}")
    except FileNotFoundError:
        logging.warning(f"Script not found: {script_path}")


def is_ipv6(address):
    logging.debug(f"Validating IPv6 address: {address}")
    """Checks if a string is a valid IPv6 address."""
    if not address:
        return False
    try:
        ipaddress.IPv6Address(address)
        return True
    except (ipaddress.AddressValueError, ValueError, TypeError):
        return False


def is_ipv4(address):
    logging.debug(f"Validating IPv4 address: {address}")
    """Checks if a string is a valid IPv4 address."""
    if not address:
        return False
    try:
        ipaddress.IPv4Address(address)
        return True
    except (ipaddress.AddressValueError, ValueError, TypeError):
        return False


def safe_json_load(s):
    logging.debug("Parsing JSON response")
    try:
        return json.loads(s)
    except (json.JSONDecodeError, TypeError):
        logging.debug("Failed to parse JSON. safe_json_load returning None.")
        return None


def find_IpAddr(json_string, search):
    """
    Finds and extracts a given key from each 'metric' result in the Thanos JSON response.

    Args:
      json_string: The JSON string to search.
      search: The key to retrieve from result_item['metric'].

    Returns:
      First matching value as string, or None.
    """
    obj = safe_json_load(json_string)
    if not obj:
        if json_string:
            logging.debug(f"Non-JSON or empty response (first 200 chars): {str(json_string)[:200]}")
        else:
            logging.debug("Empty response from thanos2.py")
        return None

    try:
        for result_item in obj.get('data', {}).get('result', []):
            logging.debug(f"Inspecting result item: {result_item}")
            val = result_item.get('metric', {}).get(search)
            if val:
                return val
    except Exception as e:
        logging.warning(f"Error parsing JSON structure: {e}")
    return None


# --- Begin main behavior ---
if __name__ == '__main__':
    path = "./toybox-main"
    Short_output = len(sys.argv) == 4
    if Short_output:
        arg1 = sys.argv[1]   # 'PROD' or 'DEV'
        arg2 = sys.argv[2]   # 'CM' or 'CPE'
        arg3 = sys.argv[3]   # CM MAC or list string
    else:
        print("Please provide 3 arguments: PROD or DEV, CM or CPE, MACs")
        arg1 = 'PROD'
        arg2 = 'CPE'
        arg3 = ['aa:76:3f:f0:78:b0','8c:76:3f:f0:78:c4','10:e1:77:58:d1:78']
        #arg3 = '24:a1:86:1b:ed:e4'
#2001:0558:40A0:0013:DD18:FF03:710D:6047    CM Do not use
#2001:0558:6043:003F:2855:D2DC:2D77:FD23    CPE MACs for testing
    if arg1 == "PROD":
        url = "https://sat-prod.codebig2.net/v2/ws/token.oauth2"
        PROD_secret = os.environ.get("PROD_API_KEY")
        if PROD_secret is None:
            print("PROD_API_KEY environment variable not set.")
            sys.exit(1)
        secret = PROD_secret
        tag = 'prod'
    elif arg1 == "DEV":
        url = "https://sat-stg.codebig2.net/v2/ws/token.oauth2"
        DEV_secret = os.environ.get("DEV_API_KEY")
        if DEV_secret is None:
            print("DEV_API_KEY environment variable not set.")
            sys.exit(1)
        secret = DEV_secret
        tag = 'dev'
    else:
        print(f"Unknown environment '{arg1}'. Use PROD or DEV.")
        sys.exit(1)

    # Determine target type
    # 24:a1:86:1b:ed:e4
    if arg2 == "CM":
        #2001:0558:40A0:0013:DD18:FF03:710D:6047
        k_matrix = 'K_CmRegStatus_Config'
        find_ipv4 = 'ipV4Addr'
        find_ipv6 = 'ipv6Addr'
    elif arg2 == "CPE":
        #2001:0558:6043:003F:2855:D2DC:2D77:FD23        cpeIpv6Addr
        k_matrix = 'K_CmCpeList'
        find_ipv4 = 'cpeIpv4Addr'
        find_ipv6 = 'cpeIpv6Addr'
    else:
        print(f"Unknown target '{arg2}'. Use CM or CPE.")
        sys.exit(1)

    websec = os.path.join(path, 'websec.py')
    thanos2 = os.path.join(path, 'thanos2.py')

    # Acquire token via websec.py
    logging.debug("Acquiring token via websec.py")
    run_script(websec, ["thanos-prod", "--url", url, "--id", "ngan-hs", "--secret", secret, "--scope", "ngan:telemetry:thanosapi"])
    token = run_script_and_get_result(websec, [f"thanos-{tag}", "--bearer"]) or ""

    # Build MAC list
    if isinstance(arg3, str):
        logging.debug("Single MAC address provided")
        mac_list = [arg3]
    else:
        mac_list = arg3

    for mac in mac_list:
        # First attempt: without bearer (for environments where thanos2.py reads cached token)
        arguments = [f"--{tag}", k_matrix, f"cmMacAddr={mac}"]
        result = run_script_and_get_result(thanos2, arguments)

        # If no result, try again passing bearer explicitly (if supported)
        if (not result) and token:
            arguments_bearer = [f"--{tag}", k_matrix, f"cmMacAddr={mac}", "--bearer", token]
            result = run_script_and_get_result(thanos2, arguments_bearer)

        if not result:
            print(f"CM MAC = {mac}: no result from thanos2.py")
            continue

        ip = find_IpAddr(result, find_ipv4)
        if is_ipv4(ip) and ip != '0.0.0.0':
            print(ip if Short_output else f"CM MAC = {mac}, {find_ipv4} = {ip}")
            continue

        ip = find_IpAddr(result, find_ipv6)
        if is_ipv6(ip):
            print(ip if Short_output else f"CM MAC = {mac}, {find_ipv6} = {ip}")
        else:
            print(f"CM MAC = {mac}: No valid {find_ipv4}/{find_ipv6} found.")
