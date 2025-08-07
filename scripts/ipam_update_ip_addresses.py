import sys
import os
import asyncio
import socket
import ipaddress
import socket
import argparse

# Add parent path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from netbox_utils.functions import get_ip_address, get_all_active_ipam_prefixes
from netbox_utils.config import netbox
from scapy.all import IP, ICMP, sr1

parser = argparse.ArgumentParser(description="Update IP addresses in NetBox")
parser.add_argument("--block-size", type=int, default=25, help="Number of IPs to process in each block")
parser.add_argument("--pause-duration", type=int, default=10, help="Pause duration between blocks in seconds")
parser.add_argument("--subnet", type=str, required=True, help="Subnet to scan (e.g. 172.30.2)")
args = parser.parse_args()

block_size = args.block_size
pause_duration = args.pause_duration
subnet = args.subnet


# --- ASYNC HELPERS ---

async def async_ping(ip):
    def ping():
        return sr1(IP(dst=str(ip)) / ICMP(), timeout=1, verbose=0)
    return await asyncio.to_thread(ping)

async def async_reverse_dns(ip):
    def resolve():
        try:
            return socket.gethostbyaddr(str(ip))[0]
        except socket.herror:
            return 'Unknown'
    return await asyncio.to_thread(resolve)

async def handle_host(ip, netbox):
    response = await async_ping(ip)
    if response is None:
        return

    dns_name = await async_reverse_dns(ip)
    ip_str = str(ip)
    address = ip_str + "/32"

    if dns_name.startswith('AP') or dns_name.startswith('LL'):
        print(f"{ip_str} - Skipped (Client endpoint)")
        return

    netbox_ipaddress = await asyncio.to_thread(get_ip_address, netbox, ip_str)

    if netbox_ipaddress is None:
        dns_to_set = dns_name if dns_name != 'Unknown' else 'unknown'
        payload = {
            "address": address,
            "status": 'active',
            "dns_name": dns_to_set
        }
        try:
            await asyncio.to_thread(netbox.ipam.ip_addresses.create, payload)
            print(f"Created new IP: {ip_str} - {dns_to_set}")
        except Exception as e:
            print(f"Failed to create {ip_str}: {e}")
    else:
        existing_dns = (netbox_ipaddress.dns_name or '').lower()
        new_dns = dns_name.lower()

        if dns_name != 'Unknown' and new_dns != existing_dns:
            # Overwrite only if different and not 'Unknown'
            try:
                netbox_ipaddress.dns_name = dns_name
                await asyncio.to_thread(netbox_ipaddress.save)
                print(f"Updated DNS for {ip_str} from '{existing_dns}' to '{dns_name}'")
            except Exception as e:
                print(f"Failed to update DNS for {ip_str}: {e}")
        elif dns_name == 'Unknown':
            # DNS not found, only set blank if existing is empty
            if not existing_dns:
                try:
                    netbox_ipaddress.dns_name = ''
                    await asyncio.to_thread(netbox_ipaddress.save)
                    print(f"Set DNS for {ip_str} to blank (no DNS found)")
                except Exception as e:
                    print(f"Failed to clear DNS for {ip_str}: {e}")
            else:
                print(f"{ip_str} DNS '{existing_dns}' present, no update needed")
        else:
            # dns_name == existing_dns, no change
            print(f"{ip_str} DNS '{existing_dns}' is up to date, no update needed")



async def process_subnet(subnet, netbox, block_size, pause_duration):
    hosts = list(ipaddress.ip_network(subnet).hosts())

    for i in range(0, len(hosts), block_size):
        block = hosts[i:i + block_size]
        print(f"\nScanning block {i // block_size + 1} with {len(block)} IPs...")

        tasks = [handle_host(ip, netbox) for ip in block]
        await asyncio.gather(*tasks)

        if i + block_size < len(hosts):
            print(f"Pausing {pause_duration}s before next block...")
            await asyncio.sleep(pause_duration)


async def main():
    active_prefixes = get_all_active_ipam_prefixes(netbox)
    target_prefixes = [str(p.prefix) for p in active_prefixes if str(p.prefix).startswith(subnet)]

    if not target_prefixes:
        print(f"No active prefixes found starting with {subnet}. Please check your input.")
        return

    for prefix in target_prefixes:
        print(f"\nStarting scan of subnet: {prefix}")
        await process_subnet(prefix, netbox, block_size, pause_duration)
        print("Finished scanning subnet. Pausing for 10 minutes...")
        await asyncio.sleep(10)  # Change this to a lower value for testing

if __name__ == "__main__":
    asyncio.run(main())
