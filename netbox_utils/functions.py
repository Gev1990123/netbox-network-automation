import logging

#Setup Logging
logger = logging.getLogger(__name__)

#------------------
# REGION FUNCTIONS 
#------------------

def get_region(netbox, region_name):
    region = netbox.dcim.regions.get(name=region_name)
    if not region:
        logger.warning(f"Region'{region_name}' not found.")
    return region

#------------------
# SITE FUNCTIONS 
#------------------

def get_site(netbox, site_name):
    site = netbox.dcim.sites.get(name=site_name)
    if not site:
        logger.info(f"Site '{site_name}' not found.")
    return site

#------------------
# IPAM FUNCTIONS 
#------------------

def get_ipam_role(netbox, role_name):
    role = netbox.ipam.roles.get(name=role_name)
    if not role:
        logger.warning(f"IPAM Role '{role_name}' not found.")
    return role

def get_ipam_prefix(netbox, prefix):
    result = netbox.ipam.prefixes.get(prefix=prefix)
    if not result:
        logger.warning(f"IPAM Prefix '{prefix}' not found.")
    return result

def get_all_active_ipam_prefixes(netbox):
    return netbox.ipam.prefixes.filter(status="active")

def get_ip_address(netbox, ip_address):
    try:
        result = netbox.ipam.ip_addresses.get(address=ip_address)
        if not result:
            logger.warning(f"IP Address '{ip_address}' not found.")
        return result
    except Exception as e:
        logger.error(f"Error retrieving IP address '{ip_address}': {e}")
        return None

def get_dns_name_by_ip(netbox, ip_address):
    try:
        ip_obj = netbox.ipam.ip_addresses.get(address=ip_address)
        if ip_obj:
            return ip_obj.dns_name or "DNS name not set"
        else:
            return "IP address not found in NetBox"
    except Exception as e:
        logger.error(f"Error occurred while fetching DNS name for {ip_address}: {e}")
        return f"Error occurred: {e}"
    
def get_ip_addresses_from_prefix(netbox, prefix):
    try:
        # Get all IP addresses within the prefix
        ip_addresses = netbox.ipam.ip_addresses.filter(parent=prefix)
        return list(ip_addresses)
    except Exception as e:
        logger.error(f"Error retrieving IP addresses for prefix '{prefix}': {e}")
        return []
