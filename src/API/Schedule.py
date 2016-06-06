# Schedule.py
# This class represents a class schedule containing Class objects and information about the schedule as a whole
# Member variables:
# classes: a list of Class objects that represent the classes in the schedule

import src.API.ClassTime as ct
import src.API.Class as Class
import datetime as dt

class Schedule(object):

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