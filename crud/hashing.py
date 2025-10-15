from passlib.context import CryptContext

pwd_ctx = CryptContext(schemes=["argon2"], deprecated="auto")

class Hash():
    def argon2(password: str):

        return pwd_ctx.hash(password)
