# Class.py
# This module defines an abstract class that represents a class at a school

from abc import ABC, abstractmethod
from src.class_scheduler.SectionList import SectionList

#Class to represent a section of a course at a school
# Subclasses must override conflictsWith, and may need to override __eq__
class Class(ABC):

	# Constructor for Class object
	# Member variables:
	# name: the name of the course
	# courseNum: the course number for the given Class object
	# sectionNum: the section number for the given Class object
	# classTimes: a dictionary of ClassTime objects describing when class meetings take place;
	#   Keys are uppercase day identifiers (i.e. M, T, W, R, F)
	#   Use the key "U" with an UndefinedClassTime object to indicate that a particular class has an undefined time
	# corecs: a SectionList object that defines the corecs for the given class
	def __init__(self, name, courseNum, sectionNum, classTimes):
		self.name = name
		self.courseNum = courseNum
		self.sectionNum = sectionNum
		self.classTimes = {}
		self.addTimes(classTimes)
		self.corecs = SectionList()

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

	# Function to add a corec to the class
	# courseNum: the course number of the corec
	# sectionList: a Python list of Class objects that represent the classes of courseNum that are corecs for
	# the class section represented by self
	def addCorec(self, courseNum, sectionsList):
		self.corecs.insertSectionsForNewCourse(courseNum, sectionsList)

	# Function to determine if the class has any corecs
	def hasCorecs(self):
		return not self.corecs.isEmpty()

	# Function to allow use of in operator when a Class object is in a container
	# A subclass can override this method or use the default implementation
	def __eq__(self, other):
		areSame = ((self.courseNum == other.courseNum) and (self.sectionNum == other.sectionNum))
		return areSame
