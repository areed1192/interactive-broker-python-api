
import ssl
# cert_pem = ssl.get_server_certificate(addr=('localhost',5000))
# cert_der = ssl.PEM_cert_to_DER_cert(cert_pem)

# with open('alex\certs_new.pem', 'w') as f: f.write(cert_pem)

url = "https://localhost:5000/v1/portal/iserver/accounts"
import requests
import subprocess

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.99 Safari/537.36'}

# try:
    # As long as the certificates in the certs directory are in the OS's certificate store, `verify=True` is fine.
print(requests.get(url, headers=headers, verify=True, cert='alex'))
# except requests.exceptions.SSLError:
#     subprocess.run('openssl rehash -compat -v "C:/Users/Alex/OneDrive/Desktop"', shell=True, check=True)
#     print(requests.get(url, verify="my_certs_dir"))