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
	classList = SectionList()
	coursesAdded = set()
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
		if sections[0].courseNum not in coursesAdded:
			classList.insertSectionsForNewCourse(sections[0].courseNum, sections)
			coursesAdded.add(sections[0].courseNum)
			# Add corecs of course to coursesAdded set to avoid repeats
			coursesAdded = coursesAdded.union(sections[0].corecs.courseNums)

	if classList.isEmpty():
		return ([], errorsList)

	# Call a helper function to build the schedules
	logger.info("Building schedules...")
	schedule = Schedule()
	scheduleList = []
	__buildSchedules(schedule, scheduleList, classList.head)
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
