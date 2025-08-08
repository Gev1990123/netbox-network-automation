import ipaddress

def subdivide_and_find(available_prefixes, desired_length):
    derived = []
    for prefix in available_prefixes:
        prefix_length = int(prefix["prefix"].split("/")[1])
        if prefix_length < desired_length:
            network = ipaddress.ip_network(prefix["prefix"])
            subnets = list(network.subnets(new_prefix=desired_length))
            for subnet in subnets:
                derived.append((str(subnet), prefix["prefix"]))
    return derived

def calculate_utilisation(prefix, ip_addresses):
    network = prefix.prefix 
    net = ipaddress.ip_network(network)
    total_ips = net.num_addresses
    used_ips = len(ip_addresses)

    utilisation = (used_ips / total_ips) * 100 if total_ips > 0 else 0

    return used_ips, total_ips, utilisation