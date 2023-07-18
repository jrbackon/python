from dns import resolver, reversename

with open('ip.txt', 'r') as f:
    addresses = f.readlines()
    hostnames = []
    for address in addresses:
        try:
            addr = reversename.from_address(address[:-1])
            hostnames.append(address[:-1] + ", " + str(resolver.resolve(addr, "PTR")[0]))
        except:
            hostnames.append(address[:-1] + ", " + "The DNS query name does not exist")

    with open('hostnames.csv', 'w', newline='') as g:
        for name in hostnames:
            g.write(name + "\n")
            
