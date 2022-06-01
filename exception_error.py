class LoginError(Exception):
    pass


class LoginLargeSizeError(Exception):
    pass


class LoginShortSizeError(Exception):
    pass


class ConflictError(Exception):
    pass


class PasswordError(Exception):
    pass


class PasswordLargeSizeError(Exception):
    pass


class PasswordShortSizeError(Exception):
    pass


class CpfError(Exception):
    pass


class EmailError(Exception):
    pass


class PhoneError(Exception):
    pass


class CnpjError(Exception):
    pass


class DateError(Exception):
    pass


class DateFormatError(Exception):
    pass


class AuthenticateError(Exception):
    pass
