import sys
import os
import csv
from pathlib import Path

# Add parent path for importing local modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from netbox_utils.config import netbox
from netbox_utils.functions import get_dns_name_by_ip

# File paths
base_dir = Path(__file__).resolve().parent.parent
input_csv = base_dir / "data" / "ipam_ip_address_lookup.csv"
output_csv = base_dir / "output" / "ip_dns_mapping.csv"

# Ensure output directory exists
output_csv.parent.mkdir(parents=True, exist_ok=True)

with input_csv.open(mode='r', newline='') as infile, output_csv.open(mode='w', newline='') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)
    writer.writerow(["IP Address", "DNS Name"])

    next(reader, None)  # Skip header row

    for row in reader:
        if row:
            ip = row[0].strip()
            dns_name = get_dns_name_by_ip(netbox, ip)
            print(f"Processing {ip} → {dns_name}")
            writer.writerow([ip, dns_name])
