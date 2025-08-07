# NetBox Automation Scripts

This repo contains Python scripts to automate tasks in NetBox, such as creating regions and sites.

---

## 📁 Project Structure (Recommended)
| Folder / File     | Description                                   |
|-------------------|-----------------------------------------------|
| scripts/          | Python automation scripts                     |
| netbox_utils/     | Shared helper functions and NetBox config     |
| data/             | Input CSV/YAML files                          |
| output/           | Generated output files (e.g., reports, logs)  |
| .env              | Environment variables (do not commit)         |
| requirements.txt  | Python dependencies                           |
| README.md         | Project documentation                         |


## ⚙️ Setup
### 1. Clone the repository
git clone https://github.com/Gev1990123/netbox-network-automation.git
cd netbox-network-automation

### 2. Configure environment variables
Create a .env file in the root directory with the following values:
NETBOX_URL=https://your-netbox-instance
NETBOX_API_TOKEN=your_api_token
NETBOX_VERIFY_SSL=False  # or True if using a valid certificate

### 3. Install Python dependencies
pip install -r requirements.txt

## 🚀 Scripts Overview
Each script is located in the scripts/ directory and can be run individually. Some require corresponding CSV files in the data/ folder.

| Script Name                   | Description                                   |
|-------------------------------|-----------------------------------------------|
| add_regions.py                | Adds predefined regions to NetBox             |
| add_site.py                   | Adds sites under regions                      |
| ipam_add_roles.py	            | Adds IPAM roles                               |
| ipam_add_prefixes.py	        | Creates prefixes based on a CSV               |
| ipam_add_ip_addresses.py	    | Creates IP addresses from a CSV               |
| ipam_find_cidr_available.py   | Finds available subnets by size               |
| ipam_update_ip_addresses.py   | Pings IP, does reverse DNS, updates netbox    |
| ipam_ip_address_lookup.py     | Exports DNS names for given IPs to CSV        |

## 📁 Data Files
Place your CSV files in the data/ folder. Ensure they follow the expected structure (column headers, no missing values).

## ✅ Output
Some scripts will generate results in the output/ folder (e.g., DNS lookup mappings).

## 🧪 Example
To run the IP address import:

python scripts/ipam_add_ip_addresses.py

Or to ping and register DNS:

python scripts/ipam_update_ip_addresses.py --subnet 172.30.2.0/24 --block-size 25 --pause-duration 10

For questions or improvements, feel free to open an issue or submit a PR.
