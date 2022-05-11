import hashlib
import binascii
import random

def get_digest(password):
  encoded_password = password.encode('utf-8')
  hasher = hashlib.sha256(encoded_password)
  digest = hasher.digest()
  digest_as_hex = binascii.hexlify(digest)
  digest_as_hex_string = digest_as_hex.decode('utf-8')
  return digest_as_hex_string

def check_digest(expected, digest):
  if expected == digest:
    return True
  else:
    return False

def debug(password_options):
  for option in password_options:
    word_digest = get_digest(option)
    if check_digest('182072537ada59e4d6b18034a80302ebae935f66adbdf0f271d3d36309c2d481', word_digest) == True:
      print(f"Jeff's password: {option}")

def print_results(found_passwords, accounts):
  if len(found_passwords) == len(accounts):
    print("All passwords cracked!")
    print(f"Successfully cracked {len(found_passwords)} passwords")
  else:
    print("Failed to crack all passwords")
    print(f"Successfully cracked {len(found_passwords)} passwords")
  return None

def create_random_num_list(num_words):
  random_num_list = []
  for i in range(0,2000):
    j = random.randint(0,num_words)
    while j in random_num_list:
      j = random.randint(0,num_words)
    random_num_list.append(j)
  return random_num_list

accounts = [line.split(':')[0:2] for line in open('passwords2.txt')]
account_dict = {}
for account in accounts:
  account_dict[account[1]] = account[0]

words = [line.strip().lower() for line in open('words.txt')]
with open("sample_words.txt", 'w') as f:
    for word in words:
        if word[0] == 'c':
            f.write(word + '\n')
sample_words = [line.strip().lower() for line in open('sample_words.txt')]

found_passwords = []

output_file = open("cracked222.txt", "x")

hash_numbers = []

num_words_as_index = len(words)-1

random_num_list = create_random_num_list(num_words_as_index)

debug(words)

num_hashes = 0
for word in words:
  num_hashes += 1
  word_digest = get_digest(word)
  for key, value in account_dict.items():
    if check_digest(value, word_digest) == True:
      output_file.write(f"{key}:{word}\n")
      found_passwords.append(f"{key}:{word}")
hash_numbers.append(num_hashes)

num_hashes = 0
for word1 in sample_words:
  for word2 in words:
    num_hashes += 1
    password = word1 + word2
    word_digest = get_digest(password)
    if word_digest in account_dict:
      output_file.write(f"{account_dict.get(word_digest)}:{password}\n")
      found_passwords.append(f"{account_dict.get(word_digest)}:{password}")
      print(f"Found password for {account_dict.get(word_digest)}:{password}")
  hash_numbers.append(num_hashes)


for key, value in account_dict.items():
  password_sections = value.split('$')
  num_hashes = 0
  for word in words:
    num_hashes += 1
    password = password_sections[2] + word
    word_digest = get_digest(password)
    if check_digest(password_sections[3], word_digest) == True:
      output_file.write(f"{key}:{word}\n")
      found_passwords.append(f"{key}:{word}")
      break
  hash_numbers.append(num_hashes)


print_results(found_passwords, accounts)
cracks_per_hash = len(found_passwords)/sum(hash_numbers)
total_hashes = sum(hash_numbers)
print(f"Total number of hashes performed: {total_hashes}")
print(f"Average number of password cracks per hash calculated: {cracks_per_hash}")
