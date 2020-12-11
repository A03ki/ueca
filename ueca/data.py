import pint
import sympy

import copy
from numbers import Real
from typing import Any, Optional, Union


ureg = pint.UnitRegistry()


class PhysicsData:
    def __init__(self, magnitude: Any, unit: str, left_side: str = "",
                 symbol: Optional[Union[str, sympy.Basic]] = None,
                 uncertainty: Optional[Real] = None,
                 base_symbols: Optional[dict] = None) -> None:
        if isinstance(symbol, str):
            if not symbol.isdecimal() and symbol != "":
                symbol = sympy.Symbol(symbol)

        if isinstance(symbol, sympy.Basic):
            self.data = ureg.Quantity(symbol, unit)
        else:
            self.data = ureg.Quantity(magnitude, unit)
            if uncertainty:
                self.data = self.data.plus_minus(uncertainty)

        self.symbol = symbol
        self.__uncertainty = uncertainty
        self.left_side = left_side

        if base_symbols is None:
            self._base_symbols = dict()
        else:
            self._base_symbols = base_symbols

        if isinstance(symbol, sympy.Symbol) and str(symbol) not in self._base_symbols:
            data = ureg.Quantity(magnitude, unit)
            if uncertainty:
                data = data.plus_minus(uncertainty)
            self._base_symbols[str(symbol)] = data

    @property
    def magnitude(self) -> Any:
        if self.is_symbolic():
            symbol_args = [sympy.Symbol(k) for k in sorted(self._base_symbols.keys())]
            values = [self._base_symbols[k].magnitude for k in sorted(self._base_symbols.keys())]
            return sympy.lambdify(symbol_args, self.symbol, modules="numpy")(*values)
        return self.data.magnitude

    @property
    def unit(self) -> str:
        return str(self.data.units)

    @property
    def uncertainty(self) -> Real:
        if isinstance(self.data, ureg.Measurement):
            return self.data.error.magnitude
        return self.__uncertainty

    def is_symbolic(self):
        if isinstance(self.symbol, sympy.Basic):
            return True
        return False

    def __add__(self, other: Any) -> "PhysicsData":
        other = as_physicsdata(other)
        new_data = self.data + other.data
        if self.is_symbolic():
            symbols = copy.deepcopy(self._base_symbols)
            symbols.update(other._base_symbols)
            return PhysicsData(None, str(new_data.units), symbol=new_data.magnitude,
                               base_symbols=symbols)
        return PhysicsData(new_data.magnitude, str(new_data.units))

    __radd__ = __add__

    def __sub__(self, other: Any) -> "PhysicsData":
        other = as_physicsdata(other)
        new_data = self.data - other.data
        if self.is_symbolic():
            symbols = copy.deepcopy(self._base_symbols)
            symbols.update(other._base_symbols)
            return PhysicsData(None, str(new_data.units), symbol=new_data.magnitude,
                               base_symbols=symbols)
        return PhysicsData(new_data.magnitude, str(new_data.units))

    def __rsub__(self, other: Any) -> "PhysicsData":
        other = as_physicsdata(other)
        new_data = other.data - self.data
        if self.is_symbolic():
            symbols = copy.deepcopy(self._base_symbols)
            symbols.update(other._base_symbols)
            return PhysicsData(None, str(new_data.units), symbol=new_data.magnitude,
                               base_symbols=symbols)
        return PhysicsData(new_data.magnitude, str(new_data.units))

    def __mul__(self, other: Any) -> "PhysicsData":
        other = as_physicsdata(other)
        new_data = self.data * other.data
        if self.is_symbolic():
            symbols = copy.deepcopy(self._base_symbols)
            symbols.update(other._base_symbols)
            return PhysicsData(None, str(new_data.units), symbol=new_data.magnitude,
                               base_symbols=symbols)
        return PhysicsData(new_data.magnitude, str(new_data.units))

    __rmul__ = __mul__

    def __floordiv__(self, other: Any) -> "PhysicsData":
        other = as_physicsdata(other)
        new_magnitude = self.data.magnitude // other.data.magnitude
        new_units = self.data.units / other.data.units
        if self.is_symbolic():
            symbols = copy.deepcopy(self._base_symbols)
            symbols.update(other._base_symbols)
            return PhysicsData(None, str(new_units), symbol=new_magnitude,
                               base_symbols=symbols)
        return PhysicsData(new_magnitude, str(new_units))

    def __rfloordiv__(self, other: Any) -> "PhysicsData":
        other = as_physicsdata(other)
        new_magnitude = other.data.magnitude // self.data.magnitude
        new_units = self.data.units / other.data.units
        if self.is_symbolic():
            symbols = copy.deepcopy(self._base_symbols)
            symbols.update(other._base_symbols)
            return PhysicsData(None, str(new_units), symbol=new_magnitude,
                               base_symbols=symbols)
        return PhysicsData(new_magnitude, str(new_units))

    def __truediv__(self, other: Any) -> "PhysicsData":
        other = as_physicsdata(other)
        new_data = self.data / other.data
        if self.is_symbolic():
            symbols = copy.deepcopy(self._base_symbols)
            symbols.update(other._base_symbols)
            return PhysicsData(None, str(new_data.units), symbol=new_data.magnitude,
                               base_symbols=symbols)
        return PhysicsData(new_data.magnitude, str(new_data.units))

    def __rtruediv__(self, other: Any) -> "PhysicsData":
        other = as_physicsdata(other)
        new_data = other.data / self.data
        if self.is_symbolic():
            symbols = copy.deepcopy(self._base_symbols)
            symbols.update(other._base_symbols)
            return PhysicsData(None, str(new_data.units), symbol=new_data.magnitude,
                               base_symbols=symbols)
        return PhysicsData(new_data.magnitude, str(new_data.units))

    def __pow__(self, n: Union[int, float]) -> "PhysicsData":
        other = as_physicsdata(n)
        new_data = self.data ** other.data
        if self.is_symbolic():
            symbols = copy.deepcopy(self._base_symbols)
            return PhysicsData(None, str(new_data.units), symbol=new_data.magnitude,
                               base_symbols=symbols)
        return PhysicsData(new_data.magnitude, str(new_data.units))

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
