import math;
import random;
import time;

def calculate_amount_of_sets(number_of_blocks, set_associativity):
    """
    T
    """ #TODO fix ugly comments
    amount_of_sets = int(number_of_blocks / set_associativity)
    return amount_of_sets 

def calculate_real_size(nominal_size_value, tag_size, block_size, number_of_blocks):
    """
    T
    """
    real_size = nominal_size_value + (((int(tag_size) )/8)*number_of_blocks)
    return real_size

def calculate_tag_sizeDM(number_of_blocks, offset):
    """
    T
    """
    if number_of_blocks == 0:
        print("Size of nominal size too small: Restarting")
        print("----------------------------------------------------------- \n")
        main()
    else:
        index_bits = int(math.log2(number_of_blocks))
    return 32 - index_bits - int(offset)

def calculate_number_of_blocks(nominal_size_value, block_size):
    """
    T
    """
    nominal_size = int(nominal_size_value)
    block_size = int(block_size)
    return nominal_size // block_size


def calculate_block_size(word_per_block):
    """
    T
    """
    block_size = word_per_block * 4
    return block_size

def calculate_offset(block_size):
    """
    T
    """
    return int(math.log2(block_size))

def user_input():
    """
    T
    """
    nominal_size = input("Enter the nominal size of the cache ([Most Sig Fig] [B,KB,MB,TB]): ")
    WordPerBlock = input("Enter the number of words per block (1, 2, 4, 8): ")

    if WordPerBlock not in ["1", "2", "4", "8"]:
        print("Invalid input: Restarting")
        print("----------------------------------------------------------- \n")
        main()

    Mapping = input("Enter the mapping type (Direct, Set): ").lower()

    if Mapping.lower() == "set":
        SetAssociativity = input("Enter the set associativity: ")
        SetAssociativity = int(SetAssociativity)

    elif Mapping.lower() == "direct":
        SetAssociativity = None

    else:
        print("Invalid mapping type: Restarting")
        print("----------------------------------------------------------- \n")
        main()

    return nominal_size, WordPerBlock, Mapping, SetAssociativity

def access_cache(word_address, words_per_block, mapping, num_sets, cache, set_associativity):
    """
    T
    """
    block_address = word_address // words_per_block
    index = block_address % num_sets
    tag = block_address // num_sets
    
    if mapping == "direct":
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
                cache[index].pop(set_associativity) #Get rid of most recently used
            cache[index].append(tag) #Add the new tag
            return "Miss"
        
def clear_cache(mapping,cache):
    """
    T
    """
    if mapping == "direct":
        cache.clear()
    else:
        for i in cache:
            cache[i] = []
    
def inaddr_loop(rand_in, number_of_blocks, mapping, cache, num_sets, words_per_block, SetAssociativity, Display):
    misses = 0
    hits = 0
    
    input_addr = "LALALA"
    while (input_addr != "X"):

        if rand_in == "no in":
            if Display == 1:
                input_addr = input("Enter a word address (enter X to exit, clear to clear): ")
            else:
                input_addr = input("")
        else:
            input_addr = rand_in

        if input_addr == "X":
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
            if Display == 1:
                print(f"{input_addr} was a hit!")
                print(f"Total Hits: {hits}")
                print(f"Total Misses: {misses} \n")
        if accuracy == "Miss":
            misses+=1
            if Display == 1:
                print(f"{input_addr} was a miss!")
                print(f"Total Hits: {hits}")
                print(f"Total Misses: {misses} \n")
        
        if rand_in != "no in":
            break

    return (misses, hits)

def random_gen_loop(number_of_blocks, mapping, cache, num_sets, words_per_block, SetAssociativity):
    misses = 0
    hits = 0
    rander_num = random.randint(1, number_of_blocks)
    rand_num = random.randint(1, 10*rander_num)
    i = 0

    while (i <= rand_num):
        new_addr = random.randint(1,number_of_blocks)
        new_addr = str(new_addr)
        misses_temp, hits_temp = inaddr_loop(new_addr, number_of_blocks, mapping, cache, num_sets, words_per_block, SetAssociativity, Display = 0)
        misses += misses_temp
        hits += hits_temp
        i += 1
        
    return misses,hits


def main():

    nominal_size, words_per_block, mapping, SetAssociativity = user_input()

    nominal_size_list = nominal_size.split()
    nominal_size_value = 0
    hits = 0 
    misses = 0
    
    if "b" == (str(nominal_size_list[1])).lower():
        if int(nominal_size_list[0]) < 3:
            print("Size of nominal size too small: Restarting")
            print("----------------------------------------------------------- \n")
            main()
        else:
            nominal_size_value = float(nominal_size_list[0])
    elif "kb" == (str(nominal_size_list[1])).lower():
        nominal_size_value = float(nominal_size_list[0]) * (2**10)
    elif "mb" == (str(nominal_size_list[1])).lower():
        nominal_size_value = float(nominal_size_list[0]) * (2**20)
    elif "tb" == (str(nominal_size_list[1])).lower():
        nominal_size_value = float(nominal_size_list[0]) * (2**30)
    else:
        print("Invalid size: Restarting")
        print("----------------------------------------------------------- \n")
        main()

    words_per_block = int(words_per_block)
    BlockSize = calculate_block_size(words_per_block)
    Offset = calculate_offset(BlockSize)
    number_of_blocks = calculate_number_of_blocks(nominal_size_value, BlockSize)

    if SetAssociativity:
        if number_of_blocks % SetAssociativity != 0:
            print("Invalid configuration: associativity must evenly divide number of blocks: Restarting")
            print("----------------------------------------------------------- \n")
            main()
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
        print(f"Tag Size: 1 valid bit + {int(tag_size)-1} bits")
        print(f"Index Size: {int(math.log2(amount_of_sets))} bits")
        print(f"Offset: {Offset} bits")
        print(f"Real Size of Cache: {(real_size / ((10**(3)))):.3f} Kbytes \n")
    else:
        print("-----------------------------------------------------------")
        print("Direct Mapping:")
        print(f"Number of Blocks in Cache: {number_of_blocks} blocks")
        print(f"Tag Size: 1 valid bit + {int(tag_size)-1} bits")
        print(f"Index bits: {int(math.log2(number_of_blocks))} bits")
        print(f"Offset: {Offset} bits")
        print(f"Real Size of Cache: {(real_size / (10**(3))):.3f} Kbytes \n")

    num_sets = amount_of_sets if SetAssociativity else number_of_blocks

    random_gen = input("Enter 1 for manual, 0 for random generated: ")
    if int(random_gen) == 1: 
        rand_in = "no in"
        misses,hits = inaddr_loop(rand_in, number_of_blocks, mapping, cache, num_sets, words_per_block, SetAssociativity, Display = 1)
    else:
        misses,hits = random_gen_loop(number_of_blocks, mapping, cache, num_sets, words_per_block, SetAssociativity)
    
    print(f"Total Hits: {hits}")
    print(f"Total Misses: {misses}")
    if (hits+misses) != 0:
        print(f"Hit Rate: {(hits / (hits + misses)) * 100:.1f}%")
        print(f"Miss Rate: {(misses / (hits + misses)) * 100:.1f}% \n")
    else: 
        print("Hit Rate: 0%")
        print("Miss Rate: 100% \n")

    reset_in = input("Enter 1 to restart, 0 to end calculation: ")
    if reset_in == '1':
        print("\n")
        print("----------------------------------------------------------- \n")
        clear_cache(mapping,cache)
        main()
    else:
        print("\n")
        reset_in == 0
        print("Ending calculation...")
        time.sleep(1.2)
        print("Disabling L2 Cache of CPU 1")
        time.sleep(0.8)
        print("Ending task 'main'")
        time.sleep(0.9)
        print("Installing Minecraft")
        time.sleep(1.5)
        print("Uninstalling Minecraft")
        time.sleep(1.2)
        print("End \n")

if __name__ == "__main__":
    main() 