def _xor_operation(buffer_a, buffer_b):
    cypher = []
    for i in range(len(buffer_a)):
        cypher.append(buffer_a[i] ^ buffer_b[i])

    cypher = bytes(cypher)

    return cypher