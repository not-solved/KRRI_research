data = [0x02, 0x00, 0x2D, 0xFF, 0x01, 0x00, 0x00]
result = 0
for i in data :
    result ^= i
print(hex(result))
