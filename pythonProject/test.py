import binascii
ReceivedData = "02005300000032384c37303833384c3730383300000000010000000000001507170f111d06000000000000000000bd3b710037343230383631ab03"

def len_in_header(str) :
    return int(str)

def date_in_data(str) :
    return str[60:72]

def tagged_ID(str) :
    return str[92:98]

def direction_check(str):
    if str[47:48] == "1":
        return "Out Way"
    elif str[47:48] == "0" :
        return "In Way"



header = ReceivedData[0:2*7]
print(header)
print("Time (hex) : ", date_in_data(ReceivedData))
print("Tagged ID : ", tagged_ID(ReceivedData))
print(ReceivedData[47:48])
print(direction_check(ReceivedData))
# print(int("33")//10 * 16 + int("33") % 10)


CardList = ["8f4fbb", "120908", "bd3b71", "7d6974"]

def is_in_list(str):
    for c in CardList:
        if str == c:
            return True
    return False

print(is_in_list("8f4fbb"))

