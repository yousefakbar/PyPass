import os
import subprocess


class Pass:
    def show_password_from_path(self, path):
        # path should be relative to $PASSWORD_STORE_DIR, not a full literal path
        res = subprocess.run(['pass', path], stdout=subprocess.PIPE, check=True)
        return res.stdout.decode('utf-8')

    
    def copy_password_from_path(self, path):
        subprocess.run(['pass', '-c', path], check=True)


    def copy_otp_from_path(self, path):
        subprocess.run(['pass', 'otp', '-c', path], check=True)
