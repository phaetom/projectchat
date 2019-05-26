from virgil_crypto import VirgilCrypto

crypto = VirgilCrypto()
key_pair = crypto.generate_keys()
print(key_pair)