import pint
import sympy

import copy
from typing import Any, Optional, Union


ureg = pint.UnitRegistry()


class PhysicsData:
    def __init__(self, magnitude, unit: str, left_side: str = "",
                 symbol: Optional[Union[str, sympy.Basic]] = None,
                 base_symbols: Optional[dict] = None) -> None:
        if isinstance(magnitude, str):
            if not magnitude.isdecimal() and magnitude != "":
                magnitude = sympy.Symbol(magnitude)

        self.data = ureg.Quantity(magnitude, unit)
        self.symbol = symbol
        self.left_side = left_side

        if base_symbols is None:
            self._base_symbols = dict()
        else:
            self._base_symbols = base_symbols

        if isinstance(magnitude, sympy.Symbol) and magnitude not in self._base_symbols:
            self._base_symbols[str(magnitude)] = str(self.data.units)

    @property
    def magnitude(self) -> Any:
        return self.data.magnitude

    @property
    def unit(self) -> str:
        return str(self.data.units)

    def is_symbolic(self):
        if isinstance(self.symbol, sympy.Basic):
            return True
        return False

    def __add__(self, other: Any) -> "PhysicsData":
        other = as_physicsdata(other)
        symbols = copy.deepcopy(self._base_symbols)
        symbols.update(other._base_symbols)
        new_data = self.data + other.data
        return PhysicsData(new_data.magnitude, str(new_data.units), base_symbols=symbols)

    __radd__ = __add__

    def __sub__(self, other: Any) -> "PhysicsData":
        other = as_physicsdata(other)
        symbols = copy.deepcopy(self._base_symbols)
        symbols.update(other._base_symbols)
        new_data = self.data - other.data
        return PhysicsData(new_data.magnitude, str(new_data.units), base_symbols=symbols)

    def __rsub__(self, other: Any) -> "PhysicsData":
        other = as_physicsdata(other)
        symbols = copy.deepcopy(self._base_symbols)
        symbols.update(other._base_symbols)
        new_data = other.data - self.data
        return PhysicsData(new_data.magnitude, str(new_data.units), base_symbols=symbols)

    def __mul__(self, other: Any) -> "PhysicsData":
        other = as_physicsdata(other)
        symbols = copy.deepcopy(self._base_symbols)
        symbols.update(other._base_symbols)
        new_data = self.data * other.data
        return PhysicsData(new_data.magnitude, str(new_data.units), base_symbols=symbols)

    __rmul__ = __mul__

    def __floordiv__(self, other: Any) -> "PhysicsData":
        other = as_physicsdata(other)
        symbols = copy.deepcopy(self._base_symbols)
        symbols.update(other._base_symbols)
        new_magnitude = self.data.magnitude // other.data.magnitude
        new_units = self.data.units / other.data.units
        return PhysicsData(new_magnitude, str(new_units), base_symbols=symbols)

    def __rfloordiv__(self, other: Any) -> "PhysicsData":
        other = as_physicsdata(other)
        symbols = copy.deepcopy(self._base_symbols)
        symbols.update(other._base_symbols)
        new_magnitude = other.data.magnitude // self.data.magnitude
        new_units = self.data.units / other.data.units
        return PhysicsData(new_magnitude, str(new_units), base_symbols=symbols)

    def __truediv__(self, other: Any) -> "PhysicsData":
        other = as_physicsdata(other)
        symbols = copy.deepcopy(self._base_symbols)
        symbols.update(other._base_symbols)
        new_data = self.data / other.data
        return PhysicsData(new_data.magnitude, str(new_data.units), base_symbols=symbols)

    def __rtruediv__(self, other: Any) -> "PhysicsData":
        other = as_physicsdata(other)
        symbols = copy.deepcopy(self._base_symbols)
        symbols.update(other._base_symbols)
        new_data = other.data / self.data
        return PhysicsData(new_data.magnitude, str(new_data.units), base_symbols=symbols)

    def __pow__(self, n: Union[int, float]) -> "PhysicsData":
        other = as_physicsdata(n)
        symbols = copy.deepcopy(self._base_symbols)
        new_data = self.data ** other.data
        return PhysicsData(new_data.magnitude, str(new_data.units), base_symbols=symbols)

    def __repr__(self) -> str:
        return str(self.data)

    def _repr_html_(self) -> str:
        return self.__repr__()

    def _repr_latex_(self, symbolic: bool = True) -> str:
        latex_spec = "{:~L}"
        if not symbolic:
            latex_spec = latex_spec.replace("~", "")

        text = latex_spec.format(self.data)

        if self.left_side != "":
            text = f"{self.left_side} = {text}"

        return text


def as_physicsdata(obj) -> PhysicsData:
    if not isinstance(obj, PhysicsData):
        obj = PhysicsData(obj, "dimensionless")
    return obj
