# ScheduleBuilder.py
# This module contains a function to, given a list of course numbers, build a list of Schedule objects representing
# all possible schedules that can be taken with the given courses

import src.API.ClassSearchParser as CSP
import src.API.Schedule as Schedule
import logging
import copy

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Return a tuple containing a list of Schedule objects representing all possible Schedules from the course numbers in the list, and a list of errors
def buildSchedules(courseNumberList):
	# Given the list of courses, retrieve the corresponding Course objects and compile them
	# into a 2D list where each row represents a course, and columns are sections of each course

	# Remove duplicates
	courseNumberList = list(set(courseNumberList))
	errorsList = []

	# Build the two dimensional array of Class objects that will be used to create the schedules
	classArray2D = []
	parser = CSP.ClassSearchParser()
	coursesAdded = []
	logger.info("Gathering course information...")
	for courseNumberString in courseNumberList:
		# Get sections of given course
		sections = []
		try:
			sections = parser.getAllSectionsForCourse(courseNumberString)
		except AttributeError as e:
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
	schedule = Schedule.Schedule()
	scheduleList = []
	__buildSchedules(schedule, scheduleList, classArray2D)
	return (scheduleList, errorsList)

# Helper function for creating the list of Schedule objects
def __buildSchedules(currentSchedule, scheduleList, classArray2D):
	row = currentSchedule.size()

	# Base Case: add the schedule to the schedule list, and return up the recursion tree
	if row >= len(classArray2D):
		scheduleList.append(copy.deepcopy(currentSchedule))
		return

	# Recursive step: Walk through courses in current row, and if a course can be added to the schedule,
	# add it and recurse
	for classSection in classArray2D[row]:
		if currentSchedule.addClass(classSection):
			__buildSchedules(currentSchedule, scheduleList, classArray2D)
			currentSchedule.removeLastClass()

if __name__ == '__main__':
	schedules = buildSchedules(["asdfads", "asdfa"])
	print(schedules)