"""Demonstration of Python properties (getter/setter) with validation."""


class User:
    """A simple user with validated name, login, password, and email fields.

    Every field is backed by a property. Setting any field marks the object
    as modified, and ``None`` values are rejected with a ``ValueError``.
    """

    def __init__(self, name: str, login: str, password: str, email: str) -> None:
        self._is_modified = False
        self.name = name
        self.login = login
        self.password = password
        self.email = email
        # Reset flag -- the assignments above set it to True
        self._is_modified = False

    @property
    def is_modified(self) -> bool:
        """Whether any field has been changed since creation."""
        return self._is_modified

    # -- name --
    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        if value is None:
            raise ValueError("Name cannot be None!")
        self._is_modified = True
        self._name = value

    # -- login --
    @property
    def login(self) -> str:
        return self._login

    @login.setter
    def login(self, value: str) -> None:
        if value is None:
            raise ValueError("Login cannot be None!")
        self._is_modified = True
        self._login = value

    # -- password --
    @property
    def password(self) -> str:
        return self._password

    @password.setter
    def password(self, value: str) -> None:
        if value is None:
            raise ValueError("Password cannot be None!")
        self._is_modified = True
        self._password = value

    # -- email --
    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str) -> None:
        if value is None:
            raise ValueError("Email cannot be None!")
        self._is_modified = True
        self._email = value


if __name__ == "__main__":
    user = User(
        name="John User",
        login="j.user",
        email="j.user@gmail.com",
        password="p4ssw0rd!",
    )
    print(f"Created a User. Is it modified? {user.is_modified}")

    user.name = "Updated name"
    print(f"Changed a User. Is it modified? {user.is_modified}")
