# SectionList
# This class defines a data structure to hold and organize sections of classes in a manner that facilitates
# the creation of schedules
# The class essentially defines a linked list of vectors (Python "lists")
# Each node in the linked list represents a course, and each node holds a vector of Class objects
# Member variables:
# head: the beginning of the linked list
# tail: the end of the linked list
# courseNums: a set of strings representing course numbers that are present in the SectionList

# Inner Class: SectionListNode
# Keeps track of the section data
# Member variables:
# sections: a vector (Python list) of Class objects for a given course
# nextCourse: a SectionList instance representing another course

class SectionList(object):

	class SectionListNode(object):
		# Constructor for SectionListNode
		# Accepts a Python list of Class objects for the same course as a parameter
		# The above condition is not enforced. The programmer must ensure all Class objects are for same course
		def __init__(self, sectionList):
			self.sections = sectionList
			self.nextCourse = None

	# Constructor for SectionList
	def __init__(self):
		self.head = None
		self.tail = None
		self.courseNums = set()

	# Function to add a new course to the linked list
	# sections is a python list of Class objects from the same course
	def insertSectionsForNewCourse(self, courseNum, sections):
		if (courseNum in self.courseNums) or (not sections):
			return
		else:
			self.courseNums.add(courseNum)
		node = SectionList.SectionListNode(sections)
		if self.head is None:
			self.head = node
			self.tail = node
		else:
			self.tail.nextCourse = node
			self.tail = node

	# Function that returns true if there are no courses that are listed as corecs for this class
	def isEmpty(self):
		return self.head is None

	# Overrides python __contains__ function
	# Used to determine if a given course already exists in the SectionList
	def __contains__(self, courseNum):
		return courseNum in self.courseNums