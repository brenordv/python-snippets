# -*- coding: utf-8 -*-

class User(object):
    def __init__(self, name: str, login: str, password: str, email: str):
        self.name = name
        self.login = login
        self.password = password
        self.email = email
        self.__is_modified__ = False

    def is_modified(self):
        return self.__is_modified__

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if value is None:
            raise ValueError("Name cannot be none!")
        self.__is_modified__ = True
        self.__name = value

    @property
    def login(self):
        return self.__login

    @login.setter
    def login(self, value):
        if value is None:
            raise ValueError("Login cannot be none!")
        self.__is_modified__ = True
        self.__login = value

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, value):
        if value is None:
            raise ValueError("Password cannot be none!")
        self.__is_modified__ = True
        self.__password = value

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        if value is None:
            raise ValueError("Email cannot be none!")
        self.__is_modified__ = True
        self.__email = value


if __name__ == '__main__':
    user = User(name="John User", login="j.user", email="j.user@gmail.com", password="p4ssw0rd!")

    print(f"Created an User. Is it modified? {user.is_modified()}")

    user.name = "Updated name"

    print(f"Changed an User. Is it modified? {user.is_modified()}")
