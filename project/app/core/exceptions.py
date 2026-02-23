class BronzeException(Exception):
    pass


class ApiException(BronzeException):
    pass


class DatabaseException(BronzeException):
    pass


class SparkException(Exception):
    pass