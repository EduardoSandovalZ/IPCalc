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

    print(f"Clase de IP: {get_ip_class(ip)}\n")
    print(f"IP en decimal: {ip}/{cidr}")
    print(f"IP en binario: {ip_to_binary(ip)}\n")
    print(f"Máscara de red en decimal: {mask}")
    print(f"Máscara de red en binario: {ip_to_binary(mask)}")
    print(f"Wildcard en decimal: {wildcard}")
    print(f"Wildcard en binario: {ip_to_binary(wildcard)}\n")
    print(f"Dirección de red en decimal: {ip}/{cidr}")
    print(f"Dirección de red en binario: {ip_to_binary(ip)}\n")
    print(f"Dirección de broadcast en decimal: {broadcast}")
    print(f"Dirección de broadcast en binario: {ip_to_binary(broadcast)}\n")
    print(f"Primer host en decimal: {first_host}")
    print(f"Último host en decimal: {last_host}")
    print(f"Número de hosts utilizables: {num_hosts}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python script.py <IP> o <IP/CIDR>")
        sys.exit(1)
    
    ip_input = sys.argv[1]
    if '/' not in ip_input:
        ip_input += '/24'  # Valor predeterminado
    
    calculate_network_info(ip_input)
