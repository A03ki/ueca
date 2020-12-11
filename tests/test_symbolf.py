import pytest

from ueca.data import PhysicsData
from ueca.symbolf import (physicsdata_symbolic_exception,
                          physicsdata_symbolic_dimensionless_exception, diff_symbol,
                          exp, log, ln, sqrt, sin, cos, tan, asin, acos, atan,
                          sinh, cosh, tanh, asinh, acosh, atanh)


def test_physicsdata_symbolic_exception_input_unexpected_type():
    with pytest.raises(TypeError):
        physicsdata_symbolic_exception(lambda x: x)(1)


def test_physicsdata_symbolic_exception_input_physicsdata_non_symbolic_mode():
    length = PhysicsData(1, "meter")
    with pytest.raises(ValueError):
        physicsdata_symbolic_exception(lambda x: x)(length)


def test_physicsdata_symbolic_dimensionless_exception():
    length = PhysicsData(1, "meter", symbol="x")
    with pytest.raises(ValueError):
        physicsdata_symbolic_dimensionless_exception(lambda x: x)(length)


class TestDiffSymbol:  # test for diff_symbol
    def test_input_physicsdata_atom(self):
        values = [1, 1]
        symbols = ["l1", "1"]
        units = ["meter", "dimensionless"]
        length = PhysicsData(values[0], units[0], symbol=symbols[0])
        value = diff_symbol(length, length, 1)
        assert str(value.symbol) == symbols[1]
        assert value.magnitude == values[1]
        assert value.unit == units[1]
        assert value._base_symbols == dict()

    def test_input_physicsdata_add(self):
        length1 = PhysicsData(1, "meter", symbol="x")
        length2 = PhysicsData(2, "meter", symbol="y")
        length3 = length1 + length2
        with pytest.raises(ValueError):
            diff_symbol(length3, length1, 1)

    def test_input_physicsdata_sub(self):
        length1 = PhysicsData(1, "meter", symbol="x")
        length2 = PhysicsData(2, "meter", symbol="y")
        length3 = length1 - length2
        with pytest.raises(ValueError):
            diff_symbol(length3, length1, 1)

    def test_input_physicsdata_mul(self):
        values = [2, 3, 6]
        symbols = ["m", "a", "a*m"]
        units = ["kilogram", "meter / second**2", "kilogram * meter / second ** 2"]
        mass = PhysicsData(values[0], units[0], symbol=symbols[0])
        acceleration = PhysicsData(values[1], units[1], symbol=symbols[1])
        power = mass * acceleration
        assert str(power.symbol) == symbols[2]
        assert power.magnitude == values[2]
        assert power.unit == units[2]
        acceleration2 = diff_symbol(power, mass, 1)
        assert acceleration.symbol == acceleration2.symbol
        assert acceleration.magnitude == acceleration2.magnitude
        assert acceleration.unit == acceleration2.unit
        assert acceleration._base_symbols == acceleration2._base_symbols
        mass2 = diff_symbol(power, acceleration, 1)
        assert mass.symbol == mass2.symbol
        assert mass.magnitude == mass2.magnitude
        assert mass.unit == mass2.unit
        assert mass._base_symbols == mass2._base_symbols

    def test_input_physicsdata_pow(self):
        values = [3, 27, 18]
        symbols = ["l1", "3*l1**2", "6*l1"]
        units = ["meter", "meter ** 2", "meter ** 3"]
        length = PhysicsData(values[0], units[0], symbol=symbols[0])
        area = length * length
        volume = length * length * length
        area2 = diff_symbol(volume, length, 1)
        assert str(area2.symbol) == symbols[1]
        assert area.unit == area2.unit
        assert area2.magnitude == values[1]
        assert area._base_symbols == area2._base_symbols
        length2 = diff_symbol(volume, length, 2)
        assert str(length2.symbol) == symbols[2]
        assert length2.magnitude == values[2]
        assert length.unit == length2.unit
        assert length._base_symbols == length2._base_symbols

    def test_input_string_symbol(self):
        values = [2, 3, 18, 9, 6, 2]
        symbols = ["l1", "l2", "l1*l2**2", "l2**2", "2*l2", "2"]
        units = ["meter", "meter ** 2", "meter ** 3", "dimensionless"]
        length1 = PhysicsData(values[0], units[0], symbol=symbols[0])
        length2 = PhysicsData(values[1], units[0], symbol=symbols[1])
        volume = length1 * length2 * length2
        assert str(volume.symbol) == symbols[2]
        assert volume.magnitude == values[2]
        assert volume.unit == units[2]
        area = diff_symbol(volume, length1, 1)
        assert str(area.symbol) == symbols[3]
        assert area.magnitude == values[3]
        assert area.unit == units[1]
        assert len(area._base_symbols) == 1
        assert str(area._base_symbols[symbols[1]].units) == units[0]
        length3 = diff_symbol(area, length2, 1)
        assert str(length3.symbol) == symbols[4]
        assert length3.magnitude == values[4]
        assert length3.unit == units[0]
        assert len(area._base_symbols) == 1
        assert str(area._base_symbols[symbols[1]].units) == units[0]
        value = diff_symbol(length3, length2, 1)
        assert str(value.symbol) == symbols[5]
        assert value.magnitude == values[5]
        assert value.unit == units[3]
        assert value._base_symbols == dict()

    def test_input_unexpected_type(self):
        length = PhysicsData(1, "meter", symbol="l1")
        with pytest.raises(TypeError):
            diff_symbol(length, 3.0, 1)

    def test_input_physicsdata_non_symbolic_mode(self):
        length = PhysicsData(1, "meter")
        with pytest.raises(ValueError):
            diff_symbol(length, 3.0, 1)

    def test_input_string_non_symbol(self):
        length = PhysicsData(1, "meter", symbol="l1")
        with pytest.raises(ValueError):
            diff_symbol(length, "l2", 1)

    def test_input_string_non_symbol_dimensionless(self):
        unit = "dimensionless"
        value = PhysicsData(3, unit, symbol="l1")
        value2 = diff_symbol(value, "l2", 1)
        assert str(value2.symbol) == "0"
        assert value2.magnitude == 0
        assert value2.unit == unit
        assert value2._base_symbols == dict()


def test_exp():
    length1 = PhysicsData(1, "dimensionless", symbol="x")
    length2 = exp(length1)
    assert str(length2.symbol) == "exp(x)"
    assert length2.unit == length1.unit
    assert length2._base_symbols == length1._base_symbols
    with pytest.raises(ValueError):
        exp(PhysicsData(1, "meter", symbol="x"))


def test_log():
    length1 = PhysicsData(1, "dimensionless", symbol="x")
    length2 = log(length1)
    assert str(length2.symbol) == "log(x)"
    assert length2.unit == length1.unit
    assert length2._base_symbols == length1._base_symbols
    with pytest.raises(ValueError):
        log(PhysicsData(1, "meter", symbol="x"))


def test_ln():
    length1 = PhysicsData(1, "dimensionless", symbol="x")
    length2 = ln(length1)
    assert str(length2.symbol) == "log(x)"
    assert length2.unit == length1.unit
    assert length2._base_symbols == length1._base_symbols
    with pytest.raises(ValueError):
        ln(PhysicsData(1, "meter", symbol="x"))


def test_sqrt():
    length1 = PhysicsData(1, "dimensionless", symbol="x")
    length2 = sqrt(length1)
    assert str(length2.symbol) == "sqrt(x)"
    assert length2.unit == length1.unit
    assert length2._base_symbols == length1._base_symbols
    with pytest.raises(ValueError):
        sqrt(PhysicsData(1, "meter", symbol="x"))


def test_sin():
    length1 = PhysicsData(1, "dimensionless", symbol="x")
    length2 = sin(length1)
    assert str(length2.symbol) == "sin(x)"
    assert length2.unit == length1.unit
    assert length2._base_symbols == length1._base_symbols
    with pytest.raises(ValueError):
        sin(PhysicsData(1, "meter", symbol="x"))


def test_cos():
    length1 = PhysicsData(1, "dimensionless", symbol="x")
    length2 = cos(length1)
    assert str(length2.symbol) == "cos(x)"
    assert length2.unit == length1.unit
    assert length2._base_symbols == length1._base_symbols
    with pytest.raises(ValueError):
        cos(PhysicsData(1, "meter", symbol="x"))


def test_tan():
    length1 = PhysicsData(1, "dimensionless", symbol="x")
    length2 = tan(length1)
    assert str(length2.symbol) == "tan(x)"
    assert length2.unit == length1.unit
    assert length2._base_symbols == length1._base_symbols
    with pytest.raises(ValueError):
        tan(PhysicsData(1, "meter", symbol="x"))


def test_asin():
    length1 = PhysicsData(1, "dimensionless", symbol="x")
    length2 = asin(length1)
    assert str(length2.symbol) == "asin(x)"
    assert length2.unit == length1.unit
    assert length2._base_symbols == length1._base_symbols
    with pytest.raises(ValueError):
        asin(PhysicsData(1, "meter", symbol="x"))


def test_acos():
    length1 = PhysicsData(1, "dimensionless", symbol="x")
    length2 = acos(length1)
    assert str(length2.symbol) == "acos(x)"
    assert length2.unit == length1.unit
    assert length2._base_symbols == length1._base_symbols
    with pytest.raises(ValueError):
        acos(PhysicsData(1, "meter", symbol="x"))


def test_atan():
    length1 = PhysicsData(1, "dimensionless", symbol="x")
    length2 = atan(length1)
    assert str(length2.symbol) == "atan(x)"
    assert length2.unit == length1.unit
    assert length2._base_symbols == length1._base_symbols
    with pytest.raises(ValueError):
        atan(PhysicsData(1, "meter", symbol="x"))


def test_sinh():
    length1 = PhysicsData(1, "dimensionless", symbol="x")
    length2 = sinh(length1)
    assert str(length2.symbol) == "sinh(x)"
    assert length2.unit == length1.unit
    assert length2._base_symbols == length1._base_symbols
    with pytest.raises(ValueError):
        sinh(PhysicsData(1, "meter", symbol="x"))


def test_conh():
    length1 = PhysicsData(1, "dimensionless", symbol="x")
    length2 = cosh(length1)
    assert str(length2.symbol) == "cosh(x)"
    assert length2.unit == length1.unit
    assert length2._base_symbols == length1._base_symbols
    with pytest.raises(ValueError):
        cosh(PhysicsData(1, "meter", symbol="x"))


def test_tanh():
    length1 = PhysicsData(1, "dimensionless", symbol="x")
    length2 = tanh(length1)
    assert str(length2.symbol) == "tanh(x)"
    assert length2.unit == length1.unit
    assert length2._base_symbols == length1._base_symbols
    with pytest.raises(ValueError):
        tanh(PhysicsData(1, "meter", symbol="x"))


def test_asinh():
    length1 = PhysicsData(1, "dimensionless", symbol="x")
    length2 = asinh(length1)
    assert str(length2.symbol) == "asinh(x)"
    assert length2.unit == length1.unit
    assert length2._base_symbols == length1._base_symbols
    with pytest.raises(ValueError):
        asinh(PhysicsData(1, "meter", symbol="x"))


def test_acosh():
    length1 = PhysicsData(1, "dimensionless", symbol="x")
    length2 = acosh(length1)
    assert str(length2.symbol) == "acosh(x)"
    assert length2.unit == length1.unit
    assert length2._base_symbols == length1._base_symbols
    with pytest.raises(ValueError):
        acosh(PhysicsData(1, "meter", symbol="x"))


def test_atanh():
    length1 = PhysicsData(1, "dimensionless", symbol="x")
    length2 = atanh(length1)
    assert str(length2.symbol) == "atanh(x)"
    assert length2.unit == length1.unit
    assert length2._base_symbols == length1._base_symbols
    with pytest.raises(ValueError):
        atanh(PhysicsData(1, "meter", symbol="x"))
