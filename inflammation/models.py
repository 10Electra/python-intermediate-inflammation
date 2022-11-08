"""Module containing models representing patients and their data.

The Model layer is responsible for the 'business logic' part of the software.

Patients' data is held in an inflammation table (2D array) where each row contains
inflammation data for a single patient taken over a number of days
and each column represents a single day across all patients.
"""

import numpy as np

class Observation:
    def __init__(self, day: int, value, doctor=None) -> None:
        self.day = day
        self.value = value
        self.doctor = doctor
    
    def __str__(self) -> str:
        return str(self.value)


class Person:
    def __init__(self,name: str) -> None:
        self.name = name
    
    def __str__(self) -> str:
        return self.name


class Patient(Person):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.observations = []

    @property
    def last_observation(self):
        return self.observations[-1]
    
    def add_observation(self,value, day=None, doctor=None):
        if day is None:
            try:
                day = self.observations[-1].day + 1
            except IndexError:
                day = 0
        
        new_observation = Observation(day, value, doctor)
        if doctor is not None:
            doctor.made_observation(new_observation,self)
        self.observations.append(new_observation)
        return new_observation


class Doctor(Person):
    def __init__(self, name: str, patients: list) -> None:
        super().__init__(name)
        self.patients = patients
        self.observations_made = []

    def made_observation(self, observation, patient):
        self.observations_made.append((observation,patient))


def load_csv(filename):
    """Load a Numpy array from a CSV

    :param filename: Filename of CSV to load
    :returns: a Numpy array with data from the CSV file
    """
    return np.loadtxt(fname=filename, delimiter=',')


def daily_mean(data):
    """Calculate the daily mean of a 2D inflammation data array.

    :param data: 2D Numpy array containing inflammation data
    :returns: A one-dimensional Numpy array containing mean averages"""
    return np.mean(data, axis=0)


def daily_std(data):
    """Calculate the standard deviation of a 2D inflammation data array

    Args:
        data (np.ndarray): Input inflammation data
    """
    return np.std(data,axis=0)


def daily_max(data):
    """Calculate the daily max of a 2D inflammation data array.

    :param data: 2D Numpy array containing inflammation data
    :returns: A one-dimensional Numpy array containing the max value of each column"""
    return np.max(data, axis=0)


def daily_min(data):
    """Calculate the daily min of a 2D inflammation data array.

    :param data: 2D Numpy array containing inflammation data
    :returns: A one-dimensional Numpy array containing the min value of each column"""
    return np.min(data, axis=0)


def patient_normalise(data):
    """Normalise patient data from 2D array of inflammation data

    Args:
        data (np.ndarray): 2D array of input data
    """
    if np.any(data < 0):
        raise ValueError('Inflammation values should not be zero')
    maxes = np.nanmax(data, axis=1)
    with np.errstate(invalid='ignore', divide='ignore'):
        normalised = data / maxes[:, np.newaxis]
    normalised[np.isnan(normalised)] = 0
    normalised[normalised < 0] = 0
    return normalised