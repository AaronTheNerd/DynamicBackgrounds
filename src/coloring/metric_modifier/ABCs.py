from abc import abstractmethod

from serial.ABCs import SerialABC


# Takes a value between 0 and 1 and converts to a value between 0 and 1
class ModifierABC(SerialABC):
    @abstractmethod
    def get_value(self, t: float) -> float: ...


# Takes a value between 0 and 1 and converts to a value between 0 and 1 but its ends must be equal
class ReflectiveModifierABC(ModifierABC): ...
