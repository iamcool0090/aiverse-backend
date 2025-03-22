from abc import ABC, abstractmethod


class BaseDB(ABC):
    """
    Abstract base class for database operations.
    This class defines the interface for database clients, ensuring consistent
    behavior across different database implementations.
    Methods
    -------
    _set_schema()
        Abstract method to define the schema for the database.
    _initialize_client()
        Abstract method to establish a connection with the database.
    add(data)
        Abstract method to add data to the database.
    get(query)
        Abstract method to retrieve data from the database based on a query.
    get_all_characters()
        Abstract method to retrieve all character records from the database.
    """
    def __init__(self):
        self._initialize_client()
        pass
    

    @abstractmethod
    def _set_schema(self):
        pass

    @abstractmethod
    def _initialize_client(self):
        pass


    @abstractmethod
    def add(self, data):
        pass

    @abstractmethod
    def get(self, query):
        pass

    @abstractmethod
    def get_all_characters(self):
        pass

