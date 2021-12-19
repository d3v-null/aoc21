import numpy as np

DEBUG = False

def parse_a_packet(tail):
    """
    Parse an entire packet, including subpackets, returning the value of the literal or operator
    expression, and remaining unprocessed input (the tail).
    """
    if len(tail) == 0:
        return 0, ''
    if all(c == '0' for c in tail):
        return 0, ''

    # get the version string, which is the first 3 digits of the binary string
    version_str, tail = tail[:3], tail[3:]
    version = int(version_str, 2)
    if DEBUG: print("ver", version_str, version)
    # get the type ID
    typeid_str, tail = tail[:3], tail[3:]
    typeid = int(typeid_str, 2)
    if DEBUG: print("typeid", typeid_str, typeid)

    if typeid == 4:
        # process a literal
        full_literal_str = ''
        continue_bit = 1
        while continue_bit:
            [continue_bit_str, *literal_word_str], tail = tail[:5], tail[5:]
            continue_bit = int(continue_bit_str, 2)
            full_literal_str += ''.join(literal_word_str)
        literal_value = int(full_literal_str, 2)
        if DEBUG: print(f"{full_literal_str=} {literal_value=}")
        return literal_value, tail

    # process an operator

    # get the length type id
    length_typeid_str, tail = tail[:1], tail[1:]
    length_typeid = int(length_typeid_str, 2)
    if DEBUG: print("length_typeid", length_typeid_str, length_typeid)

    subpacket_values = []

    if length_typeid == 1:
        num_subpackets_length = 11
        num_subpackets_str, tail = tail[:num_subpackets_length], tail[num_subpackets_length:]
        num_subpackets = int(num_subpackets_str, 2)

        for _ in range(num_subpackets):
            subpacket_value, tail = parse_a_packet(tail)
            subpacket_values.append(subpacket_value)
    else:
        # length_typeid == 0:
        subpackets_bit_length = 15

        subpacket_length_str, tail = tail[:subpackets_bit_length], tail[subpackets_bit_length:]
        subpacket_length = int(subpacket_length_str, 2)

        subpacket_tail, tail = tail[:subpacket_length], tail[subpacket_length:]

        while len(subpacket_tail) > 0:
            subpacket_value, subpacket_tail = parse_a_packet(subpacket_tail)
            subpacket_values.append(subpacket_value)

    if DEBUG: print(f"{subpacket_values=}, {typeid=}")
    value = None
    if typeid == 0:
        # sum of subpackets
        value = sum(subpacket_values)
    elif typeid == 1:
        # product of subpackets
        value = np.product(subpacket_values)
    elif typeid == 2:
        # minimum of subpackets
        value = min(subpacket_values)
    elif typeid == 3:
        # maximum of subpackets
        value = max(subpacket_values)
    elif typeid == 5:
        # value is 1 if the value of the first sub-packet is greater than the value of the second
        # sub-packet; otherwise, their value is 0. These packets always have exactly two sub-packets
        assert len(subpacket_values) == 2
        value = 1 if subpacket_values[0] > subpacket_values[1] else 0
    elif typeid == 6:
        # value is 1 if the value of the first sub-packet is less than the value of the second
        # sub-packet; otherwise, their value is 0. These packets always have exactly two sub-packets.
        assert len(subpacket_values) == 2
        value = 1 if subpacket_values[0] < subpacket_values[1] else 0
    elif typeid == 7:
        # value is 1 if the value of the first sub-packet is equal to the value of the second
        # sub-packet; otherwise, their value is 0. These packets always have exactly two sub-packets.
        assert len(subpacket_values) == 2
        value = 1 if subpacket_values[0] == subpacket_values[1] else 0
    else:
        raise ValueError(f"Unknown typeid: {typeid}")
    return value, tail


def main(tail):
    """
    >>> main("C200B40A82")
    3
    >>> main("04005AC33890")
    54
    >>> main("880086C3E88112")
    7
    >>> main("CE00C43D881120")
    9
    >>> main("D8005AC2A8F0")
    1
    >>> main("F600BC2D8F")
    0
    >>> main("9C005AC2F8F0")
    0
    >>> main("9C0141080250320F1802104A08")
    1
    """
    # given a hexadecimal string, create an np.ndarray of binary digits
    hex_digits = np.array([int(c, 16) for c in tail])
    # convert each hex digit to binary
    binary_str = ''.join([bin(d)[2:].zfill(4) for d in hex_digits])
    if DEBUG: print(binary_str)

    total_versions = 0
    tail = binary_str
    while len(tail) > 0:
        version, tail = parse_a_packet(tail)
        total_versions += version
    if DEBUG: print(f"{total_versions=}")
    return total_versions

if __name__ == "__main__":
    # LITERAL_EXAMPLE = """D2FE28"""
    # OPERATOR_EXAMPLE = """38006F45291200"""
    INPUT = """005532447836402684AC7AB3801A800021F0961146B1007A1147C89440294D005C12D2A7BC992D3F4E50C72CDF29EECFD0ACD5CC016962099194002CE31C5D3005F401296CAF4B656A46B2DE5588015C913D8653A3A001B9C3C93D7AC672F4FF78C136532E6E0007FCDFA975A3004B002E69EC4FD2D32CDF3FFDDAF01C91FCA7B41700263818025A00B48DEF3DFB89D26C3281A200F4C5AF57582527BC1890042DE00B4B324DBA4FAFCE473EF7CC0802B59DA28580212B3BD99A78C8004EC300761DC128EE40086C4F8E50F0C01882D0FE29900A01C01C2C96F38FCBB3E18C96F38FCBB3E1BCC57E2AA0154EDEC45096712A64A2520C6401A9E80213D98562653D98562612A06C0143CB03C529B5D9FD87CBA64F88CA439EC5BB299718023800D3CE7A935F9EA884F5EFAE9E10079125AF39E80212330F93EC7DAD7A9D5C4002A24A806A0062019B6600730173640575A0147C60070011FCA005000F7080385800CBEE006800A30C023520077A401840004BAC00D7A001FB31AAD10CC016923DA00686769E019DA780D0022394854167C2A56FB75200D33801F696D5B922F98B68B64E02460054CAE900949401BB80021D0562344E00042A16C6B8253000600B78020200E44386B068401E8391661C4E14B804D3B6B27CFE98E73BCF55B65762C402768803F09620419100661EC2A8CE0008741A83917CC024970D9E718DD341640259D80200008444D8F713C401D88310E2EC9F20F3330E059009118019A8803F12A0FC6E1006E3744183D27312200D4AC01693F5A131C93F5A131C970D6008867379CD3221289B13D402492EE377917CACEDB3695AD61C939C7C10082597E3740E857396499EA31980293F4FD206B40123CEE27CFB64D5E57B9ACC7F993D9495444001C998E66B50896B0B90050D34DF3295289128E73070E00A4E7A389224323005E801049351952694C000"""
    # main(LITERAL_EXAMPLE)
    # main(OPERATOR_EXAMPLE)
    # main("8A004A801A8002F478")
    EXAMPLE = "C200B40A82"
    print(f"{main(EXAMPLE)=}")
    print(f"{main(INPUT)=}")
