import struct
# The conversion was gotten from Geek for Geeks: https://www.geeksforgeeks.org/program-for-conversion-of-32-bits-single-precision-ieee-754-floating-point-representation/
class FloatingPointConverter:
    def __init__(self):
        pass
    
    # Private helper functions. 
    @staticmethod
    def float_to_int_bits(f):
        # Pack the floating-point number into its binary representation
        packed_data = struct.pack('d', f)

        # Convert the packed binary data to an integer
        int_bits = int.from_bytes(packed_data, 'big')

        return int_bits

    @staticmethod
    def int_bits_to_float(int_bits):
        # Convert the integer to its binary representation as bytes
        packed_data = int_bits.to_bytes(8, 'big')

        # Unpack the binary data as a floating-point number
        float_value = struct.unpack('d', packed_data)[0]

        return float_value

 # Test the functions
# float_value = 7.935666576
# int_bits = FloatingPointConverter.float_to_int_bits(float_value)
# converted_float = FloatingPointConverter.int_bits_to_float(int_bits)

# print("Original Float Value:", float_value)
# print("Integer Bits:", int_bits)
# print("Converted Float Value:", converted_float)

# val = [11140104038263627584,14829452853005571135,11140104038263671103,11140104038263622464,0,1552698340489358143,7535064769459774015,3533263145447772991,11140104038263619904,11140104038263619904,11140104038263619904,11140104038263619904]
# for item in val:
#     print(FloatingPointConverter.int_bits_to_float(item))
# print(type(11140104038263622464))


print(str(FloatingPointConverter.float_to_int_bits(float(0))))