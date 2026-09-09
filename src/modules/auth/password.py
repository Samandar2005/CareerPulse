from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher

password_hash_context = PasswordHash((Argon2Hasher(),))


def hash_password(password: str) -> str:
    return password_hash_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash_context.verify(plain_password, hashed_password)