import rsa


def generate_key():
    key = rsa.newkeys(2048)
    private_key = key[1]
    public_key = key[0]
    # convert to hex and return
    return private_key.save_pkcs1().hex(), public_key.save_pkcs1().hex()
