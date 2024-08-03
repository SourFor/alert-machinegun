# alert-machinegun

```
python3 alert-machinegun.py -c config.yml
```

## OPENSSL

```sh
openssl aes-256-cbc -a -salt -pbkdf2 -md sha-256 -iter 100000 -in config.yml -out enc-config.yml -k '$uperSecret'
ALERT_MACHINEGUN_ENCRYPTION_KEY='$uperSecret' python3 alert-machinegun.py -c enc-config.yml --openssl
```

## GPG

```sh
gpg --batch --yes --passphrase '$uperSecret' --armor --symmetric --cipher-algo AES256 --output enc-config.yml config.yml
ALERT_MACHINEGUN_ENCRYPTION_KEY='$uperSecret' python3 alert-machinegun.py -c config.yml.asc --gpg
```

### config.yml

```yaml
login: "admin"
password: "admin"
server: "http://localhost:9093"
```