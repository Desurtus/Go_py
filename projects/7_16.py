def decode(encoded_list):
    if len(encoded_list) == 0 or len(encoded_list) == 1:
        return encoded_list
    result = []
    element = encoded_list[0]
    repeats = encoded_list[1]
    for i in range(repeats):
        result.append(element)
    return result + decode(encoded_list[2:])

print(decode(["X", 3, "Z", 2, "X", 2, "Y", 3, "Z", 2]))