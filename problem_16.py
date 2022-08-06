import json
import dataclasses
from dataclasses import dataclass

# import struct
import numpy as np

data_path = "data/problem_16.txt"
# data_path = "data/problem_16_test.txt"

with open(data_path, "r") as f:
    data = f.read().strip()


def hex_to_binary(hex_string):
    return np.unpackbits(np.frombuffer(bytes.fromhex(hex_string), dtype=np.uint8))


def bits_to_string(bit_array):
    return "".join([str(x) for x in bit_array])


@dataclass
class Packet:
    version: int = None

    @staticmethod
    def _binary_to_int(bits):
        exponents = np.arange(len(bits) - 1, -1, -1)
        return np.bitwise_or.reduce(bits.astype(np.int64) << exponents)

    @classmethod
    def unpack(cls, bit_array, start=0):
        """Returns tuple of [packet, bits read]"""
        # print(bits_to_string(bit_array[start:]))
        offset = start
        version = cls._binary_to_int(bit_array[offset:offset + 3])
        offset += 3

        type_id = cls._binary_to_int(bit_array[offset:offset + 3])
        offset += 3

        packet, bits_read = PACKET_TYPE_MAP[type_id].unpack(version, bit_array, offset)
        offset += bits_read

        if start == 0:
            return packet
        else:
            return packet, offset - start


    def get_version_sum(self):
        if isinstance(self, OperatorPacket):
            return self.version + sum((subpacket.get_version_sum() for subpacket in self.subpackets))
        else:
            return self.version

    def print_tree(self, indent_level=0):
        string = " " * (indent_level * 2) + "- "

        if isinstance(self, LiteralPacket):
            string += str(self.value)
        else:
            assert isinstance(self, OperatorPacket)
            string += self.__class__.__name__.replace("Packet", "") + " = " + str(self.evaluate())

            for subpacket in self.subpackets:
                # subpacket_string = subpacket.get_string(indent_level=indent_level + 1)
                string += "\n" + subpacket.print_tree(indent_level=indent_level + 1)

        if indent_level == 0:
            print(string)
        else:
            return string


@dataclass
class LiteralPacket(Packet):
    value: int = None

    @classmethod
    def _unpack_literal_value(cls, bit_array, start):
        chunk_count = np.argmin(bit_array[start::5]) + 1 # get index of first 5-bit chunk starting with a 0
        literal_length = chunk_count * 5

        # magically remove every 5th bit since that's not part of the number
        filtered_bits = np.delete(bit_array[start:start + literal_length], slice(None, None, 5))
        return cls._binary_to_int(filtered_bits), literal_length

    @classmethod
    def unpack(cls, version, bit_array, start):
        literal_value, bits_read = cls._unpack_literal_value(bit_array, start)
        return cls(version=version, value=literal_value), bits_read

    def evaluate(self):
        return self.value


@dataclass
class OperatorPacket(Packet):
    subpackets: list = None

    def evaluate_subpackets(self):
        return [s.evaluate() for s in self.subpackets]

    @classmethod
    def _parse_subpacket_length(cls, bit_array, offset):
        length_type = bit_array[offset]
        length_size = 15 if length_type == 0 else 11
        length = cls._binary_to_int(bit_array[offset + 1:offset + length_size + 1])

        return length_type, length, length_size + 1

    @classmethod
    def unpack(cls, version, bit_array, start):
        offset = start
        subpacket_length_type, subpacket_length, bits_read = cls._parse_subpacket_length(bit_array, offset)
        offset += bits_read

        subpackets = []
        if subpacket_length_type == 0:
            subpacket_offset = 0
            while subpacket_offset < subpacket_length:
                subpacket, bits_read = Packet.unpack(bit_array, start=offset + subpacket_offset)
                subpackets.append(subpacket)
                subpacket_offset += bits_read

            offset += subpacket_offset
        else:
            for i in range(subpacket_length):
                subpacket, bits_read = Packet.unpack(bit_array, start=offset)
                subpackets.append(subpacket)
                offset += bits_read

        packet = cls(version=version, subpackets=subpackets)

        return packet, offset - start

@dataclass
class SumPacket(OperatorPacket):
    def evaluate(self):
        return np.sum(self.evaluate_subpackets())

@dataclass
class ProductPacket(OperatorPacket):
    def evaluate(self):
        return np.prod(self.evaluate_subpackets())

@dataclass
class MinimumPacket(OperatorPacket):
    def evaluate(self):
        return np.min(self.evaluate_subpackets())

@dataclass
class MaximumPacket(OperatorPacket):
    def evaluate(self):
        return np.max(self.evaluate_subpackets())

@dataclass
class GreaterThanPacket(OperatorPacket):
    def evaluate(self):
        assert len(self.subpackets) == 2
        return np.int64(self.subpackets[0].evaluate() > self.subpackets[1].evaluate())

@dataclass
class LessThanPacket(OperatorPacket):
    def evaluate(self):
        assert len(self.subpackets) == 2
        return np.int64(self.subpackets[0].evaluate() < self.subpackets[1].evaluate())

@dataclass
class EqualToPacket(OperatorPacket):
    def evaluate(self):
        assert len(self.subpackets) == 2
        return np.int64(self.subpackets[0].evaluate() == self.subpackets[1].evaluate())


PACKET_TYPE_MAP = (
    SumPacket,          # 0
    ProductPacket,      # 1
    MinimumPacket,      # 2
    MaximumPacket,      # 3
    LiteralPacket,      # 4
    GreaterThanPacket,  # 5
    LessThanPacket,     # 6
    EqualToPacket,      # 7
)


# part 1
top_level_packet = Packet.unpack(hex_to_binary(data))
# top_level_packet = Packet.unpack(hex_to_binary("04005AC33890"))
# top_level_packet.print_tree()
print(f"Part 1 solution: {top_level_packet.get_version_sum()}")

# part 2
test_cases = (
    ("C200B40A82", 3),
    ("04005AC33890", 54),
    ("880086C3E88112", 7),
    ("CE00C43D881120", 9),
    ("D8005AC2A8F0",  1),
    ("F600BC2D8F", 0),
    ("9C005AC2F8F0", 0),
    ("9C0141080250320F1802104A08", 1),
)
for test_case, expected_value in test_cases:
    test_packet = Packet.unpack(hex_to_binary(test_case))
    assert test_packet.evaluate() == expected_value

print(f"Part 2 solution: {top_level_packet.evaluate()}")


