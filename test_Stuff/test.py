from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

# Replace 'your_password' with the actual password
hashed_password = hash_password("matthias_123")
print(hashed_password)