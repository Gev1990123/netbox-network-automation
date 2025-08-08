import sys
import os
import csv
from pathlib import Path
import argparse

# Add parent path for importing local modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from netbox_utils.config import netbox
from netbox_utils.helpers import calculate_utilisation
from netbox_utils.functions import get_all_active_ipam_prefixes, get_ip_addresses_from_prefix

parser = argparse.ArgumentParser(description="Generate IPAM prefix utilisation report")
parser.add_argument("--role", type=str, default="All", choices=["All", "Internal", "External"], help="Filter prefixes by role category (default: All)")
args = parser.parse_args()

INTERNAL_ROLES = {"data", "management", "video conferencing", "voice", "wireless"}


def get_role_category(role_name: str) -> str:
    role_name_norm = role_name.lower().strip()
    if role_name_norm == "external":
        return "external"
    elif role_name_norm in INTERNAL_ROLES or role_name_norm == "":
        # Treat empty or known internal roles as internal
        return "internal"
    else:
        return "other"

def include_prefix(role_name: str, filter_value: str) -> bool:
    category = get_role_category(role_name)
    if filter_value == "All":
        return True
    elif filter_value == "Internal":
        return category == "internal"
    elif filter_value == "External":
        return category == "external"
    return False

def main():
    output_dir = Path(__file__).resolve().parent.parent / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "prefix_utilisation_report.csv"

    prefixes = get_all_active_ipam_prefixes(netbox)

    print(f"{'Prefix':<18} {'Site':<18} {'VLAN':<30} {'Used IPs':<8} {'Total IPs':<9} {'Utilisation %':<12}")
    print("-" * 105)

    role_filter = args.role

    results = []
    for prefix in prefixes:
        role = getattr(prefix, "role", None)
        role_name = role.name if role else ""

        if include_prefix(role_name, role_filter):
            site = str(prefix.scope.display) if getattr(prefix, "scope", None) else "N/A"
            vlan = str(prefix.vlan.display) if getattr(prefix, "vlan", None) else "N/A"
            ip_addresses = get_ip_addresses_from_prefix(netbox, prefix.prefix)
            used_ips, total_ips, utilisation = calculate_utilisation(prefix, ip_addresses)
            results.append((prefix.prefix, site, vlan, used_ips, total_ips, utilisation))

    results.sort(key=lambda x: x[5], reverse=True)

    with output_file.open("w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Prefix", "Site", "VLAN", "Used IPs", "Total IPs", "Utilisation %"])

        for prefix_str, site, vlan, used, total, util in results:
            print(f"{prefix_str:<18} {site:<18} {vlan:<30} {used:<8} {total:<9} {util:.2f}%")
            writer.writerow([prefix_str, site, vlan, used, total, f"{util:.2f}"])

if __name__ == "__main__":
    main()