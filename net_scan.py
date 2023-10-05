import nmap
# assigns the portscanner to the variable nm.
nm = nmap.PortScanner()

# scans the target
def scan(net):
    return nm.scan(hosts=net, arguments='-sn')

# creates a list of host ips discovered in the scan
def hosts(scan):
    host_list = []
    for host in scan['scan']:
        host_list.append(host)
    return host_list

# using the list of host ips this function creates a list of hostnames
def hostnames(hosts, scan):
    hostname_list = []
    for host in hosts:
        hostname_list.append(scan['scan'][host]['hostnames'][0]['name'])
    return hostname_list

# this function reads in the list of subnets from a file and puts them in a python list
def subnets(subnets):
    with open(subnets, 'r') as f:
        nets = f.readline().split(',')
    return nets

# this code block iterates over each subnet and writes the scan output ip, hostname to a csv file.
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
