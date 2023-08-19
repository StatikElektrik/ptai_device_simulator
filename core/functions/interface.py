"""
This class is the base class for all the function
implementations. It defines the interface that all
subclasses must implement.
"""

from abc import ABC, abstractmethod, abstractstaticmethod

class BaseFunction(ABC):
    """Follow this interface to implement a function for
    DataGenerator.
    """

    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def calculate(self, x: float) -> float:
        pass

    @abstractmethod
    def inverse(self, y: float) -> float:
        pass

    @abstractstaticmethod
    def plot() -> None:
        pass