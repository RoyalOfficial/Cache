import math;
def calculate_amount_of_sets(number_of_blocks, set_associativity):
    """
    The function calculates the amount of sets based on the number of blocks and set associativity.
    
    :param number_of_blocks: The `number_of_blocks` parameter represents the total number of blocks
    in a cache or memory system
    :param set_associativity: The `set_associativity` parameter represents the number of blocks that can
    be mapped to a single set in a cache memory system. It is used to calculate the number of sets
    in the cache
    :return: the amount of sets in the cache.
    """
    amount_of_sets = int(number_of_blocks / set_associativity)
    return amount_of_sets 

def calculate_real_size(nominal_size_value,tag_size):
    """
    The function calculates the real size based on a nominal size value and a tag size.
    
    :param nominal_size_value: The `nominal_size_value` parameter represents the base value of the size.
    It is the starting point for calculating the real size
    :param tag_size: Tag size is the size of the tag in bits
    :return: The function `calculate_real_size` returns the calculated real size value based on the
    formula provided in the function.
    """
    
    real_size = nominal_size_value + ((int(tag_size) )/8)* (2**16)
    return real_size

def calculate_tag_sizeDM(number_of_blocks, offset):
    """
    The function calculates the tag size based on the number of blocks and offset.
    
    :param number_of_blocks: The `number_of_blocks` parameter represents the total number of blocks
    in a cache or memory system
    :param offset: The `offset` parameter in the `calculate_tag_size` function represents the number of bits
    used for the offset within a block. It is used to calculate the tag size by determining how many bits
    are needed to represent the number of blocks
    :return: the tag size in bits.
    """
    
    tag_size = (32 - math.log2(int(number_of_blocks)) - int(offset))
    return tag_size

def calculate_number_of_blocks(nominal_size_value, block_size):
    """
    The function calculates the number of blocks that can fit within a given nominal size based on a
    specified block size.
    
    :param nominal_size: The `nominal_size` parameter represents the total size of the material in
    blocks
    :param block_size: The `block_size` parameter in the `calculate_number_of_blocks` function
    represents the size of each block in the calculation. This value is used to determine how many
    blocks can fit into the `nominal_size`
    :return: the number of blocks that can be created from a given nominal size and block size.
    """
    
    nominal_size = int(nominal_size_value)
    block_size = int(block_size)
    return nominal_size // block_size


def calculate_block_size(word_per_block):
    """
    The function calculates the block size based on the number of words per block.
    
    :param word_per_block: It looks like the function `calculate_block_size` takes a parameter `word_per_block`
    which represents the number of words in a block. The function calculates the block size based on this
    input
    :return: The function `calculate_block_size` returns the block size in bytes, which is calculated by
    multiplying the `word_per_block` parameter by 4 (assuming each word is 4 bytes).
    """
    
    block_size = word_per_block * 4
    return block_size

def calculate_offset(block_size):
    """
    The function calculates the offset based on the number of words per block.
    
    :param WordPerBlock: It looks like the function `calculate_offset` takes a parameter `WordPerBlock`
    which represents the number of words per block. The function calculates the offset based on this
    input
    :return: The function `calculate_offset` returns the offset calculated based on the block size,
    which is determined by multiplying the `WordPerBlock` parameter by 4 and then taking the base 2
    logarithm of the result.
    """
    
    offset = math.log2(int(block_size*4))
    return offset

def user_input():
    """
    The `user_input` function prompts the user to input cache parameters such as nominal size, words per
    block, and mapping type, handling set associativity if specified.
    :return: The `user_input` function returns a tuple containing the following values in order:
    1. nominal_size
    2. WordPerBlock
    3. Mapping
    4. SetAssociativity
    """
    
    nominal_size = input("Enter the nominal size of the cache and specify the amount of bytes (as in KB,MB): ")
    WordPerBlock = input("Enter the number of words per block(1, 2, 4, 8): ")
    if (math.log2(WordPerBlock) > 3): {
        print("Invalid size 1,2,4,8")
    }
    Mapping = input("Enter the mapping type (Direct, Set): ")
    if Mapping.lower() == "set":
        SetAssociativity = input("Enter the set associativity: ")
        SetAssociativity = int(SetAssociativity)
    else:
        SetAssociativity = None
    return nominal_size, WordPerBlock, Mapping, SetAssociativity

def main():

    # This code snippet is a part of a program written in Python that simulates cache memory
    # operations. Let's break down what the code is doing:
    nominal_size, WordPerBlock, Mapping, SetAssociativity = user_input()
    
    #= user_input()
    nominal_size_list = nominal_size.split()
    nominal_size_value = 0
    if 'KB' in nominal_size_list[1]:
        nominal_size_value = float(nominal_size_list[0]) * 1024
    elif 'MB' in nominal_size_list[1]:
        nominal_size_value = float(nominal_size_list[0]) * 1024 * 1024
   
    #print(f"Nominal Size: {nominal_size_value} bytes")
    #print(f"Words per Block: {WordPerBlock}")
    #print(f"Mapping Type: {Mapping}")
    #print (f"Log base 2 of : {math.log2(nominal_size_value)}")
   
    Offset = calculate_offset(WordPerBlock)
    BlockSize = calculate_block_size(int(WordPerBlock))
    number_of_blocks = calculate_number_of_blocks(nominal_size_value, BlockSize)
    calculate_tag_size_value = calculate_tag_sizeDM(number_of_blocks, calculate_offset(WordPerBlock))
    real_size = calculate_real_size(nominal_size_value, calculate_tag_size_value)
    amount_of_sets = calculate_amount_of_sets(number_of_blocks, SetAssociativity) if SetAssociativity else None
    
    
    # print(f"Offset: {Offset}, bits")
    # print(f"Number of Block Size: {number_of_blocks} blocks")
    # print(f"bits of number of Block Size: {math.log2(number_of_blocks)} bits")
    # print(f"Tag Size: {calculate_tag_size_value} bits")
    # print(f"Real Size of Cache: {real_size} bits")
    # print(f"Real Size of Cache: {real_size/(2**10)} Kbytes")
    
    if SetAssociativity:
        
        calculate_tag_size_value = 32 - math.log2(amount_of_sets) - Offset
        real_size = calculate_real_size(nominal_size_value, calculate_tag_size_value)
        print(f"Set Associativity: {SetAssociativity}")
        print(f"The amount of set in bits is: {math.log2(amount_of_sets)} bits")
        print(f"Offset: {Offset}, bits")
        print(f"Number of Block Size: {number_of_blocks} blocks")
        print(f"bits of number of tag: {calculate_tag_size_value} bits")
        print(f"Real Size of Cache: {real_size} bits")
        print(f"Real Size of Cache: {real_size/(2**10)} Kbytes")
    else :
        print("Direct Mapping:")
        print(f"bits of number of Block Size: {math.log2(number_of_blocks)} bits")
        print(f"Offset: {Offset}, bits")
        print(f"Number of Block Size: {number_of_blocks} blocks")
        print(f"Tag Size: {calculate_tag_size_value} bits")
        print(f"Real Size of Cache: {real_size} bits")
        print(f"Real Size of Cache: {real_size/(2**10)} Kbytes")
        
    print(f"Offset: {calculate_offset(WordPerBlock)} bits")
if __name__ == "__main__":
    main() 