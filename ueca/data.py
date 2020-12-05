import pint


from typing import Any


ureg = pint.UnitRegistry()


class PhysicsData:
    def __init__(self, magnitude, unit: str, left_side: str = "") -> None:
        self.data = ureg.Quantity(magnitude, unit)
        self.left_side = left_side

    @property
    def magnitude(self) -> Any:
        return self.data.magnitude

    @property
    def unit(self) -> str:
        return str(self.data.units)

    def __add__(self, other: Any) -> "PhysicsData":
        other = as_physicsdata(other)
        new_data = self.data + other.data
        return PhysicsData(new_data.magnitude, str(new_data.units))

    __radd__ = __add__

    def __sub__(self, other: Any) -> "PhysicsData":
        other = as_physicsdata(other)
        new_data = self.data - other.data
        return PhysicsData(new_data.magnitude, str(new_data.units))

    def __rsub__(self, other: Any) -> "PhysicsData":
        other = as_physicsdata(other)
        new_data = other.data - self.data
        return PhysicsData(new_data.magnitude, str(new_data.units))

    def __mul__(self, other: Any) -> "PhysicsData":
        other = as_physicsdata(other)
        new_data = self.data * other.data
        return PhysicsData(new_data.magnitude, str(new_data.units))

    __rmul__ = __mul__

    def __floordiv__(self, other: Any) -> "PhysicsData":
        other = as_physicsdata(other)
        new_magnitude = self.data.magnitude // other.data.magnitude
        new_units = self.data.units / other.data.units
        return PhysicsData(new_magnitude, str(new_units))

    def __rfloordiv__(self, other: Any) -> "PhysicsData":
        other = as_physicsdata(other)
        new_magnitude = other.data.magnitude // self.data.magnitude
        new_units = self.data.units / other.data.units
        return PhysicsData(new_magnitude, str(new_units))

    def __truediv__(self, other: Any) -> "PhysicsData":
        other = as_physicsdata(other)
        new_data = self.data / other.data
        return PhysicsData(new_data.magnitude, str(new_data.units))

    def __rtruediv__(self, other: Any) -> "PhysicsData":
        other = as_physicsdata(other)
        new_data = other.data / self.data
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
