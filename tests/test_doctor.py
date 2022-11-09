"""Tests for statistics functions within the Model layer."""

import numpy as np
import numpy.testing as npt
import pytest


def test_doctor_creation():
    """Check that a Doctor gets created correctly
    and that its name attribute works"""
    from inflammation.models import Doctor

    doctor = Doctor('Sally',None)
    npt.assert_array_equal(doctor.name, 'Sally')


def test_doctor_patients():
    """Check that a Doctor's attributed patients works correctly"""
    from inflammation.models import Doctor, Patient

    doctor = Doctor('Sally',None)
    p1 = Patient('Joe')
    p2 = Patient('Josh')
    p3 = Patient('Jill')

    doctor.patients.append(p1)
    doctor.patients.append(p2)
    doctor.patients.append(p3)
    npt.assert_array_equal(doctor.patients,[p1,p2,p3])