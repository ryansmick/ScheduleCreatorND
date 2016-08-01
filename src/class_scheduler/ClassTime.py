# ClassTime.py
# This module defines two classes (ClassTime and UndefinedClassTime) that are used to record the time at which a class
# takes place

import datetime as dt

# ClassTime
# This class defines an object that represents the time of a class (as a span of time)
# member variables:
# startTime: Time object representing the start of the class on a given day
# endTime: Time object representing the end of the class on a given day
# neverConflict: Boolean variable indicating whether the time can conflict with another time or not
class ClassTime(object):

	# Constructor for ClassTime object
	def __init__(self, startHour=0, startMin=0, endHour=0, endMin=0):
		self.startTime = dt.time(startHour, startMin)
		self.endTime = dt.time(endHour, endMin)
		self.neverConflict = False

	# Function to determine if two times conflict
	# Returns a boolean indicating whether the given time conflicts with the other time
	def conflictsWith(self, otherClassTime):
		if self.neverConflict or otherClassTime.neverConflict:
			return False

		beforeOtherClass = self.startTime < otherClassTime.startTime and self.endTime < otherClassTime.startTime
		afterOtherClass = self.startTime > otherClassTime.endTime and self.endTime > otherClassTime.endTime

		if (beforeOtherClass or afterOtherClass):
			return False
		else:
			return True

# UndefinedClassTime
# This class is used to indicate that a time for a given course has not been set
# This class extends ClassTime and does not introduce any new member variables
class UndefinedClassTime(ClassTime):
	def __init__(self):
		super().__init__()
		self.neverConflict = True

	# Function to determine if this class conflicts with another class
	# Always returns False because these times do not conflict with other class times
	def conflictsWith(self, otherClassTime):
		return False