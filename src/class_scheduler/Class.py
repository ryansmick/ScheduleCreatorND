# Class.py
# This module defines an abstract class that represents a class at a school

from abc import ABC, abstractmethod

#Class to represent a section of a course at a school
# Subclasses must override conflictsWith and __eq__
class Class(ABC):

	# Constructor for Class object
	# Subclasses should define member variables self.name and self.classTimes
	#name: the name of the course
	# classTimes: a dictionary of ClassTime objects describing when class meetings take place; Keys are uppercase day identifiers (i.e. M, T, W, R, F)
	def __init__(self, name, classTimes):
		self.name = name
		self.classTimes = {}
		self.addTimes(classTimes)

	# Function to determine if two classes conflict
	# Returns true if the classes cannot be taken together, false otherwise
	@abstractmethod
	def conflictsWith(self, otherClass):
		raise NotImplementedError

	# Function to add times to the class
	# times is a dictionary with a letter representing the day as the key, and the ClassTime object as the value
	def addTimes(self, times):
		for day in times:
			self.classTimes[day.upper()] = times[day]

	# Function to allow use of in operator when a Class object is in a container
	# Any subclass must override this method, because the ScheduleBuilder makes use of the in operator
	@abstractmethod
	def __eq__(self, other):
		raise NotImplementedError