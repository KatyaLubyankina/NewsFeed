from passlib.context import CryptContext

pwd_cxt = CryptContext(schemes=['bcrypt'], deprecated='auto')


class Hash():
    """

    This class provides password hashing and verifing.
    Password must be hashed before adding to the database.
    Function verify allows comparisment of plain and hashed passwords.

    """
    def bcrypt(password: str):
        return pwd_cxt.hash(password)

    def verify(hashed_password, plain_password):
        return pwd_cxt.verify(plain_password, hashed_password)
