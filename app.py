from main import CalculoIPv4

app = CalculoIPv4(ip='192.168.0.1', mascara='255.255.255.0')

print(f'IP Address: {app.ip}')
print(f'Network Address: {app.rede}')
print(f'Broadcast Address: {app.broadcast}')
print(f'Total Number of Hosts: {app.numero_ips}')
print(f'Subnet Mask: {app.mascara}')
print(f'CIDR Notation: /{app.prefixo}')
