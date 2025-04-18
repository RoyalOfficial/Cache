import math;
def calculate_amount_of_sets(number_of_blocks, set_associativity):
    """
    This function calculates the amount of sets based on the number of blocks and set associativity.
    
    :param number_of_blocks: The `number_of_blocks` parameter represents the total number of blocks
    in a cache or memory system
    :param set_associativity: The `set_associativity` parameter represents the number of blocks that can
    be mapped to a single set in a cache memory system. It is used to calculate the number of sets
    in the cache
    :return: the amount of sets in the cache.
    """
    amount_of_sets = int(number_of_blocks / set_associativity)
    return amount_of_sets 

def calculate_real_size(nominal_size_value, tag_size, block_size, number_of_blocks):
    """
    This function calculates the real size based on a nominal size value and a tag size.
    
    :param nominal_size_value: The `nominal_size_value` parameter represents the base value of the size.
    It is the starting point for calculating the real size
    :param tag_size: Tag size is the size of the tag in bits
    :return: The function `calculate_real_size` returns the calculated real size value based on the
    formula provided in the function.
    """
    data_bits = block_size * 8
    bits_per_block = data_bits + int(tag_size) + 1
    total_bits = bits_per_block * number_of_blocks
    return total_bits
    #real_size = nominal_size_value + ((int(tag_size) )/8)* (2**16)
    #return real_size
    #TODO fix this

def calculate_tag_sizeDM(number_of_blocks, offset):
    """
    This function calculates the tag size based on the number of blocks and offset.
    :param number_of_blocks: The `number_of_blocks` parameter represents the total number of blocks
    in a cache or memory system
    :param offset: The `offset` parameter in the `calculate_tag_size` function represents the number of bits
    used for the offset within a block. It is used to calculate the tag size by determining how many bits
    are needed to represent the number of blocks
    :return: the tag size in bits.
    """
    index_bits = int(math.log2(number_of_blocks))
    return 32 - index_bits - int(offset)
    #tag_size = (32 - math.log2(int(number_of_blocks)) - int(offset))
    #return tag_size

def calculate_number_of_blocks(nominal_size_value, block_size):
    """
    This function calculates the number of blocks that can fit within a given nominal size based on a
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
    This function calculates the block size based on the number of words per block.
    
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
    This function calculates the offset based on the number of words per block.
    
    :param WordPerBlock: It looks like the function `calculate_offset` takes a parameter `WordPerBlock`
    which represents the number of words per block. The function calculates the offset based on this
    input
    :return: The function `calculate_offset` returns the offset calculated based on the block size,
    which is determined by multiplying the `WordPerBlock` parameter by 4 and then taking the base 2
    logarithm of the result.
    """
    return int(math.log2(block_size))
    #offset = math.log2(int(block_size)*4)
    #return offset

def user_input():
    """
    This function prompts the user to input cache parameters such as nominal size, words per
    block, and mapping type, handling set associativity if specified.
    :return: The `user_input` function returns a tuple containing the following values in order:
    1. nominal_size
    2. WordPerBlock
    3. Mapping
    4. SetAssociativity
    """
    
    nominal_size = input("Enter the nominal size of the cache and specify the amount of bytes (as in KB,MB): ")
    WordPerBlock = input("Enter the number of words per block(1, 2, 4, 8): ")
    if WordPerBlock not in ["1", "2", "4", "8"]:
        print("Invalid input")
        exit(1)
    Mapping = input("Enter the mapping type (Direct, Set): ").lower()
    if Mapping.lower() == "set":
        SetAssociativity = input("Enter the set associativity: ")
        SetAssociativity = int(SetAssociativity)
    else:
        SetAssociativity = None
    return nominal_size, WordPerBlock, Mapping, SetAssociativity

def access_cache(word_address, words_per_block, mapping, num_sets, cache, set_associativity):
    """
    This function is responsible for accessing the cache and depends on direct mapping
    """
    #TODO fix the bad set ass thing
    block_address = word_address // words_per_block
    index = block_address % num_sets
    tag = block_address // num_sets
    
    if mapping == "direct" or "d":
        if index in cache and cache[index] == tag:
            return "Hit"
        else:
            cache[index] = tag
            return "Miss"
        
    if mapping == "set":
        # Grabs the set (list of all the tags)
        tag_list = cache[index]
        if tag in cache[index]:
            #LRU(leasy recently used) move the most recently used to the end
            tag_list.remove(tag)
            tag_list.append(tag)
            return "Hit"
        else:
            if (len(tag_list) >= set_associativity):
                cache[index].pop(0) #Get rid of most recently used
            cache[index].append(tag) #Add the new tag
            return "Miss"
        
def clear_cache(mapping,cache):
    """
    Takes in a cache and clears it
    :param Mapping: Type of mapping which depends on how cache is cleared
    :param cache: cache to clear
    """
    if mapping == "direct":
        cache.clear()
    else:
        for i in cache:
            cache[i] = []
    
def inaddr_loop(number_of_blocks, mapping, cache, num_sets, words_per_block, SetAssociativity):
    misses = 0
    hits = 0

    input_addr = "LALALA"
    while (input_addr != "0"):
        input_addr = input("Enter a word address (enter 0 to exit, clear to clear):")
        if input_addr == "0":
            continue
        if (input_addr == "clear"):
            clear_cache(mapping, cache)
            print("Cache cleared! \n")
            misses = 0
            hits = 0
            continue
        if not input_addr.isdigit():
            print("Invalid input enter numerical values only \n")
            continue
        if int(input_addr) > int(number_of_blocks):
            print("Input out of range \n")
            continue
        accuracy = access_cache(int(input_addr), int(words_per_block), mapping, int(num_sets), cache, SetAssociativity)
        if accuracy == "Hit":
            hits+=1
            print(f"{input_addr} was a hit!")
            print(f"Total Hits: {hits}")
            print(f"Total Misses: {misses} \n")
        if accuracy == "Miss":
            misses+=1
            print(f"{input_addr} was a miss!")
            print(f"Total Hits: {hits}")
            print(f"Total Misses: {misses} \n")
    return (misses, hits)

def main():

    nominal_size, words_per_block, mapping, SetAssociativity = user_input()
    # Convert nominal size to bytes
    nominal_size_list = nominal_size.split()
    nominal_size_value = 0
    hits = 0 
    misses = 0

    if 'KB' in nominal_size_list[1]:
        nominal_size_value = float(nominal_size_list[0]) * 1024
    elif 'MB' in nominal_size_list[1]:
        nominal_size_value = float(nominal_size_list[0]) * 1024 * 1024

    words_per_block = int(words_per_block)
    BlockSize = calculate_block_size(words_per_block)
    Offset = calculate_offset(BlockSize)
    number_of_blocks = calculate_number_of_blocks(nominal_size_value, BlockSize)

    if SetAssociativity:
        if number_of_blocks % SetAssociativity != 0:
            print("Invalid configuration: associativity must evenly divide number of blocks")
            exit(1)
        amount_of_sets = calculate_amount_of_sets(number_of_blocks, SetAssociativity)
        tag_size = 32 - int(math.log2(amount_of_sets)) - Offset
        cache = {i: [] for i in range(amount_of_sets)}
    else:
        cache = {}
        tag_size = calculate_tag_sizeDM(number_of_blocks, Offset)

    real_size = calculate_real_size(nominal_size_value, tag_size, BlockSize, number_of_blocks)

    if SetAssociativity:
        print("-----------------------------------------------------------")
        print(f"Set Associativity: {SetAssociativity}")
        print(f"Number of Blocks in Cache: {number_of_blocks} blocks")
        print(f"The amount of sets: {amount_of_sets}")
        print(f"Tag Size: {int(tag_size)} bits")
        print(f"Index Size: {int(math.log2(amount_of_sets))} bits")
        print(f"Offset: {Offset} bits")
        print(f"Real Size of Cache: {real_size / (2**13)} Kbytes \n")
    else:
        print("-----------------------------------------------------------")
        print("Direct Mapping:")
        print(f"Number of Blocks in Cache: {number_of_blocks} blocks")
        print(f"Tag Size: {int(tag_size)} bits")
        print(f"Index bits: {int(math.log2(number_of_blocks))} bits")
        print(f"Offset: {Offset} bits")
        print(f"Real Size of Cache: {(real_size / (2**13)):.01f} Kbytes \n")

    num_sets = amount_of_sets if SetAssociativity else number_of_blocks

    misses,hits = inaddr_loop(number_of_blocks, mapping, cache, num_sets, words_per_block, SetAssociativity)
    
    print(f"Total Hits: {hits}")
    print(f"Total Misses: {misses}")
    print(f"Hit Rate: {(hits / (hits + misses)) * 100:.1f}%")
    print(f"Miss Rate: {(misses / (hits + misses)) * 100:.1f}% \n")
    
if __name__ == "__main__":
    main() 