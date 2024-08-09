import gnupg

def decrypt_gpg_file(file_path, password):
    gpg = gnupg.GPG()
    with open(file_path, 'rb') as f:
        status = gpg.decrypt_file(f, passphrase=password)

    if status.ok:
        return status.data
    else:
        raise ValueError(f"Decryption failed: {status.status}")
