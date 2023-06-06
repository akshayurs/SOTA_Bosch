import rsa

key = rsa.newkeys(2048)

private_key = key[1]
public_key = key[0]

name = input("Enter file suffix: ")

with open('private_key_'+name+'.pem', 'wb') as f:
    f.write(private_key.save_pkcs1())

with open('public_key_'+name+'.pem', 'wb') as f:
    f.write(public_key.save_pkcs1())
