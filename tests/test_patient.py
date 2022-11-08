"""Tests for the Patient model."""


def test_create_patient():
    from inflammation.models import Patient

    name = 'Alice'
    p = Patient(name=name)
    p.add_observation('super strong today', day=0)
    p.add_observation('looking a little green')

    assert p.name == name
    assert [observation.value for observation in p.observations] == ['super strong today', 'looking a little green']
    assert [observation.day for observation in p.observations] == [0,1]