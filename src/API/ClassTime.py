# ClassTime.py
# This class defines an object that represents the time of a class (as a span of time)
# member variables:
# startHour: hour from 0-23 representing the hour at which the class starts during the day
# startMin: minute (in range 0-59) in the hour at which the class starts
# endHour: hour from 0-23 representing the hour at which the class ends during the day
# endMin: minute (in range 0-59) in the hour at which the class ends

class ClassTime(object):

    # Constructor for ClassTime object
	def __init__(self, startHour=0, startMin=0, endHour=0, endMin=0):
		self.startHour = startHour
		self.startMin = startMin
		self.endHour = endHour
		self.endMin = endMin

	##### Public Facing Functions #####

	# Function to determine if two times conflict
	def conflictsWith(self, otherClassTime):
		startTime1 = ClassTimeStaticHelpers.convertTimeToMinutes(self.startHour, self.startMin)
		endTime1 = ClassTimeStaticHelpers.convertTimeToMinutes(self.endHour, self.endMin)
		startTime2 = ClassTimeStaticHelpers.convertTimeToMinutes(otherClassTime.startHour, otherClassTime.startMin)
		endTime2 = ClassTimeStaticHelpers.convertTimeToMinutes(otherClassTime.endHour, otherClassTime.endMin)

		beforeOtherClass = startTime1 < startTime2 and endTime1 < startTime2
		afterOtherClass = startTime1 > endTime2 and endTime1 > endTime2

		if (beforeOtherClass or afterOtherClass):
			return False
		else:
			return True


	##### Helper Functions #####

class ClassTimeStaticHelpers:
	# Helper function to return the startTime in minutes from the beginning of the day
	@staticmethod
	def convertTimeToMinutes(hour, minute):
		return (60 * hour) + minute