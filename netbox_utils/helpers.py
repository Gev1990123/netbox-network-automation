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