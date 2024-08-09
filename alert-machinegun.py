import argparse
import json
import requests
import yaml
import os
from datetime import datetime, timezone 
import logging

from decryptor import decrypt_openssl_file, decrypt_gpg_file

# create logger
logger = logging.getLogger('alert-machinegun')
logger.setLevel(logging.DEBUG)
# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# create console handler
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)

# create file handler
fh = logging.FileHandler('/var/log/alert-machingun.log')
fh.setFormatter(formatter)
logger.addHandler(fh)

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--config", default="config.yml", help="Path to the configuration file. Default: config.yml")
parser.add_argument("-d", "--data", default="data", help="Alerts folder path with json files. Default: data")
enc_mode = parser.add_mutually_exclusive_group()
enc_mode.add_argument('--openssl', action='store_true', help="Use openssl decryptor")
enc_mode.add_argument('--gpg', action='store_true', help="Use gpg decryptor")
args = parser.parse_args()

def get_key():
    key = os.getenv('ALERT_MACHINEGUN_ENCRYPTION_KEY')
    if not key:
        raise ValueError(f"ALERT_MACHINEGUN_ENCRYPTION_KEY environment variable is not defined")
    return key

# Get config and decrypt it
def get_config(path):
    if args.openssl:
        try:
            config = decrypt_openssl_file(path, get_key())
            # logger.debug("Decrypted content from OpenSSL:")
            # logger.debug(config)
            config = yaml.safe_load(config)
        except Exception as e:
            logger.critical(f"An error occurred with OpenSSL decryption: {e}")
    elif args.gpg:
        try:
            config = decrypt_gpg_file(path, get_key())
            # logger.debug("Decrypted content from GPG:")
            # logger.debug(config)
            config = yaml.safe_load(config)
        except Exception as e:
            logger.critical(f"An error occurred with GPG decryption: {e}")
    else:
        with open(path, "r") as file:
            config = yaml.safe_load(file)

    return config

def get_files(path):
    alert_files = []

    for (dirpath, dirnames, filenames) in os.walk(path):
        for f in filenames:
            if f.split('.')[-1] == "json":
                alert_files.append(os.path.join(path,f))

    return alert_files

def prepare_data(files):
    data = []
    for file in files:
        with open(file, 'r') as f:
            alert = json.load(f)
            data.append(alert)
    return data

def push(data, config):
    local_time = datetime.now(timezone.utc).astimezone()
    local_time.isoformat()
    headers = {
        "Content-Type": "application/json"
    }
    server = config["server"] + '/api/v2/alerts'
    try:
        response = requests.post(server, data=json.dumps(data), headers=headers, auth=(config["login"], config["password"]))
        logger.info("DATA: {} STATUS: {}".format(json.dumps(data), response.status_code))
    except Exception as e:
        logger.error(f"An error occurred when requesting: {e}\nDATA: {json.dumps(data)}")

def run():
    config = get_config(args.config)

    push(prepare_data(get_files(args.data)), config)

if __name__ == '__main__':
    run()