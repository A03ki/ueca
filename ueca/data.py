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
        if not isinstance(other, PhysicsData):
            other = PhysicsData(other, "dimensionless")
        new_data = self.data + other.data
        return PhysicsData(new_data.magnitude, str(new_data.units))

    def __sub__(self, other: Any) -> "PhysicsData":
        if not isinstance(other, PhysicsData):
            other = PhysicsData(other, "dimensionless")
        new_data = self.data - other.data
        return PhysicsData(new_data.magnitude, str(new_data.units))

    def __mul__(self, other: Any) -> "PhysicsData":
        if not isinstance(other, PhysicsData):
            other = PhysicsData(other, "dimensionless")
        new_data = self.data * other.data
        return PhysicsData(new_data.magnitude, str(new_data.units))

    def __floordiv__(self, other: Any) -> "PhysicsData":
        if not isinstance(other, PhysicsData):
            other = PhysicsData(other, "dimensionless")
        new_data = self.data // other.data
        return PhysicsData(new_data.magnitude, str(new_data.units))

    def __truediv__(self, other: Any) -> "PhysicsData":
        if not isinstance(other, PhysicsData):
            other = PhysicsData(other, "dimensionless")
        new_data = self.data / other.data
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
