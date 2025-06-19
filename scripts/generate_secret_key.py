
# generate_secret_key.py
import secrets

def generate_secret_key(length=50):
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    return ''.join(secrets.choice(chars) for _ in range(length))

if __name__ == "__main__":
    print("Generated Django SECRET_KEY:\n")
    print(generate_secret_key())


# 1. Navigate to your Django project folder, then activate your environment.
# venv\Scripts\activate

# 2. Enter the scripts folder
# cd scripts

# 3. python generate_secret_key.py
