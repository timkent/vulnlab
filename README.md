# vulnlab
Scripts to control an "OSCP-like" lab environment.

# Scripts

## vulnlab.py

This script is a fully contained web control panel to allow resets of virtual machines within the lab. It uses Flask for the web server and https://github.com/vmware/pyvmomi to talk to ESX. In Debian 9, installing the "python3-flask" and "python3-pyvmomi" packages should be all that is required.

Please note this was written as a proof of concept and does not have sufficient error checking. Please submit a pull request if you have time to clean it up!

You will need to configure your ESX host details and the name of your control VM within the script. By default, the web server will listen on port 5000.

# Intended Use

Configure the lab machines so their hard drives are in "Independent - Non-persistent" mode. This means any disk changes to any of the lab VMs will not persist after a reset/power cycle.

Ideally you will want to have a second virtual NIC attached to your control VM that can talk to VMkernel so you don't have your ESX management interface directly on the VulnLab LAN.

Please let me know if you find this useful!
