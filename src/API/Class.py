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
# coursePageLink: the url of the corresponding course page on Class Search

import ClassTime as ct

#Class to represent a section of a course at Notre Dame
class Class:

	#Constructor for Class object
	def __init__(self, name="", crn=0, courseNum = "", sectionNum = "", profName = "", classTimes={}, openSpots=0, coursePageLink=""):
		self.name = name
		self.crn = crn
		self.courseNum = courseNum
		self.sectionNum = sectionNum
		self.profName = profName
		self.openSpots = openSpots
		self.coursePageLink = coursePageLink

		self.classTimes = {}
		self.addTimes(classTimes)


	# Function to add times to the class
	def addTimes(self, times):
		for day in times:
			self.classTimes[day.lower()] = times[day]

	# Function to determine if two classes conflict
	def conflictsWith(self, otherClass):
		for day in self.classTimes:
			if self.classTimes[day].conflictsWith(otherClass.classTimes[day]):
				return True
		return False