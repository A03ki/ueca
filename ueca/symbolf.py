import sympy
from ueca.data import PhysicsData, ureg


def physicsdata_symbolic_exception(func):
    def wrapper(obj: PhysicsData, *args, **kwargs):
        if not isinstance(obj, PhysicsData):
            raise TypeError(f"The type of '{obj.__class__.__name__}' isn't 'PhysicsData'")

        if not obj.is_symbolic():
            raise ValueError("'PhysicsData' isn't the symbolic mode")

        return func(obj, *args, **kwargs)
    return wrapper


@physicsdata_symbolic_exception
def diff_symbol(obj: PhysicsData, symbol: str, n: int) -> PhysicsData:
    if not (obj.symbol.is_Atom or obj.symbol.is_Pow or obj.symbol.is_Mul):
        raise ValueError(f"unsupport differentiation for: '{obj.symbol}'")

    if isinstance(symbol, PhysicsData):
        tgt_units = symbol.data.units
        symbol = symbol.symbol
        if not isinstance(symbol, sympy.Symbol):
            raise ValueError(f"unsupport differentiation by non symbol: '{symbol}'")
    elif isinstance(symbol, str):
        if symbol in obj._base_symbols:
            tgt_unit = str(obj._base_symbols[symbol].uints)
        elif obj.data.dimensionless:
            tgt_unit = "dimensionless"
        else:
            raise ValueError(f"'PhysicsData' don't include the symbol: '{symbol}'")
        tgt_units = ureg.parse_units(tgt_unit)

    else:
        raise TypeError(f"unsupport differentiation by type of '{symbol.__class__.__name__}'")

    new_symbol = sympy.diff(obj.symbol, symbol, n)
    new_unit = str(obj.data.units / (tgt_units ** n))
    _free_symbol_keys = [str(i) for i in new_symbol.free_symbols]
    new_symbols = {k: v for k, v in obj._base_symbols.items() if k in _free_symbol_keys}
    return PhysicsData(None, new_unit, symbol=new_symbol, base_symbols=new_symbols)


@physicsdata_symbolic_exception
def exp(obj: PhysicsData) -> PhysicsData:
    expr = sympy.exp(obj.symbol)
    return PhysicsData(None, obj.unit, symbol=expr, base_symbols=obj._base_symbols)


@physicsdata_symbolic_exception
def log(obj: PhysicsData) -> PhysicsData:
    expr = sympy.log(obj.symbol)
    return PhysicsData(None, obj.unit, symbol=expr, base_symbols=obj._base_symbols)


@physicsdata_symbolic_exception
def ln(obj: PhysicsData) -> PhysicsData:
    expr = sympy.ln(obj.symbol)
    return PhysicsData(None, obj.unit, symbol=expr, base_symbols=obj._base_symbols)


@physicsdata_symbolic_exception
def sqrt(obj: PhysicsData) -> PhysicsData:
    expr = sympy.sqrt(obj.symbol)
    return PhysicsData(None, obj.unit, symbol=expr, base_symbols=obj._base_symbols)


@physicsdata_symbolic_exception
def sin(obj: PhysicsData) -> PhysicsData:
    expr = sympy.sin(obj.symbol)
    return PhysicsData(None, obj.unit, symbol=expr, base_symbols=obj._base_symbols)


@physicsdata_symbolic_exception
def cos(obj: PhysicsData) -> PhysicsData:
    expr = sympy.cos(obj.symbol)
    return PhysicsData(None, obj.unit, symbol=expr, base_symbols=obj._base_symbols)


@physicsdata_symbolic_exception
def tan(obj: PhysicsData) -> PhysicsData:
    expr = sympy.tan(obj.symbol)
    return PhysicsData(None, obj.unit, symbol=expr, base_symbols=obj._base_symbols)


@physicsdata_symbolic_exception
def asin(obj: PhysicsData) -> PhysicsData:
    expr = sympy.asin(obj.symbol)
    return PhysicsData(None, obj.unit, symbol=expr, base_symbols=obj._base_symbols)


@physicsdata_symbolic_exception
def acos(obj: PhysicsData) -> PhysicsData:
    expr = sympy.acos(obj.symbol)
    return PhysicsData(None, obj.unit, symbol=expr, base_symbols=obj._base_symbols)


@physicsdata_symbolic_exception
def atan(obj: PhysicsData) -> PhysicsData:
    expr = sympy.atan(obj.symbol)
    return PhysicsData(None, obj.unit, symbol=expr, base_symbols=obj._base_symbols)


@physicsdata_symbolic_exception
def sinh(obj: PhysicsData) -> PhysicsData:
    expr = sympy.sinh(obj.symbol)
    return PhysicsData(None, obj.unit, symbol=expr, base_symbols=obj._base_symbols)


@physicsdata_symbolic_exception
def cosh(obj: PhysicsData) -> PhysicsData:
    expr = sympy.cosh(obj.symbol)
    return PhysicsData(None, obj.unit, symbol=expr, base_symbols=obj._base_symbols)


@physicsdata_symbolic_exception
def tanh(obj: PhysicsData) -> PhysicsData:
    expr = sympy.tanh(obj.symbol)
    return PhysicsData(None, obj.unit, symbol=expr, base_symbols=obj._base_symbols)


@physicsdata_symbolic_exception
def asinh(obj: PhysicsData) -> PhysicsData:
    expr = sympy.asinh(obj.symbol)
    return PhysicsData(None, obj.unit, symbol=expr, base_symbols=obj._base_symbols)


@physicsdata_symbolic_exception
def acosh(obj: PhysicsData) -> PhysicsData:
    expr = sympy.acosh(obj.symbol)
    return PhysicsData(None, obj.unit, symbol=expr, base_symbols=obj._base_symbols)


@physicsdata_symbolic_exception
def atanh(obj: PhysicsData) -> PhysicsData:
    expr = sympy.atanh(obj.symbol)
    return PhysicsData(None, obj.unit, symbol=expr, base_symbols=obj._base_symbols)
