# ClassTime.py
# This class defines an object that represents the time of a class (as a span of time)
# member variables:
# startTime: Time object representing the start of the class on a given day
# endTime: Time object representing the end of the class on a given day

import datetime as dt

class ClassTime(object):

    # Constructor for ClassTime object
	def __init__(self, startHour=0, startMin=0, endHour=0, endMin=0):
		self.startTime = dt.time(startHour, startMin)
		self.endTime = dt.time(endHour, endMin)

	##### Public Facing Functions #####

	# Function to determine if two times conflict
	def conflictsWith(self, otherClassTime):

		beforeOtherClass = self.startTime < otherClassTime.startTime and self.endTime < otherClassTime.startTime
		afterOtherClass = self.startTime > otherClassTime.endTime and self.endTime > otherClassTime.endTime

		if (beforeOtherClass or afterOtherClass):
			return False
		else:
			return True