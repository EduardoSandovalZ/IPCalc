import sys
import ipaddress

def ip_to_binary(ip):
    return ".".join(f"{int(octet):08b}" for octet in ip.split('.'))

def get_ip_class(ip):
    first_octet = int(ip.split('.')[0])
    if 1 <= first_octet <= 126:
        return 'A'
    elif 128 <= first_octet <= 191:
        return 'B'
    elif 192 <= first_octet <= 223:
        return 'C'
    return 'X'  # Desconocida

def calculate_network_info(ip_with_prefix):
    try:
        network = ipaddress.IPv4Network(ip_with_prefix, strict=False)
    except ValueError:
        print("Dirección IP no válida.")
        return

    ip = str(network.network_address)
    mask = str(network.netmask)
    wildcard = str(network.hostmask)
    broadcast = str(network.broadcast_address)
    cidr = network.prefixlen
    num_hosts = network.num_addresses - 2 if network.num_addresses > 2 else 0
    first_host = str(network.network_address + 1) if num_hosts > 0 else "N/A"
    last_host = str(network.broadcast_address - 1) if num_hosts > 0 else "N/A"
    
    
    print(f"\n----------SUMMARY----------\n")
    

    print(f"Class: {get_ip_class(ip)}")
    print(f"Decimal IP: {ip}/{cidr}")
    print(f"Binary IP: {ip_to_binary(ip)}\n")
    
    print(f"\n----------NETWORK----------\n")
    print(f"Decimal Network: {ip}/{cidr}")
    print(f"Binary Network: {ip_to_binary(ip)}\n")
    print(f"Decimal Mask: {mask}")
    print(f"Binary Mask: {ip_to_binary(mask)}")
    print(f"Decimal Broadcast: {broadcast}")
    print(f"Binary Broadcast: {ip_to_binary(broadcast)}\n")
    print(f"Decimal Wildcard: {wildcard}")
    print(f"Binary Wildcard: {ip_to_binary(wildcard)}\n")


    print(f"\n----------HOSTS----------\n")
    print(f"HostMin: {first_host}")
    print(f"HostMax: {last_host}")
    print(f"Hosts/Net: {num_hosts}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python script.py <IP> o <IP/CIDR>")
        sys.exit(1)
    
    ip_input = sys.argv[1]
    if '/' not in ip_input:
        ip_input += '/24'  # Valor predeterminado
    
    calculate_network_info(ip_input)
