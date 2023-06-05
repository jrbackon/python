import ipaddress
import math

# load the existing record
def load_record():
    record = input("What is the path of the existing spf record? ")
    with open(record, 'r') as f:
        spf = f.readlines()
    return spf
# create a list of all IPs
def create_spfList(spf):
    spf_list = []
    address_list = []
    for item in spf:
        spf_list.append(item.split())
    
    flattenlist = sum(spf_list,[])
    for item in flattenlist:
        if "ip4:" in item:
            address_list.append(item[4:])
    return address_list

# load the list of IPs to be added
def load_additions():
    additions = input("What is the path of the file with the IP additions? ")
    with open(additions, 'r') as f:
        new_ips = f.readlines()
        new_list = []
        for ip in new_ips:
            if "\n" in ip:
                new_list.append(ip[:-1])
            else:
                new_list.append(ip)
    
    return new_list
# create a list of all IPs
def combine_lists(spf_list, additions):
    for ip in additions:
        spf_list.append(ip)
    return spf_list
    
# create a list of all networks
def network_list(spf_list):
    networks = []
    for address in spf_list:
        if "/" in address:
            networks.append(address)
    return networks

# convert networks into IP addresses
# convert the IP strings to IP4 or IP6 objects
# sort the list
def address_convert(spf_list):
    converted_list = []
    for address in spf_list:
        if "/" in address:
            converted_list.append(ipaddress.ip_address(address.split("/", 1)[0]))
        else:
            converted_list.append(ipaddress.ip_address(address))
    return sorted(converted_list)

# convert the list back into a list of string objects
def sorted_strings(converted_list):
    string_list = []
    for address in converted_list:
        string_list.append(str(address))
    return string_list

# compare the list of string addresses to the list of networks
# if there is a match we replace the string address with the network
# add ip4: to the beginning of each item in the list
def network_replace(string_list, network_list):
    formatted_list = []
    for address in string_list:
        for network in network_list:
            if network.split("/", 1)[0] == address:
                formatted_list.append("ip4:"+network)
            else:
                pass
        formatted_list.append("ip4:"+address)
    return formatted_list


# add 26 addresses to each sublist
def add_toRecords(formatted_list, sublists):
    record_dict = {}
    location = 0
    for i in range(sublists):
        count = 0
        record_dict[i] = []
        for address in formatted_list:
            try:
                if count <= 26:
                    record_dict[i].append(formatted_list[location + count])
                    count += 1
                else:
                    location = location + count
                    break
            except IndexError:
                break
    return record_dict

# add the spf info to each sublist
def add_recordInfo(record_dict):
    for i in range(len(record_dict)):
        if i == 0:
            record_dict[i].insert(0, "babson.edu")
            record_dict[i].insert(1, "v=spf1")
            record_dict[i].append("include :spf"+str(i+1)+".babson.edu ~all")
        elif i == len(record_dict):
            record_dict[i].insert(0, "spf"+str(i)+".babson.edu")
            record_dict[i].insert(1, "v=spf1")
            record_dict[i].append("~all")
        else:
            record_dict[i].insert(0, "spf"+str(i)+".babson.edu")
            record_dict[i].insert(1, "v=spf1")
            record_dict[i].append("include:spf"+str(i+1)+".babson.edu ~all")
    return record_dict

# convert each sublist to a string
    # write each list to a file

# print(create_spfList(load_record()))
#print(load_additions())
combined_record = combine_lists(create_spfList(load_record()), load_additions())
network_list = network_list(combined_record)
sorted_list = sorted_strings(address_convert(combined_record))
# print(network_replace(sorted_list, network_list))

# calculate total number of sublists len(list) / 29
sublists = math.ceil(len(network_replace(sorted_list, network_list))/29)
record_dict = add_toRecords(network_replace(sorted_list, network_list), sublists)
print(add_recordInfo(record_dict))