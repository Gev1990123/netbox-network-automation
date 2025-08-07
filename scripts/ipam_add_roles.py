import sys
import os
import csv
from pathlib import Path

# Add parent path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from netbox_utils.functions import get_ipam_role
from netbox_utils.config import netbox

# Resolve CSV path
base_dir = Path(__file__).resolve().parent.parent
csv_file_path = base_dir / "data" / "ipam_roles.csv"

def load_roles(csv_path):
    roles = []
    with open(csv_path, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            roles.append(row['role'].strip())
    return roles

role_names = load_roles(csv_file_path)

# Create each role
for role_name in role_names:
    slug = role_name.lower().replace(" ", "-")
    role_present = get_ipam_role(netbox, role_name)

    if role_present:
        print(f'{role_name} is already created. ')
    else:
        try:
            created_role = netbox.ipam.roles.create({
                "name": role_name,
                "slug": slug
            })
            print(f"Created Role: {role_name}")
        except Exception as e:
            print(f"❌ Error creating role {role_name}: {e}")