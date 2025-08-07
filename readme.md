# NetBox Automation Scripts

This repo contains Python scripts to automate tasks in NetBox, such as creating regions and sites.

## Setup

1. Clone the repo
2. Create a `.env` file with:
- NETBOX_URL=https://your-netbox-instance
- NETBOX_API_TOKEN=your_api_token
- NETBOX_VERIFY_SSL=(True / False)
3. Install dependencies:
- pip install -r requirements.txt
4. Run the scripts:
- add_regions.py
- add_site.py
- ipam_add_prefixes.py
- ipam_add_ip_addresses.py