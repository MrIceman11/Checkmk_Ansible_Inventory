#!/usr/bin/env python3
import pprint
import requests
import yaml

# Configuration Options
HOST_NAME = "your.cmk.server"
SITE_NAME = "mysite"
PROTO = "https" #[http|https]
API_URL = f"{PROTO}://{HOST_NAME}/{SITE_NAME}/check_mk/api/1.0"

USERNAME = "user"
PASSWORD = "password"

# Folders to filter and corresponding Ansible groups
FOLDERS = {
    "/linux": "linux",
    "/os/winserver": "windows",
}

# Output file name
OUTPUT_FILE = "custom_hosts.yaml"

session = requests.session()
session.headers['Authorization'] = f"Bearer {USERNAME} {PASSWORD}"
session.headers['Accept'] = 'application/json'

resp = session.get(
    f"{API_URL}/domain-types/host_config/collections/all",
    params={  # goes into query string
        "effective_attributes": False,  # Show all effective attributes on hosts, not just the attributes which were set on this host specifically.
        "include_links": False,  # Flag which toggles whether the links field of the individual hosts should be populated.
    },
)

def filter_hosts_by_folder(hosts, folder):
    """Filters hosts by the specified folder and extracts their names and IPs."""
    filtered_hosts = []
    try:
        for host in hosts.get('value', []):
            host_folder = host.get('extensions', {}).get('folder', '').lower()
            if host_folder == folder:
                host_name = host.get('title', 'Unknown')
                host_ip = host.get('extensions', {}).get('attributes', {}).get('ipaddress', 'Unknown')
                filtered_hosts.append({"name": host_name, "ip": host_ip})
    except AttributeError as e:
        print(f"Error processing hosts: {e}")
    return filtered_hosts

def write_to_ansible_yaml(folder_hosts, filename):
    """Writes the hosts to an Ansible-compatible YAML inventory file."""
    inventory = {
        "all": {
            "children": {
                group: {
                    "hosts": {host["name"]: {"ansible_host": host["ip"]} for host in hosts}
                } for folder, group in FOLDERS.items() for hosts in [folder_hosts.get(folder, [])]
            }
        }
    }

    with open(filename, "w") as yaml_file:
        yaml.dump(inventory, yaml_file, default_flow_style=False)

    print(f"Inventory written to {filename}")

if resp.status_code == 200:
    all_hosts = resp.json()

    # Filter hosts for the specified folders
    folder_hosts = {
        folder: filter_hosts_by_folder(all_hosts, folder)
        for folder in FOLDERS.keys()
    }

    # Write to Ansible-compatible YAML inventory
    write_to_ansible_yaml(folder_hosts, OUTPUT_FILE)
else:
    raise RuntimeError(pprint.pformat(resp.json()))
