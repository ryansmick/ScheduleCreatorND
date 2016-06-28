# Class.py
# This class defines a section of a course at Notre Dame
# Member variables:
# name: the name of the course
# crn: the course registration number, as defined by the university on Class Search
# courseNum: the course number for the course, which consists of a department identifier followed by a 5 digit number
# sectionNum: the section number of the particular class
# profName: the name of the professor teaching the course
# classTimes: a dictionary of ClassTime objects describing when class meetings take place; Keys are lowercase day identifiers (i.e. m, t, w, r, f)
# openSpots: the number of open spots in the class
# totalSpots: the total number of spots in the class
# coursePageLink: the url of the corresponding course page on Class Search

import src.API.ClassTime as ct
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

#Class to represent a section of a course at Notre Dame
class Class:

	#Constructor for Class object
	def __init__(self, name="", crn="0", courseNum = "", sectionNum = "", profName = "", classTimes={}, openSpots=0, totalSpots=0, coursePageLink=""):
		self.name = name
		self.crn = crn
		self.courseNum = courseNum
		self.sectionNum = sectionNum
		self.profName = profName
		self.openSpots = openSpots
		self.totalSpots = totalSpots
		self.coursePageLink = coursePageLink

		self.classTimes = {}
		self.addTimes(classTimes)
		logger.info("Creating Class instance for {}-{}...".format(courseNum, sectionNum))

	# Function to add times to the class
	# times is a dictionary with a letter representing the day as the key, and the ClassTime object as the value
	def addTimes(self, times):
		for day in times:
			self.classTimes[day.upper()] = times[day]
		logger.info("Adding times to {}-{}...".format(self.courseNum, self.sectionNum))

	# Function to determine if two classes conflict
	# Returns true if the classes conflict in their times, or if the two classes are from the same course
	def conflictsWith(self, otherClass):
		if self.courseNum == otherClass.courseNum:
			return True

		for day in self.classTimes:
			try:
				if self.classTimes[day].conflictsWith(otherClass.classTimes[day]):
					return True
			except KeyError:
				pass
		return False

	# Function to allow use of in operator when a Class object is in a container
	def __eq__(self, other):
		areSame = ((self.courseNum == other.courseNum) and (self.sectionNum == other.sectionNum))
		return areSame