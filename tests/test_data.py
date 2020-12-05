from ueca.data import PhysicsData, as_physicsdata


class TestPhysicsData:
    def test_add_physicsdata(self):
        length_values = [2.3, 6.7, 9.0]
        unit = "meter"
        length1 = PhysicsData(length_values[0], unit)
        length2 = PhysicsData(length_values[1], unit)
        length3 = length1 + length2
        assert length3.magnitude == length_values[2]
        assert str(length3.unit) == unit

    def test_add_except_physicsdata(self):
        unit = "dimensionless"
        length1 = PhysicsData(11, unit)
        length2 = (length1 + 2) + 2.0
        assert length2.magnitude == 15.0
        assert str(length2.unit) == unit

    def test_radd_except_physicsdata(self):
        unit = "dimensionless"
        length1 = PhysicsData(3, unit)
        length2 = 10.0 + (5 + length1)
        assert length2.magnitude == 18.0
        assert str(length2.unit) == unit

    def test_sub_physicsdata(self):
        length_values = [6.3, 2.5, 3.8]
        unit = "meter"
        length1 = PhysicsData(length_values[0], unit)
        length2 = PhysicsData(length_values[1], unit)
        length3 = length1 - length2
        assert length3.magnitude == length_values[2]
        assert str(length3.unit) == unit

    def test_sub_except_physicsdata(self):
        unit = "dimensionless"
        length1 = PhysicsData(11, unit)
        length2 = (length1 - 2) - 2.0
        assert length2.magnitude == 7.0
        assert str(length2.unit) == unit

    def test_rsub_except_physicsdata(self):
        unit = "dimensionless"
        length1 = PhysicsData(3, unit)
        length2 = 10.0 - (5 - length1)
        assert length2.magnitude == 8.0
        assert str(length2.unit) == unit

    def test_mul_physicsdata(self):
        length_values = [7.0, 3.0, 21.0]
        units = ["meter", "meter ** 2"]
        length1 = PhysicsData(length_values[0], units[0])
        length2 = PhysicsData(length_values[1], units[0])
        length3 = length1 * length2
        assert length3.magnitude == length_values[2]
        assert str(length3.unit) == units[1]

    def test_mul_except_physicsdata(self):
        unit = "meter"
        length1 = PhysicsData(11, unit)
        length2 = (length1 * 2) * 2.0
        assert length2.magnitude == 44.0
        assert str(length2.unit) == unit

    def test_rmul_except_physicsdata(self):
        unit = "meter"
        length1 = PhysicsData(3, unit)
        length2 = 10.0 * (5 * length1)
        assert length2.magnitude == 150.0
        assert str(length2.unit) == unit

    def test_floordiv_physicsdata(self):
        length_values = [9.3, 4.0, 2.0]
        units = ["meter", "dimensionless"]
        length1 = PhysicsData(length_values[0], units[0])
        length2 = PhysicsData(length_values[1], units[0])
        length3 = length1 // length2
        assert length3.magnitude == length_values[2]
        assert str(length3.unit) == units[1]

    def test_floordiv_except_physicsdata(self):
        unit = "meter"
        length1 = PhysicsData(11, unit)
        length2 = (length1 // 2) // 2.0
        assert length2.magnitude == 2
        assert str(length2.unit) == unit

    def test_rfloordiv_except_physicsdata(self):
        unit = "meter"
        length1 = PhysicsData(3, unit)
        length2 = 10.0 // (5 // length1)
        assert length2.magnitude == 10
        assert str(length2.unit) == unit

    def test_truediv_physicsdata(self):
        length_values = [9.3, 4.0, 2.325]
        units = ["meter", "dimensionless"]
        length1 = PhysicsData(length_values[0], units[0])
        length2 = PhysicsData(length_values[1], units[0])
        length3 = length1 / length2
        assert length3.magnitude == length_values[2]
        assert str(length3.unit) == units[1]

    def test_truediv_except_physicsdata(self):
        unit = "meter"
        length1 = PhysicsData(11, unit)
        length2 = (length1 / 2) / 2.0
        assert length2.magnitude == 2.75
        assert str(length2.unit) == unit

    def test_rtruediv_except_physicsdata(self):
        unit = "meter"
        length1 = PhysicsData(2, unit)
        length2 = 10.0 / (5 / length1)
        assert length2.magnitude == 4.0
        assert str(length2.unit) == unit


def test_as_physicsdata_physicsdata():
    unit = "meter"
    magnitude = 2
    x = PhysicsData(magnitude, unit)
    assert isinstance(x, PhysicsData)
    assert x.magnitude == magnitude
    assert x.unit == unit


def test_as_physicsdata_except_physicsdata():
    unit = "dimensionless"
    magnitude = 2
    x = as_physicsdata(magnitude)
    assert isinstance(x, PhysicsData)
    assert x.magnitude == magnitude
    assert x.unit == unit
