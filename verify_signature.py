from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
import os
import sys


def verify_signature(file_path, signature_path, public_key_path):
    with open(public_key_path, "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read()
        )

    with open(file_path, "rb") as file:
        file_data = file.read()

    with open(signature_path, "rb") as sig_file:
        signature = sig_file.read()

    try:
        public_key.verify(
            signature,
            file_data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except:
        return False


file_path = "software_file.txt"
signature_path = "signature.txt"
public_key_path = "public_key_cloud.pem"

if not os.path.isfile(file_path):
    print("File path {} does not exist. Exiting...".format(file_path))
    sys.exit()

if not os.path.isfile(public_key_path):
    print("Generate keys first, run generate_keys.py")
    sys.exit()

if not os.path.isfile(signature_path):
    print("File path {} does not exist. Exiting...".format(signature_path))
    sys.exit()

is_valid = verify_signature(file_path, signature_path, public_key_path)

print(is_valid)
