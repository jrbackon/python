import nmap
import datetime

# assigns the portscanner to the variable nm.
nm = nmap.PortScanner()

today = f"{datetime.date.today()}.csv"

# scans the target
def scan(net):
    return nm.scan(hosts=net, arguments='-sn')

# creates a list of host ips discovered in the scan
def hosts(scan):
    return list(scan['scan'].keys())

# using the list of host ips this function creates a list of hostnames
def hostnames(hosts, scan):
    return [scan['scan'][host]['hostnames'][0]['name'] for host in hosts]

# this function reads in the list of subnets from a file and puts them in a python list
def subnets(subnets):
    with open(subnets, 'r') as f:
        return f.readline().strip().split(',')
     
# this code block iterates over each subnet and writes the scan output ip, hostname to a csv file.
nets = subnets(r'discovery_subnets\server_subnets.txt')
output_file = r'C:\Users\jbackon\OneDrive - Babson College\Assets\Discovery Scans\serverlist_' + today
with open(output_file, 'w+') as assets:
    assets.write('hostname, ip\n')
    for net in nets:
        result = scan(net)
        print(f"{net} has been scanned successfully.")
        endpoints = hosts(result)
        names = hostnames(endpoints, result)
        for name, endpoint in zip(names, endpoints):
            assets.write(f"{name}, {endpoint}\n")
