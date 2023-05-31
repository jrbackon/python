
import ipaddress

def view_record():
    with open("spf_05182023.txt", "r") as f:
        record = f.read()
        return record

def create_recordList():
    with open("spf_05182023.txt", "r") as f:
        records = f.readlines()
        spf = []
        for record in records:
            if record == "\n":
                pass
            else:
                spf.append(record.split())
        return spf

def view_subDomain(spf):
    subDomain = ""
    while subDomain != 'b':
        subDomain = input("Which subdomain would you like to view or input 'b' to go back? (NOTE: babson.edu = 0) ")
        if subDomain == "0":
            print(' '.join(spf[0]))
        elif subDomain == "1":
            print(' '.join(spf[1]))
        elif subDomain == "2":
            print(' '.join(spf[2]))
        elif subDomain == "3":
            print(' '.join(spf[3]))
        elif subDomain == "4":
            print(' '.join(spf[4]))
        elif subDomain == "5":
            print(' '.join(spf[5]))
        elif subDomain == "6":
            print(' '.join(spf[6]))
        elif subDomain == "7":
            print(' '.join(spf[7]))
        elif subDomain == "8":
            print(' '.join(spf[8]))
        elif subDomain == "9":
            print(' '.join(spf[9]))
        else:
            print("Please enter a number '1-9' or 'b' to go back.")


def create_recordDict(spf):
    dict_spf = {i : [] for i in range(len(spf))}
    for i in range(len(spf)):
        for ip in spf[i]:
            if "babson.edu" in ip or "v=spf1" in ip or "~all" in ip:
                pass
            elif "/" in ip:
                ip = ip.split("/", 1)[0]
                if "ip6" in ip:
                    dict_spf[i].append(ipaddress.ip_address(ip.replace("ip6:", '')))
                else:
                    dict_spf[i].append(ipaddress.ip_address(ip.replace("ip4:", '')))
            elif "ip6" in ip:
                    dict_spf[i].append(ipaddress.ip_address(ip.replace("ip6:", '')))
            else:
                    dict_spf[i].append(ipaddress.ip_address(ip.replace("ip4:", '')))
    return dict_spf

def record_location(ip):
# check if ip is a host or a network
    if "/" in ip:
        # if a network, remove the cidr notation
        temp_ip = ip.split("/", 1)[0]
        temp_ip = ipaddress.ip_address(temp_ip)
    else:
        temp_ip = ipaddress.ip_address(ip)
# check if ip is greater than last entry in record
    temp_record = create_recordDict(create_recordList())
    for i in range(len(temp_record)):
        try:
            if temp_ip > temp_record[i][-1]:
                # if it is move on to the next
                pass
            else:
            # if it isn't add to the record and sort
                temp_record[i].append(temp_ip)
                temp_record[i] = sorted(temp_record[i])
                location = temp_record[i].index(temp_ip)
                break
        except TypeError:
            pass

    return (i, location, ip)

def add_record(i, location, ip):
    # call create_recordList to generate the existing record as a list of lists
    record = create_recordList()
    # insert the new ip/network at the given location
    if ":" in ip:
        record[i].insert(location, "ip6:"+ip)
    else:
        record[i].insert(location, "ip4:"+ip)
    # call check_limit
    final_record = check_limit(record)
    # convert lists to strings
    output = ''
    for i in range(len(final_record)):
        output += "\n" + "\n" + ' '.join(final_record[i])

    return output

def check_limit(temp_record):
    limit = 30
    # loop through record
    for i in range(len(temp_record)):
    # if record is greater than limit
        if len(temp_record[i]) >= limit:
        # take last ip and remove from current record
            switch = temp_record[i][-3]
            temp_record[i].remove(switch)
        # add to the next record
            temp_record[i+1].insert(2, switch)
    return temp_record

def print_record(output):
    with open("spf_record_new", "w") as f:
        f.write(output)

def main():
    selection = ""
    while selection != "q":
        print("-"*60)
        print(" " * 25 + "SPF EDITOR")
        print("-"*60)
        print("1) View the current full record")
        print("2) View a specific subdomain")
        print("3) Add an IP to the current record")
        print("4) Output the record to a file")
        print("q) Quit")
        print()
        selection = input("Please make a selection: ")
        if selection == "1":
            print(view_record())
        elif selection == "2":
            print(view_subDomain(create_recordList()))
        elif selection == "3":
            ip = input("What is the IP address or network you would like to add? ")
            output = (add_record(record_location(ip)[0], record_location(ip)[1]+2, record_location(ip)[2]))
            print(output)
        elif selection == "4":
            print_record(output)

main()