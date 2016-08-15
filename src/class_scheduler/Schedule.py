# Schedule.py
# This class represents a class schedule containing Class objects and information about the schedule as a whole
# Member variables:
# classes: a list of Class objects that represent the classes in the schedule

from src.class_scheduler.ClassSchedulerJSONEncoder import JSONEncoderInterface

class Schedule(JSONEncoderInterface):

	# Constructor for Schedule object
	def __init__(self, classes=[]):
		self.classes = classes

	# Function to calculate the earliest start time during the week
	def calcEarliestStartTime(self):
		# Get start times for every class in the schedule
		startTimes = [x.classTimes.values() for x in self.classes]
		startTimes = [item for sublist in startTimes for item in sublist]
		startTimes = [x.startTime for x in startTimes]

		return min(startTimes)

	# Function to calculate the latest end time during the week
	def calcLatestEndTime(self):
		# Get end times for every class in the schedule
		endTimes = [x.classTimes.values() for x in self.classes]
		endTimes = [item for sublist in endTimes for item in sublist]
		endTimes = [x.endTime for x in endTimes]

		return max(endTimes)

	# Function to add a class to the schedule
	# Returns True if the class is successfully added, False otherwise
	def addClass(self, newClass):
		for section in self.classes:
			if newClass.conflictsWith(section):
				return False
		self.classes.append(newClass)
		return True

	# Remove the last class added to the schedule
	def removeLastClass(self):
		self.classes = self.classes[:-1]

	# Return the number of classes in the schedule
	def size(self):
		return len(self.classes)

	# Helper function to return the object in a JSON serializable format
	def _toJSON(self):
		return self.classes

	# Method to allow use of the "in" operator for classes in the schedule
	# Ex. if newClass in currentSchedule: now functions properly
	def __contains__(self, item):
		if item in self.classes:
			return True
		return False