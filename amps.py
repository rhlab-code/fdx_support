import argparse
import ipaddress
import logging
from logging import config
from logging import config
import subprocess
import sys
import os
import config_manager
import macaddress
import amp_library

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
#parser = argparse.ArgumentParser(description="FDX-AMP WBFFT Analyzer for multiple measurement points.")
#parser.add_argument('--addr', type=str, help="Optional. Specify either IP or MAC address of the target device. Overrides the value in config.")
#args = parser.parse_args()
temp = None
#-----------------------------------------------
def is_ipv6(address):
  """Checks if a string is a valid IPv6 address."""
  try:
    ipaddress.IPv6Address(address)
    return True
  except ipaddress.AddressValueError:
    return False

def is_ipv4(address):
  """Checks if a string is a valid IPv4 address."""
  try:
    ipaddress.IPv4Address(address)
    return True
  except ipaddress.AddressValueError:
    return False

def is_mac(mac):
    """
    Checks if a string is a valid MAC address using the macaddress library.
    """
    try:
        macaddress.MAC(mac)
        return True
    except ValueError:
        return False

def run_script_and_get_result(script_path, arguments=[]):
  logging.debug(f"Running script: {script_path} with arguments: {arguments}")
  """Runs a Python script in a subprocess and returns the output."""
  try:
    command = ["python", script_path] + arguments
    process = subprocess.run(command, capture_output=True, text=True)
    if process.returncode == 0:
      return process.stdout.strip()
    else:
      print(f"Error running script: {process.stderr}")
      return None
  except FileNotFoundError:
    print(f"Script not found: {script_path}")
    return None


#-----------------------------------------------

def prompt_image():
    while True:
        val = input("Enter build type (CC or CS): ").strip().upper()
        if not isinstance(val, str):
            print("Build type must be a string.")
            continue
        if val in ("CC", "CS"):
            return val
        print("Invalid build. Allowed values: CC, CS")


def prompt_addr():
    while True:
        val = input("Enter MAC or IPv6: ").strip()
        if not isinstance(val, str):
            print("MAC/IPv6 must be a string.")
            continue
        if val == "":
            print("MAC/IPv6 cannot be empty.")
            continue
        return val

def find_ip(macaddr):
    script = os.path.join(".", "getip.py")
    arguments = ["PROD", "CPE", macaddr] # Use the potentially overridden domain
    temp = run_script_and_get_result(script, arguments)
    return temp

def main():
    image = prompt_image()
    addr = prompt_addr()
    if addr:
        if is_ipv4(addr) or is_ipv6(addr):
            # Address argument is IP
            ipaddr = addr
            logging.debug(f"Using IP address from --addr: {addr}")
            
        elif is_mac(addr):
            logging.debug(f"Using MAC address from --addr: {addr}")
            ipaddr = find_ip(addr)
            if ipaddr is None:
                logging.error(f"Could not find IP address for MAC: {addr}")
                sys.exit(1)
    else:
        logging.error(f"The provided --addr value '{addr}' is neither a valid IP nor a valid MAC address.")
        sys.exit(1)



    cmd = [sys.executable, "ec.py", "--image", image, "--ip", ipaddr]
    try:
        subprocess.run(cmd, check=True)
        # After successful run of ec.py, run ds.py
        ds_cmd = [sys.executable, "ds.py", "--image", image, "--ip", ipaddr]
        try:
            subprocess.run(ds_cmd, check=True)
        except subprocess.CalledProcessError as e:
            print(f"ds.py exited with return code {e.returncode}")
        except FileNotFoundError:
            print("ds.py not found. Ensure ds.py is in the same directory.")
    except subprocess.CalledProcessError as e:
        print(f"ec.py exited with return code {e.returncode}")
    except FileNotFoundError:
        print("ec.py not found. Ensure ec.py is in the same directory.")


if __name__ == "__main__":
    main()
