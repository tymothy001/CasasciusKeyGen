import os
import multiprocessing
from bitcoin import *
from multiprocessing import Pool, Manager
from tqdm import tqdm

def print_logo():
    logo = """
   ______                           _
  / ____/___ __________ ___________(_)_  _______
 / /   / __ `/ ___/ __ `/ ___/ ___/ / / / / ___/  MINI PREVATE
/ /___/ /_/ (__  ) /_/ (__  ) /__/ / /_/ (__  )   KEY SCANER V.O1
\____/\__,_/____/\__,_/____/\___/_/\__,_/____/    2024

====================================================================================

 usage:  python3 miniCacasius.py

 basis:  https://casascius.uberbills.com

 combination: 10,764,351,351,569,111,513,009,094,806,216,900,608

 donate: 1xxxxe1QUbmLATePu2AKBCm2jAfVtx2jy


====================================================================================
    """
    print(logo)

if __name__ == '__main__':
    print_logo()
found_patterns = 0

def generate_mini_private_key():
    """Generates a valid mini private key."""
    valid = False
    key = ''
    while not valid:
        key = 'S' + random_key()[:21]
        full_key = sha256(key)
        if sha256(key + '?')[0] == '0':
            valid = True
    return key, full_key

def check_address_pattern(key_info, patterns):
    """Checks if the generated address matches any pattern in the list."""
    mini_key, full_key = key_info
    address = privtoaddr(full_key)
    for pattern in patterns:
        if address.startswith(pattern):
            return mini_key, address
    return None

def load_patterns(filename='pattern.txt'):
    """Load address patterns from a text file."""
    with open(filename, 'r') as file:
        patterns = [line.strip() for line in file if line.strip()]
    return patterns

def process_keys(patterns, counter, lock):
    """Generate keys and check against patterns."""
    key_info = generate_mini_private_key()
    result = check_address_pattern(key_info, patterns)
    if result:
        mini_key, address = result
        with open('foundMini.txt', 'a') as file:
            file.write(f'Mini Key: {mini_key}, Address: {address}\n')
        with lock:
            counter.value += 1
        return f'Found matching address: {address}'
    return None

def process_task(args):
    """Wrapper function to unpack arguments for pool."""
    patterns, counter, lock = args
    return process_keys(patterns, counter, lock)

if __name__ == '__main__':
    patterns = load_patterns()
    pool_size = multiprocessing.cpu_count()

    manager = Manager()
    counter = manager.Value('i', 0)
    lock = manager.Lock()

    total_keys = 1000  # Adjust the number of keys to generate per iteration

    while True:  # Infinite loop for continuous generation
        with Pool(processes=pool_size) as pool:
            with tqdm(total=total_keys) as pbar:
                for _ in pool.imap_unordered(process_task, [(patterns, counter, lock)] * total_keys):
                    pbar.update()

        print("Iteration complete. Check 'foundMini.txt' for results.")
        print(f"Total patterns found so far: {counter.value}")
