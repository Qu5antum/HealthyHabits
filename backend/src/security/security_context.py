from passlib.hash import argon2

# şifreyi hash etmek
def hash_password(password: str):
    hashed_password = argon2.hash(password)
    return hashed_password

# şifreyi dehash etmek
def check_hashes(password_in: str, hashed_password):
    return argon2.verify(password_in, hashed_password)  