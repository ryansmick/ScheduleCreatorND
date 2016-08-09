# NDClass.py
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

from src.class_scheduler import Class
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

#Class to represent a section of a course at Notre Dame
class NDClass(Class):

	#Constructor for Class object
	def __init__(self, name, courseNum, sectionNum, classTimes, crn="00000", profName = "", openSpots=0, totalSpots=0, coursePageLink=""):
		super().__init__(name, courseNum, sectionNum, classTimes)
		self.crn = crn
		self.profName = profName
		self.openSpots = openSpots
		self.totalSpots = totalSpots
		self.coursePageLink = coursePageLink
		logger.info("Creating Class instance for {}-{}...".format(courseNum, sectionNum))

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