from ueca.data import PhysicsData


class TestPhysicsData:
    def test_add(self):
        length_values = [2.3, 6.7, 9.0]
        unit = "meter"
        length1 = PhysicsData(length_values[0], unit)
        length2 = PhysicsData(length_values[1], unit)
        length3 = length1 + length2
        assert length3.magnitude == length_values[2]
        assert str(length3.unit) == unit

    def test_sub(self):
        length_values = [6.3, 2.5, 3.8]
        unit = "meter"
        length1 = PhysicsData(length_values[0], unit)
        length2 = PhysicsData(length_values[1], unit)
        length3 = length1 - length2
        assert length3.magnitude == length_values[2]
        assert str(length3.unit) == unit

    def test_mul(self):
        length_values = [7.0, 3.0, 21.0]
        units = ["meter", "meter ** 2"]
        length1 = PhysicsData(length_values[0], units[0])
        length2 = PhysicsData(length_values[1], units[0])
        length3 = length1 * length2
        assert length3.magnitude == length_values[2]
        assert str(length3.unit) == units[1]

    def test_floordiv(self):
        length_values = [9.3, 4.0, 2.0]
        units = ["meter", "dimensionless"]
        length1 = PhysicsData(length_values[0], units[0])
        length2 = PhysicsData(length_values[1], units[0])
        length3 = length1 // length2
        assert length3.magnitude == length_values[2]
        assert str(length3.unit) == units[1]

    def test_truediv(self):
        length_values = [9.3, 4.0, 2.325]
        units = ["meter", "dimensionless"]
        length1 = PhysicsData(length_values[0], units[0])
        length2 = PhysicsData(length_values[1], units[0])
        length3 = length1 / length2
        assert length3.magnitude == length_values[2]
        assert str(length3.unit) == units[1]
