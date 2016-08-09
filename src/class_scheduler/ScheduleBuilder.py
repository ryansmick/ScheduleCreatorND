# ScheduleBuilder.py
# This module contains a function to, given a list of course numbers, build a list of Schedule objects representing
# all possible schedules that can be taken with the given courses

from src.class_scheduler import Schedule, SectionList
import logging
import copy

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Return a tuple containing a list of Schedule objects representing all possible Schedules from the course numbers in the list,
# and a list of errors
def buildSchedules(parser, courseNumberList):
	# Given the list of courses, retrieve the corresponding Course objects and compile them
	# into a 2D list where each row represents a course, and columns are sections of each course

	# Remove duplicates
	courseNumberList = list(set(courseNumberList))
	errorsList = []

	# Build the two dimensional array of Class objects that will be used to create the schedules
	classArray2D = []
	coursesAdded = []
	logger.info("Gathering course information...")
	for courseNumberString in courseNumberList:
		# Get sections of given course
		sections = []
		try:
			sections = parser.getAllSectionsForCourse(courseNumberString)
		except ValueError as e:
			logger.exception(str(e))
			errorsList.append(str(e))
			continue
		if not sections:
			errorsList.append("Course {} not found".format(courseNumberString))
			continue

		# Check if the course exists in 2dClassArray
		# If not, add it
		if not sections[0].courseNum in coursesAdded:
			classArray2D.append(sections)
			coursesAdded.append(sections[0].courseNum)

		# Get the corecs for each course, and add them to the 2D class array if they aren't currently inside
		corecs = parser.getCorecInfo(sections[0])
		for corecSectionList in corecs:
			if not corecSectionList[0].courseNum in coursesAdded:
				classArray2D.append(corecSectionList)
				coursesAdded.append(corecSectionList[0].courseNum)

	if len(classArray2D) == 0:
		return ([], errorsList)

	# Call a helper function to build the schedules
	logger.info("Building schedules...")
	schedule = Schedule()
	scheduleList = []
	__buildSchedules(schedule, scheduleList, classArray2D)
	return (scheduleList, errorsList)

# Helper function for creating the list of Schedule objects
def __buildSchedules(currentSchedule, scheduleList, classSectionListNode):

	# Base Case: add the schedule to the schedule list, and return up the recursion tree
	if classSectionListNode is None:
		scheduleList.append(copy.deepcopy(currentSchedule))
		return

	# Recursive step: Walk through courses in current row, and if a course can be added to the schedule,
	# add it, add its corecs, and recurse
	for classSection in classSectionListNode.sections:
		if currentSchedule.addClass(classSection):
			if classSection.hasCorecs():
				__buildSchedulesWithCorecs(currentSchedule, scheduleList, classSectionListNode.nextCourse, classSection.corecs.head)
			else:
				__buildSchedules(currentSchedule, scheduleList, classSectionListNode.nextCourse)
			currentSchedule.removeLastClass()

# Helper function for adding corecs into the current schedule
def __buildSchedulesWithCorecs(currentSchedule, scheduleList, classSectionListNode, corecListNode):

	# Base case:
	if corecListNode is None:
		__buildSchedules(currentSchedule, scheduleList, classSectionListNode)
		return

	# Recursive step: walk through sections for this course and add one to the schedule
	for classSection in corecListNode.sections:
		if currentSchedule.addClass(classSection):
			__buildSchedulesWithCorecs(currentSchedule, scheduleList, classSectionListNode, corecListNode.nextCourse)
			currentSchedule.removeLastClass()

if __name__ == '__main__':
	from src.school_extensions.UniversityOfNotreDame.NDClassSearchParser import NDClassSearchParserWithCaching
	parser = NDClassSearchParserWithCaching()
	mainClassArray = SectionList()
	mainClassArray.insertSectionsForNewCourse("CSE30246", parser.getAllSectionsForCourse("CSE30246"))
	mainClassArray.insertSectionsForNewCourse("CSE20110", parser.getAllSectionsForCourse("CSE20110"))
	mainClassArray.tail.sections[0].addCorec("CSE30331", parser.getAllSectionsForCourse("CSE30331"))
	mainClassArray.tail.sections[1].addCorec("CSE30151", parser.getAllSectionsForCourse("CSE30151"))
	mainClassArray.insertSectionsForNewCourse("CSE20232", parser.getAllSectionsForCourse("CSE20232"))
	schedule = Schedule()
	scheduleList = []
	__buildSchedules(schedule, scheduleList, mainClassArray.head)
	print(scheduleList)
