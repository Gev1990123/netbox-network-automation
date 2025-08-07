import sys
import os
import csv
from pathlib import Path

# Add parent path to import local modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from netbox_utils.functions import get_ip_address
from netbox_utils.config import netbox

# Load IP address data from CSV
def load_ip_addresses(csv_path):
    ip_addresses = []
    with open(csv_path, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            ip_addresses.append({
                'ipaddress': row['ipaddress'].strip(),
                'description': (row.get('description') or '').strip()
            })
    return ip_addresses

# Resolve path to CSV file
base_dir = Path(__file__).resolve().parent.parent
csv_file_path = base_dir / "data" / "ip_addresses_add.csv"

ip_data = load_ip_addresses(csv_file_path)

# Create IPs
for ip in ip_data:
    address = ip['ipaddress'] + '/32'

    ip_available = get_ip_address(netbox, address)

    if ip_available:
        print(f"⚠️ IP {address} already exists: {ip_available['display_url']}")
    else:
        ip_payload = {
            "address": address,
            "status": "active",
            "description": ip['description']
        }

        try:
            created_ip = netbox.ipam.ip_addresses.create(ip_payload)
            print(f"✅ Created IP: {ip['ipaddress']}, {created_ip['display']}")
        except Exception as e:
            print(f"❌ Failed to create IP {ip['ipaddress']}: {e}")
