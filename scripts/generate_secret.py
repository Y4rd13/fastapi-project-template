import secrets
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def generate_hashed_password(plain_password: str) -> str:
    return pwd_context.hash(plain_password)

def decode_hashed_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


if __name__ == "__main__":
    plain_password = input("Enter your password: ")
    hashed_password = generate_hashed_password(plain_password)
    print(hashed_password)
    print("Password verification: ")
    print(decode_hashed_password(plain_password, hashed_password))
    print("Secret key: ")
    print(secrets.token_hex(32))