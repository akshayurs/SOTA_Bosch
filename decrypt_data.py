import rsa

def decrypt_file(file_name, private_key_file):

    with open(file_name, "rb") as input_file:
        encrypted_data = input_file.read()

    with open(private_key_file, "rb") as private_key_file:
        private_key = rsa.PrivateKey.load_pkcs1(private_key_file.read())

    decrypted_data = rsa.decrypt(encrypted_data, private_key)

    decrypted_file_name = file_name + ".decrypted"
    with open(decrypted_file_name, "wb") as output_file:
        output_file.write(decrypted_data)

    return decrypted_file_name


file_name = "software_file.txt.encrypted"
private_key_file = "private_key_car.pem"

decrypted_file_name = decrypt_file(file_name, private_key_file)

print("The decrypted file has been saved as {}.".format(decrypted_file_name))
