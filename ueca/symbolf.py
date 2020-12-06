import sympy
from ueca.data import PhysicsData, ureg


def physicsdata_symbolic_exception(func):
    def wrapper(obj: PhysicsData, *args, **kwargs):
        if not isinstance(obj, PhysicsData):
            raise TypeError(f"The type of '{obj.__class__.__name__}' isn't 'PhysicsData'")

        if not isinstance(obj.magnitude, sympy.Basic):
            raise ValueError("'PhysicsData' isn't the symbolic mode")

        return func(obj, *args, **kwargs)
    return wrapper


@physicsdata_symbolic_exception
def diff_symbol(obj: PhysicsData, symbol: str, n: int) -> PhysicsData:
    if not (obj.magnitude.is_Atom or obj.magnitude.is_Pow or obj.magnitude.is_Mul):
        raise ValueError(f"unsupport differentiation for: '{obj.magnitude}'")

    if isinstance(symbol, PhysicsData):
        tgt_units = symbol.data.units
        symbol = symbol.magnitude
        if not isinstance(symbol, sympy.Symbol):
            raise ValueError(f"unsupport differentiation by non symbol: '{symbol}'")
    elif isinstance(symbol, str):
        if symbol in obj.symbols:
            tgt_unit = obj.symbols[symbol]
        elif obj.data.dimensionless:
            tgt_unit = "dimensionless"
        else:
            raise ValueError(f"'PhysicsData' don't include the symbol: '{symbol}'")
        tgt_units = ureg.parse_units(tgt_unit)

    else:
        raise TypeError(f"unsupport differentiation by type of '{symbol.__class__.__name__}'")

    new_units = obj.data.units / (tgt_units ** n)
    return PhysicsData(sympy.diff(obj.magnitude, symbol, n), new_units, left_side=obj.left_side,
                       symbols=obj.symbols)


@physicsdata_symbolic_exception
def exp(obj: PhysicsData) -> PhysicsData:
    return PhysicsData(sympy.exp(obj.magnitude), obj.unit, left_side=obj.left_side,
                       symbols=obj.symbols)


@physicsdata_symbolic_exception
def log(obj: PhysicsData) -> PhysicsData:
    return PhysicsData(sympy.log(obj.magnitude), obj.unit, left_side=obj.left_side,
                       symbols=obj.symbols)


@physicsdata_symbolic_exception
def ln(obj: PhysicsData) -> PhysicsData:
    return PhysicsData(sympy.ln(obj.magnitude), obj.unit, left_side=obj.left_side,
                       symbols=obj.symbols)


@physicsdata_symbolic_exception
def sqrt(obj: PhysicsData) -> PhysicsData:
    return PhysicsData(sympy.sqrt(obj.magnitude), obj.unit, left_side=obj.left_side,
                       symbols=obj.symbols)


@physicsdata_symbolic_exception
def sin(obj: PhysicsData) -> PhysicsData:
    return PhysicsData(sympy.sin(obj.magnitude), obj.unit, left_side=obj.left_side,
                       symbols=obj.symbols)


@physicsdata_symbolic_exception
def cos(obj: PhysicsData) -> PhysicsData:
    return PhysicsData(sympy.cos(obj.magnitude), obj.unit, left_side=obj.left_side,
                       symbols=obj.symbols)


@physicsdata_symbolic_exception
def tan(obj: PhysicsData) -> PhysicsData:
    return PhysicsData(sympy.tan(obj.magnitude), obj.unit, left_side=obj.left_side,
                       symbols=obj.symbols)


@physicsdata_symbolic_exception
def asin(obj: PhysicsData) -> PhysicsData:
    return PhysicsData(sympy.asin(obj.magnitude), obj.unit, left_side=obj.left_side,
                       symbols=obj.symbols)


@physicsdata_symbolic_exception
def acos(obj: PhysicsData) -> PhysicsData:
    return PhysicsData(sympy.acos(obj.magnitude), obj.unit, left_side=obj.left_side,
                       symbols=obj.symbols)


@physicsdata_symbolic_exception
def atan(obj: PhysicsData) -> PhysicsData:
    return PhysicsData(sympy.atan(obj.magnitude), obj.unit, left_side=obj.left_side,
                       symbols=obj.symbols)


@physicsdata_symbolic_exception
def sinh(obj: PhysicsData) -> PhysicsData:
    return PhysicsData(sympy.sinh(obj.magnitude), obj.unit, left_side=obj.left_side,
                       symbols=obj.symbols)


@physicsdata_symbolic_exception
def cosh(obj: PhysicsData) -> PhysicsData:
    return PhysicsData(sympy.cosh(obj.magnitude), obj.unit, left_side=obj.left_side,
                       symbols=obj.symbols)


@physicsdata_symbolic_exception
def tanh(obj: PhysicsData) -> PhysicsData:
    return PhysicsData(sympy.tanh(obj.magnitude), obj.unit, left_side=obj.left_side,
                       symbols=obj.symbols)


@physicsdata_symbolic_exception
def asinh(obj: PhysicsData) -> PhysicsData:
    return PhysicsData(sympy.asinh(obj.magnitude), obj.unit, left_side=obj.left_side,
                       symbols=obj.symbols)


@physicsdata_symbolic_exception
def acosh(obj: PhysicsData) -> PhysicsData:
    return PhysicsData(sympy.acosh(obj.magnitude), obj.unit, left_side=obj.left_side,
                       symbols=obj.symbols)


@physicsdata_symbolic_exception
def atanh(obj: PhysicsData) -> PhysicsData:
    return PhysicsData(sympy.atanh(obj.magnitude), obj.unit, left_side=obj.left_side,
                       symbols=obj.symbols)
