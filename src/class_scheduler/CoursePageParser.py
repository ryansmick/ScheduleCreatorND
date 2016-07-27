# CoursePageParser.py
# This module defines an abstract class that represents the parser for a course page

# CoursePageParser:
# This class is used to define functionality that other course page parsers must implement

from abc import ABC, abstractmethod

class CoursePageParser(ABC):

	# Accepts an course number, and must return a list of Class objects representing every section of a given course
	# Should raise ValueError when the course number can't be parsed, the department is invalid, or the course can't be found
	@abstractmethod
	def getAllSectionsForCourse(self, courseNumberString):
		raise NotImplementedError

	# Function to get the corequisites for a specific course
	# classObject is an object of the Class class
	@abstractmethod
	def getCorecInfo(self, classObject):
		raise NotImplementedError