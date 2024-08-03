import argparse
import json
import requests
import yaml
import os
from datetime import datetime, timezone 

from decryptor import decrypt_openssl_file, decrypt_gpg_file



parser = argparse.ArgumentParser()
parser.add_argument("-c", "--config", default="config.yml", help="Path to the file with login and password")
enc_mode = parser.add_mutually_exclusive_group()
enc_mode.add_argument('--openssl', action='store_true', help="Use openssl decryptor")
enc_mode.add_argument('--gpg', action='store_true', help="Use gpg decryptor")
args = parser.parse_args()

try:
    key = os.getenv('ALERT_MACHINEGUN_ENCRYPTION_KEY')
except:
    print("ALERT_MACHINEGUN_ENCRYPTION_KEY")

# Расшифровка файла, зашифрованного с помощью OpenSSL
if args.openssl:
    try:
        config = decrypt_openssl_file(args.config, key)
        # print("Decrypted content from OpenSSL:")
        # print(config)
        config = yaml.safe_load(config)
    except Exception as e:
        print(f"An error occurred with OpenSSL decryption: {e}")
# Расшифровка файла, зашифрованного с помощью GPG
elif args.gpg:
    try:
        config = decrypt_gpg_file(args.config, key)
        # print("Decrypted content from GPG:")
        # print(config)
        config = yaml.safe_load(config)
    except Exception as e:
        print(f"An error occurred with GPG decryption: {e}")
else:
    with open(args.config, "r") as file:
        config = yaml.safe_load(file)

login = config["login"]
password = config["password"]
server = config["server"] + '/api/v2/alerts'

local_time = datetime.now(timezone.utc).astimezone()
local_time.isoformat()

headers = {
 "Content-Type": "application/json"
}

alert = {
    "labels": {
        "alertname": "Scheduled alert"
    },
    "annotations": {
        "info": "This alert was sent by the verification tool"
    },
    "startsAt": local_time.isoformat(),
    "generatorURL": "localhost:80"
}
data = []
data.append(alert)
print(json.dumps(data))
response = requests.post(server, data=json.dumps(data), headers=headers, auth=(login, password))
print(response.status_code)
