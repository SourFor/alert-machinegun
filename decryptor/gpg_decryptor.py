import gnupg

def decrypt_gpg_file(file_path, password):
    gpg = gnupg.GPG()
    with open(file_path, 'rb') as f:
        status = gpg.decrypt_file(f, passphrase=password, output='decrypted_config.yml')

    if status.ok:
        with open('decrypted_config.yml', 'r') as f:
            decrypted_data = f.read()
        return decrypted_data
    else:
        raise ValueError(f"Decryption failed: {status.stderr}")
