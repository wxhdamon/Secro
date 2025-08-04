#/frontend/scripts/license_generator.py
import json
import base64
import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

def load_private_key(pem_path):
    with open(pem_path, "rb") as f:
        pem_data = f.read()

    try:
        return rsa.PrivateKey.load_pkcs1(pem_data)
    except ValueError:
        private_key = serialization.load_pem_private_key(
            pem_data,
            password=None,
            backend=default_backend()
        )
        numbers = private_key.private_numbers()
        return rsa.PrivateKey(
            n=numbers.public_numbers.n,
            e=numbers.public_numbers.e,
            d=numbers.d,
            p=numbers.p,
            q=numbers.q
        )

def generate_license():
    priv_key = load_private_key("private.pem")

    data = {
        "customer": "Acme Corp",
        "mac": "00:1A:2B:3C:4D:5E",
        "expires": "2026-01-01",
        "features": ["scanner", "parser"]
    }

    raw_data = json.dumps(data, sort_keys=True).encode('utf-8')
    signature = rsa.sign(raw_data, priv_key, "SHA-256")
    data["signature"] = base64.b64encode(signature).decode('utf-8')

    with open("license.lic", "w") as f:
        json.dump(data, f, indent=4)

generate_license()
