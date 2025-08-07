import sys
import os
import argparse

# Add parent path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from netbox_utils.functions import get_ipam_prefix
from netbox_utils.helpers import subdivide_and_find
from netbox_utils.config import netbox

parser = argparse.ArgumentParser(description="Check available subnets in NetBox")
parser.add_argument("--parent", type=str, default="172.30.0.0/16", help="Parent prefix in NetBox")
parser.add_argument("--length", type=int, default=22, help="Desired prefix length")
args = parser.parse_args()

parent_prefix = args.parent
desired_prefix_length = args.length

# Get Parent Prefix

parent = get_ipam_prefix(netbox, parent_prefix)
if not parent:
    raise ValueError(f"Parent prefix {parent_prefix} not found in NetBox.")

# Find Available Subprefixes

available_prefixes = parent.available_prefixes.list()

# Find Directly Available Matching Prefixes
directly_available_prefixes = [p["prefix"] for p in available_prefixes if int(p["prefix"].split("/")[1]) == desired_prefix_length]

# Find Subdivided Prefixes
derived_prefixes = subdivide_and_find(available_prefixes, desired_prefix_length)

# Print Results
if directly_available_prefixes:
    print(f"✅ Available /{desired_prefix_length} blocks under {parent_prefix} (already present):")
    for prefix in directly_available_prefixes:
        print(f"  - {prefix}")


if derived_prefixes:
    print('')
    print(f"🧩 Available /{desired_prefix_length} blocks under {parent_prefix} (subdivided from larger blocks):")
    for child, parent in derived_prefixes:
        print(f"  - {child} (from {parent})")
 

if not directly_available_prefixes and not derived_prefixes:
    print(f"❌ No available /{desired_prefix_length} blocks found under {parent_prefix}.")
