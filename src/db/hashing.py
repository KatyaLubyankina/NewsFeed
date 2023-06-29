from passlib.context import CryptContext

pwd_cxt = CryptContext(schemes=['bcrypt'], deprecated='auto')


class Hash():
    """This class provides password hashing and verifying.
    """
    def bcrypt(password: str) -> str:
        """Returns hashed password

        Args:
        - password (str): plain password

        Returns:
        - hashed password
        """
        return pwd_cxt.hash(password)

    def verify(hashed_password: str, plain_password: str) -> bool:
        """Verifies password

        Args:
            hashed_password (str)
            plain_password (str)

        Returns:
            True if password is correct
        """
        return pwd_cxt.verify(plain_password, hashed_password)
