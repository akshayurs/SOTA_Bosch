import rsa; 
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import  padding

def decrypt():
    from js import my_private_key
    file_data = Element("encrypted-data").element.value
    file_data = bytes.fromhex(file_data)
    hex_bytes = bytes.fromhex(my_private_key)
    private_key_byte = hex_bytes.decode('utf-8')
    private_key = rsa.PrivateKey.load_pkcs1(private_key_byte)
    decrypted_data = rsa.decrypt(file_data, private_key)
    Element("decrypted-data").element.value = decrypted_data.decode('utf-8')


def send_soft_py():
    from js import my_public_key, my_private_key,socket,send_soft_js,alert
    software = Element("software_inp").element.value
    if(software==""):
        alert("Enter Software")
    software = software.encode('utf-8')
    my_private_key_byte = bytes.fromhex(my_private_key)
    private_key = serialization.load_pem_private_key(
            my_private_key_byte,
            password=None
        )
    
    signature = private_key.sign(
        software,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    send_soft_js(software.decode('utf-8'),signature.hex())
    

def verify():
    from js import signature,users,testerpublickey,alert
    signature = bytes.fromhex(signature)
    public_key = bytes.fromhex(testerpublickey)
    public_key = serialization.load_pem_public_key(
            public_key
        )
    file_data = Element("decrypted-data").element.value
    if(file_data==""):
        alert("Decrypt Data first")
    file_data = file_data.encode('utf-8')
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
        Element("verify-status").element.innerHTML = "Verified"
    except:
        Element("verify-status").element.innerHTML = "Not Verified"