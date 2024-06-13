import os
import datetime
from cryptography.fernet import Fernet
from .models import EncryptedFile
from datetime import datetime
import shutil
from django.utils import timezone

# Generate a key and save it to a file
key = Fernet.generate_key()
with open("key.key", "wb") as key_file:
    key_file.write(key)

# Load the key from the file and instantiate a Fernet instance
with open("key.key", "rb") as key_file:
    key = key_file.read()
cipher_suite = Fernet(key)

def encrypt_files():
    log_folder = 'log_folder'
    archive_folder = 'archive_folder'  # replace with your archive folder path
    today = datetime.today().date()

    for filename in os.listdir(log_folder):
        if filename.endswith(".log") and not filename.startswith(f'folder_access_{today}'):
            with open(os.path.join(log_folder, filename), 'rb') as f:
                # Read the file
                file_data = f.read()

                # Encrypt the file
                encrypted_data = cipher_suite.encrypt(file_data)

            # Store the encrypted data in the database
            EncryptedFile.objects.update_or_create(
                filename=filename,
                defaults={'data': encrypted_data,'saved_month': datetime.now()},
            )

            # Move the original file to the archive folder
            shutil.move(os.path.join(log_folder, filename), os.path.join(archive_folder, filename))

def decrypt_files():
    log_folder = 'log_folder'

    # Get all the encrypted files from the database
    encrypted_files = EncryptedFile.objects.all()

    for encrypted_file in encrypted_files:
        # Read the encrypted data from the database
        encrypted_data = encrypted_file.data

        # Decrypt the data
        decrypted_data = cipher_suite.decrypt(encrypted_data)

        # Write the decrypted data to a new file with a .log extension
        with open(os.path.join(log_folder + "/decrypted_logs", encrypted_file.filename), 'wb') as f:
            f.write(decrypted_data)