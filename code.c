
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <arpa/inet.h>

void print_binary(unsigned int num) {
    for (int i = 31; i >= 0; i--) {
        printf("%d", (num >> i) & 1);
        if (i % 8 == 0 && i != 0) printf(".");
    }
    printf("\n");
}

void print_decimal(unsigned int num) {
    printf("%u.%u.%u.%u", (num >> 24) & 0xFF, (num >> 16) & 0xFF, (num >> 8) & 0xFF, num & 0xFF);
}

char get_ip_class(unsigned int ip) {
    unsigned int first_octet = (ip >> 24) & 0xFF;
    if (first_octet >= 1 && first_octet <= 126) return 'A';
    if (first_octet >= 128 && first_octet <= 191) return 'B';
    if (first_octet >= 192 && first_octet <= 223) return 'C';
    return 'X';  // Desconocida
}

void calculate_network_info(unsigned int ip, int cidr) {
    unsigned int mask = (cidr == 0) ? 0 : (~0U << (32 - cidr));
    unsigned int wildcard = ~mask;
    unsigned int network = ip & mask;
    unsigned int broadcast = network | wildcard;
    
    unsigned int host_min = (cidr < 31) ? (network + 1) : 0;
    unsigned int host_max = (cidr < 31) ? (broadcast - 1) : 0;
    unsigned int num_hosts = (cidr < 31) ? ((1U << (32 - cidr)) - 2) : 0;

    printf("Clase de IP: %c\n\n", get_ip_class(ip));
    
    printf("IP en decimal: "); print_decimal(ip); printf("/%d\n", cidr);
    printf("IP en binario: "); print_binary(ip);
    printf("\n");

    printf("Máscara de red en decimal: "); print_decimal(mask); printf("\n");
    printf("Máscara de red en binario: "); print_binary(mask);
    printf("Wildcard en decimal: "); print_decimal(wildcard); printf("\n");
    printf("Wildcard en binario: "); print_binary(wildcard); printf("\n");
    
    printf("Dirección de red en decimal: "); print_decimal(network); printf("/%d\n", cidr);
    printf("Dirección de red en binario: "); print_binary(network);
    printf("\n");
    
    printf("Dirección de broadcast en decimal: "); print_decimal(broadcast); printf("\n");
    printf("Dirección de broadcast en binario: "); print_binary(broadcast);
    printf("\n");
    
    if (cidr < 31) {
        printf("Primer host en decimal: "); print_decimal(host_min); printf("\n");
        printf("Último host en decimal: "); print_decimal(host_max); printf("\n");
    } else {
        printf("Primer host en decimal: N/A\n");
        printf("Último host en decimal: N/A\n");
    }
    
    printf("Número de hosts utilizables: %u\n", num_hosts);
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("Uso: %s <IP> o <IP/CIDR>\n", argv[0]);
        return 1;
    }

    char ip[INET_ADDRSTRLEN];
    int cidr = -1;
    char *slash = strchr(argv[1], '/');

    if (slash) {
        *slash = '\0';
        cidr = atoi(slash + 1);
        if (cidr < 0 || cidr > 32) {
            printf("Prefijo CIDR no válido.\n");
            return 1;
        }
    } else {
        cidr = 24;  // Valor predeterminado
    }

    strncpy(ip, argv[1], sizeof(ip) - 1);
    ip[sizeof(ip) - 1] = '\0';

    struct in_addr addr;
    if (inet_pton(AF_INET, ip, &addr) != 1) {
        printf("Dirección IP no válida.\n");
        return 1;
    }

    unsigned int ip_num = ntohl(addr.s_addr);

    calculate_network_info(ip_num, cidr);

    return 0;
}
