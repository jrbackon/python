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
    for ip in additions():
        spf_list.append(ip)
    return spf_list
    
    # create a list of all networks
# combine the two lists
# convert networks into IP addresses
# convert the IP strings to IP4 or IP6 objects
# sort the list
# convert the list back into a list of string objects
# compare the list of string addresses to the list of networks
    # if there is a match we replace the string address with the network
# add ip4: to the beginning of each item in the list
# calculate total number of sublists len(list) / 29
# add 29 addresses to each sublist
# add the spf info to each sublist
# convert each sublist to a string
    # write each list to a file

# print(create_spfList(load_record()))
#print(load_additions())
print(combine_lists(create_spfList(load_record()), load_additions()))
