# import struct
import numpy as np

data_path = "data/problem_16.txt"
# data_path = "data/problem_16_test.txt"

# data = np.genfromtxt(data_path, dtype=int, delimiter=",")
# print(data)
data = "38006F45291200"


def hex_to_binary(hex_string):
    return np.unpackbits(np.frombuffer(bytes.fromhex(hex_string), dtype=np.uint8))

def print_bits(bit_array):
    print("".join([str(x) for x in bit_array]))

def binary_to_int(bits):
    exponents = np.arange(len(bits) - 1, -1, -1)
    return np.bitwise_or.reduce(bits.astype(np.int32) << exponents)

def parse_literal(bit_array, offset):
    chunk_count = np.argmin(bit_array[offset::5]) + 1 # get index of first 5-bit chunk starting with a 0
    # print(f"chunk_count: {chunk_count}")
    literal_length = chunk_count * 5

    # magically remove every 5th bit since that's not part of the number
    filtered_bits = np.delete(bit_array[offset:offset + literal_length], slice(None, None, 5))
    return binary_to_int(filtered_bits), literal_length

    # while True:
    #     chunk = bit_array[offset:offset + 5]
    #     offset += 5
    #     if chunk[0]

def parse_subpacket_length(bit_array, offset):
    length_type = bit_array[offset]
    length_size = 15 if length_type == 0 else 11
    length = binary_to_int(bit_array[offset + 1:offset + length_size + 1])

    return length_type, length, length_size + 1

# def parse_subpacket_count(bit_array):

def unpack_all(bit_array):
    offset = 0
    version = binary_to_int(bit_array[offset:offset + 3])
    offset += 3
    print(f"version: {version}")
    unpack_packet(bit_array, offset)

def unpack_packet(bit_array, offset):
    print_bits(bit_array)

    type_id = binary_to_int(bit_array[offset:offset + 3])
    offset += 3
    print(f"type_id: {type_id}")


    match type_id:
        case 4:
            literal_value, bits_read = parse_literal(bit_array, offset)
            print(f"literal_value: {literal_value}") #, literal_length = {literal_length}")
            offset += bits_read
        case _:
            subpacket_length_type, subpacket_length, bits_read = parse_subpacket_length(bit_array, offset)
            print(f"subpacket_length_type: {subpacket_length_type}, subpacket_length: {subpacket_length}, bits_read: {bits_read}")
            offset += bits_read


# 0b110100101111111000101000

# parse(hex_to_binary(data))

data = "001 110 00000000000110111101000101001010010001001000000000"

unpack_all(np.array([int(n) for n in "110 100 10111 11110 00101 000".replace(" ", "")], np.uint8))

# part 1
print(f"Part 1 solution: {None}")

# part 2
print(f"Part 2 solution: {None}")
