# README: Checkmk to Ansible Inventory Script

## Overview
This Python script retrieves host information from a Checkmk instance, filters them based on specified folders, and generates an Ansible-compatible inventory file in YAML format. The inventory groups are dynamically created based on the folders specified in the configuration.

## Prerequisites
1. **Python 3.x**: Ensure you have Python 3 installed.
2. **Required Libraries**:
   - `requests`
   - `pyyaml`
   
   Install them using:
   ```bash
   pip install requests pyyaml
   ```
3. **Checkmk API Access**:
   - A valid Checkmk server URL.
   - API username and password with sufficient permissions.

## Configuration
### Modify the following options in the script:

- **Checkmk Server Details**:
  ```python
  HOST_NAME = "your.cmk.server"
  SITE_NAME = "mysite"
  PROTO = "https"  # [http|https]
  ```
  
- **Authentication**:
  ```python
  USERNAME = "your_username"
  PASSWORD = "your_password"
  ```

- **Folders to Filter**:
  Specify the Checkmk folders and their corresponding Ansible group names:
  ```python
  FOLDERS = {
      "/it/linux": "linux",
      "/os/winserver": "windows",
  }
  ```

- **Output File Name**:
  Define the name of the YAML file:
  ```python
  OUTPUT_FILE = "custom_hosts.yaml"
  ```

## How It Works
1. **API Call**: The script fetches all hosts from the Checkmk instance.
2. **Filtering**: Hosts are filtered based on their folder (e.g., `/it/linux`, `/it/winserver`).
3. **YAML File Generation**: The filtered hosts are grouped by folder and written to an Ansible-compatible YAML inventory file.

## Usage
1. Save the script to a file, e.g., `checkmk_to_ansible.py`.
2. Run the script:
   ```bash
   python3 checkmk_to_ansible.py
   ```
3. The script generates a YAML file (e.g., `custom_hosts.yaml`) in the current directory.

## Example Output
Here is an example of the generated YAML file:

```yaml
all:
  children:
    Linux:
      hosts:
        linux-host-1:
          ansible_host: 192.168.1.10
        linux-host-2:
          ansible_host: 192.168.1.11
    Windows:
      hosts:
        windows-host-1:
          ansible_host: 192.168.2.10
        windows-host-2:
          ansible_host: 192.168.2.11
```

## Error Handling
- If the API call fails, the script raises an exception with the API response.
- If a host does not contain the expected attributes (e.g., IP address), the script logs an error message but continues processing other hosts.

## Extending the Script
- **Adding More Groups**: Add additional folders and group names to the `FOLDERS` dictionary.
- **Custom Output**: Modify the `write_to_ansible_yaml` function to adjust the YAML structure.

## Troubleshooting
1. **401 Unauthorized**: Check your username and password.
2. **404 Not Found**: Ensure the API URL is correct and accessible.
3. **Dependencies Missing**: Install required libraries using `pip install requests pyyaml`.
