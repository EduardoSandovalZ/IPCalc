
import ipaddress
import argparse

def subnet_fixed(network, num_subnets):
    try:
        net = ipaddress.IPv4Network(network, strict=False)
        new_prefix = net.prefixlen + (num_subnets - 1).bit_length()
        subnets = list(net.subnets(new_prefix=new_prefix))
        
        print(f"División de {network} en {num_subnets} subredes:")
        for i, subnet in enumerate(subnets[:num_subnets]):
            print(f"Subred {i+1}: {subnet} - Hosts utilizables: {subnet.num_addresses - 2}")
    except ValueError:
        print("Error: No se pueden crear tantas subredes con la máscara dada.")

def subnet_vlsm(network, host_requirements):
    net = ipaddress.IPv4Network(network, strict=False)
    sorted_hosts = sorted(host_requirements, reverse=True)
    allocated_subnets = []
    
    current_network = net.network_address
    for hosts in sorted_hosts:
        needed_prefix = 32 - (hosts + 2 - 1).bit_length()
        try:
            subnet = ipaddress.IPv4Network((current_network, needed_prefix), strict=False)
            allocated_subnets.append(subnet)
            current_network = subnet.broadcast_address + 1
        except ValueError:
            print("Error: No se pueden acomodar todas las subredes con VLSM.")
            return
    
    print(f"División de {network} con VLSM:")
    for i, subnet in enumerate(allocated_subnets):
        print(f"Subred {i+1}: {subnet} - Hosts utilizables: {subnet.num_addresses - 2}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Herramienta de subnetting")
    parser.add_argument("network", type=str, help="Red en formato CIDR (ej. 192.168.1.0/24)")
    parser.add_argument("-n", type=int, help="Número de subredes fijas", default=None)
    parser.add_argument("-v", nargs='+', type=int, help="Lista de requerimientos de hosts para VLSM", default=None)
    
    args = parser.parse_args()
    
    if args.n:
        subnet_fixed(args.network, args.n)
    elif args.v:
        subnet_vlsm(args.network, args.v)
    else:
        print("Debe especificar -n para subredes fijas o -v para VLSM.")
