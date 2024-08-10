# alert-machinegun

```sh
usage: alert-machinegun [-h] [-c CONFIG] [-d DATA] [--openssl | --gpg]

options:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Path to the configuration file. Default: config.yml
  -d DATA, --data DATA  Alerts folder path with json files. Default: data
  --openssl             Use openssl decryptor
  --gpg                 Use gpg decryptor

```

## PREPARE

### build

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pyinstaller --onefile alert-machinegun.py
```

### config.yml

```yaml
login: "admin"
password: "admin"
server: "http://localhost:9093"
```

## OPENSSL

```sh
openssl aes-256-cbc -a -salt -pbkdf2 -md sha-256 -iter 100000 -in config.yml -out enc-config.yml -k '$uperSecret'
ALERT_MACHINEGUN_ENCRYPTION_KEY='$uperSecret' python3 alert-machinegun.py -c enc-config.yml --openssl
```

## GPG

```sh
gpg --batch --yes --passphrase '$uperSecret' --armor --symmetric --cipher-algo AES256 --output enc-config.yml config.yml
ALERT_MACHINEGUN_ENCRYPTION_KEY='$uperSecret' python3 alert-machinegun.py -c enc-config.yml --gpg
```

## DOCKER

### build
```sh
sudo docker build -t sourfor/alert-machinegun:0.1.0 .
```

### run 

```sh
sudo docker run --rm \
--net=host \
--mount type=bind,source="$(pwd)"/config.yml,target=/opt/alert-machinegun/config.yml \
--mount type=bind,source="$(pwd)"/data,target=/opt/alert-machinegun/data \
--name alert-machinegun \
sourfor/alert-machinegun:0.1.0
```

```sh
sudo docker run --rm \
--net=host \
--mount type=bind,source="$(pwd)"/enc-config.yml,target=/opt/alert-machinegun/config.yml \
--mount type=bind,source="$(pwd)"/data,target=/opt/alert-machinegun/data \
--name alert-machinegun \
--env-file /etc/alert-machinegun/env \
sourfor/alert-machinegun:0.1.0 \
/opt/alert-machinegun/alert-machinegun --gpg
```

## Ansible role

[Ansible role](https://github.com/SourFor/ansible-role-alert-machinegun)