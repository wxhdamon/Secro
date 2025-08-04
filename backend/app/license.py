#/backend/app/license.py
import json
import base64
import rsa
import os
from datetime import datetime

LICENSE_PATH = "license.lic"
PUBLIC_KEY_PATH = "public.pem"

def check_license():
    """
    验证 license 文件是否存在、合法、未过期。
    """
    if not os.path.exists(LICENSE_PATH):
        print("❌ License file not found.")
        return False

    try:
        with open(LICENSE_PATH, "r") as f:
            data = json.load(f)

        signature = base64.b64decode(data["signature"])
        payload = json.dumps({k: data[k] for k in data if k != "signature"}, sort_keys=True).encode("utf-8")

        with open(PUBLIC_KEY_PATH, "rb") as pub_file:
            pub_key = rsa.PublicKey.load_pkcs1_openssl_pem(pub_file.read())

        rsa.verify(payload, signature, pub_key)

        expires = datetime.strptime(data["expires"], "%Y-%m-%d")
        if datetime.now() > expires:
            print("❌ License expired.")
            return False

        return True
    except Exception as e:
        print(f"❌ License check failed: {e}")
        return False

def get_license_info():
    """
    返回解析后的 license 信息（不含 signature）。
    """
    if not os.path.exists(LICENSE_PATH):
        return {}

    try:
        with open(LICENSE_PATH, "r") as f:
            data = json.load(f)
        return {k: v for k, v in data.items() if k != "signature"}
    except Exception:
        return {}
