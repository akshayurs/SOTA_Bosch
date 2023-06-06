from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
import os
import sys


def calculate_signature(file_path, private_key_path, signature_path):
    with open(private_key_path, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None
        )

    with open(file_path, "rb") as file:
        file_data = file.read()

    signature = private_key.sign(
        file_data,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    print("Signature:")
    print(signature.hex())

    with open(signature_path, "wb") as sig_file:
        sig_file.write(signature)

    print("Signature saved to", signature_path)


file_path = "software_file.txt"
private_key_path = "private_key_cloud.pem"
signature_path = "signature.txt"

if not os.path.isfile(file_path):
    print("File path {} does not exist. Exiting...".format(file_path))
    sys.exit()

if not os.path.isfile(private_key_path):
    print("Generate keys first, run generate_keys.py")
    sys.exit()

calculate_signature(file_path, private_key_path, signature_path)
