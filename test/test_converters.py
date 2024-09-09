import pytest

from loman import Computation, States


def test_conversion_on_add_node():
    comp = Computation()
    comp.add_node('a', value=1, converter=float)
    assert comp.s.a == States.UPTODATE and isinstance(comp.v.a, float) and comp.v.a == 1.0


def test_conversion_on_insert():
    comp = Computation()
    comp.add_node('a', converter=float)
    comp.insert('a', 1)
    assert comp.s.a == States.UPTODATE and isinstance(comp.v.a, float) and comp.v.a == 1.0


def test_conversion_on_computation():
    comp = Computation()
    comp.add_node('a')
    comp.add_node('b', lambda a: a + 1, converter=float)
    comp.insert('a', 1)
    comp.compute_all()
    assert comp.s.b == States.UPTODATE and isinstance(comp.v.b, float) and comp.v.b == 2.0


def throw_exception(value):
    raise ValueError("Error")


def test_exception_on_add_node():
    comp = Computation()
    with pytest.raises(ValueError):
        comp.add_node('a', value=1, converter=throw_exception)


def test_exception_on_insert():
    comp = Computation()
    comp.add_node('a', converter=throw_exception)
    with pytest.raises(ValueError):
        comp.insert('a', 1)


def test_exception_on_computation():
    comp = Computation()
    comp.add_node('a')
    comp.add_node('b', lambda a: a + 1, converter=throw_exception)
    comp.insert('a', 1)
    comp.compute_all()
    assert comp.s.b == States.ERROR
    assert isinstance(comp.v.b.exception, ValueError)
