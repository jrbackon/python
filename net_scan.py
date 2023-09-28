import nmap

nm = nmap.PortScanner()

def scan(net):
    return nm.scan(hosts=net, arguments='-sn')

def hosts(scan):
    host_list = []
    for host in scan['scan']:
        host_list.append(host)
    return host_list

def hostnames(hosts, scan):
    hostname_list = []
    for host in hosts:
        hostname_list.append(scan['scan'][host]['hostnames'][0]['name'])
    return hostname_list

def subnets(subnets):
    with open(subnets, 'r') as f:
        nets = f.readline().split(',')
    return nets

nets = subnets('server_subnets.txt')
with open('assets.csv', 'w+') as assets:
    assets.write('hostname, ip\n')
    for net in nets:
        result = scan(net)
        print(net + " has been scanned successfully.")
        endpoints = hosts(result)
        names = hostnames(endpoints, result)
        for i in range(len(endpoints)):
            assets.write(names[i] + ', ' + endpoints[i] + '\n')
