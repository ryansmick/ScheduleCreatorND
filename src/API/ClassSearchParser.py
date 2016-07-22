# ClassSearchParser.py
# This class is used to scrape Notre Dame's Class Search website to pull class information and organize it
# Class variables:
# url: the url of the Class Search page
# term: the term for which the user wishes to choose classes

from bs4 import BeautifulSoup
import requests
import re
import src.API.Class as Class
import src.API.ClassTime as ct
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class ClassSearchParser:
	classSearchURL = 'https://class-search.nd.edu/reg/srch/ClassSearchServlet'

	def __init__(self, term=None):
		logger.info("Creating ClassSearchParser instance...")
		self.term = term if term else self.__getMostRecentTerm()


	######Public facing functions#####


	#Retrieve table row in ClassSearch for each section of given class
	#The variable courseNumberString is the department identifier combined with the five-digit number (e.g. CSE30331)
	#Raises an AttributeError when the course number can't be parsed, or the department is invalid.
	# Returns an empty list if the specific course isn't found
	def getAllSectionsForCourse(self, courseNumberString):

		courseNumberString = ClassSearchParser.__sanitizeCourseNumber(courseNumberString)

		#Determine which department the course is in
		try:
			match = re.match('(\w{2,4})(\d{5})', courseNumberString)
			dept = match.group(1)
			num = match.group(2)
		except AttributeError as e:
			raise AttributeError("Invalid course number format for {}".format(courseNumberString)) from e

		try:
			table = self.__getClassSearchTable(dept)
		except AttributeError as e:
			raise e

		#Fill two dimensional array with info for each section of given class
		sectionsHTML = []
		for row in table.findAll('tr'):
			cells = row.findAll('td')
			if re.match(courseNumberString, cells[0].text):
				sectionsHTML.append(cells)

		#Create class objects for each class
		sections = []
		for section in sectionsHTML:
			courseName = section[1].text
			crn = section[7].text
			sectionNum = ClassSearchParser.__getSectionNumber(section[0].text)
			profName = ClassSearchParser.__sanitizeProf(section[9].text)
			classTimes = ClassSearchParser.__getClassTimes(section[10].text)
			openSpots = int(section[5].text)
			totalSpots = int(section[4].text)
			coursePageLink = self.__extractLinkToCoursePage(section[0])
			sections.append(Class.Class(courseName, crn, courseNumberString, sectionNum, profName, classTimes, openSpots, totalSpots, coursePageLink))

		logger.info("Returning all sections for {}...".format(courseNumberString))
		return sections

	# Function to get the corequisites for a specific course
	# classObject is an object of the Class class
	def getCorecInfo(self, classObject):
		try:
			courseNumber = classObject.courseNum
			url = classObject.coursePageLink
		except:
			return []

		response = requests.post(url)
		soup = BeautifulSoup(response.content, "html.parser")

		spans = soup.find('table', {'class':'datadisplaytable'}).find('td').findAll('span', {'class', 'fieldlabeltext'})
		for tag in spans:
			if tag.text == "Corequisites:":
				data = soup.find('table', {'class':'datadisplaytable'}).find('td').text
				pattern1 = re.compile('(Corequisites:.*?(Comments|Restrictions))', re.DOTALL)
				corecString = pattern1.findall(data)[0]
				pattern2 = re.compile('[a-zA-Z]{2,4} \d{5}')
				classSection = pattern2.findall(corecString[0])

				#Normalize each course number
				corecs = []
				for num in classSection:
					num = num.replace(" ", "")
					corecs.append(num)

				corecInfo = []
				for num in corecs:
					corecInfo.append(self.getAllSectionsForCourse(num))
				logger.debug("Corequisites of {}: {}".format(courseNumber, ", ".join(corecs)))
				logger.info("Returning info for corecs of {}...".format(courseNumber))
				return corecInfo
		return []


	######Internal Functions######


	#Function to get the most recent term available on ClassSearch
	@staticmethod
	def __sanitizeCourseNumber(courseNumber):
		# Remove all whitespace from courseNumber
		courseNumber = courseNumber.strip()
		courseNumber = courseNumber.replace(" ", "")

		# Make the course number uppercase
		courseNumber = courseNumber.upper()

		logger.debug("Returning sanitized course number: {}...".format(courseNumber))
		return courseNumber

	@classmethod
	def __getMostRecentTerm(cls):
		response = requests.post(cls.classSearchURL)
		soup = BeautifulSoup(response.content, "html.parser")

		#Find most recent term
		options = soup.find('select', {'name':'TERM'}).findAll('option')

		termNums = []
		for option in options:
			termNums.append(option['value'])

		logger.debug("Getting most recent term: {}...".format(termNums[0]))
		return termNums[0]

	# Returns a BeautifulSoup object containing the table from the Class Search site
	# Raises an AttributeError when an invalid department is given
	def __getClassSearchTable(self, department):

		# parsing parameters
		data = {
			'TERM': self.term,
			'DIVS': 'A',
			'CAMPUS': 'M',
			'SUBJ': department,
			'ATTR': '0ANY',
			'CREDIT': 'A'
		}

		# parsing data
		response = requests.post(self.classSearchURL, data=data)
		soup = BeautifulSoup(response.content, "html.parser")

		table = None
		try:
			table = soup.find('table', {'id':'resulttable'}).find('tbody')
		except AttributeError as e:
			logger.exception("Error: invalid department: ".format(department))
			raise AttributeError("Invalid department {}".format(department)) from e

		logger.debug("Returning Class Search table for the {} department...".format(department))
		return table

	#Take the entire course number field from Class Search and parse it to obtain the section number
	@staticmethod
	def __getSectionNumber(courseNumField):
		pattern = re.compile('\s\d{2}')
		classSection = pattern.findall(courseNumField)[0]
		return classSection[1:]

	#Converts a time in the Class Search format to a time in hours and minutes
	@staticmethod
	def __parseTime(time):
		hour = 0
		meridiem = time[-1]
		splitTime = time[:-1].split(':')
		splitTime = [int(splitTime[0]), int(splitTime[1])]
		minute = splitTime[1]

		if splitTime[0] == 12:
			if meridiem == "A":
				hour = 0
			else:
				hour = 12
		else:
			if meridiem == "A":
				hour = splitTime[0]
			else:
				hour = splitTime[0] + 12

		return (str(hour), str(minute))

	#Converts time from ClassSearch into a reasonable format
	#Returns a dictionary of ClassTime objects with one-letter keys representing the days of the week
	@staticmethod
	def __getClassTimes(timeString):
		timeString = re.sub('\s', '', timeString)

		#Account for possible multiple times
		timesList = re.compile("\(\d\)").split(timeString)
		if len(timesList) > 1:
			timesList=timesList[1:]

		#Convert each time in timesList to hours and minutes, then create a ClassTime object
		#and add it to the dictionary
		# Example time in timeString: 'MWF-10:30A-11:20A'
		classTimes = {}
		for time in timesList:
			splitTime = time.split("-")
			(startHour, startMin) = ClassSearchParser.__parseTime(splitTime[1])
			(endHour, endMin) = ClassSearchParser.__parseTime(splitTime[2])
			time = ct.ClassTime(int(startHour), int(startMin), int(endHour), int(endMin))
			for day in splitTime[0]:
				classTimes[day] = time

		return classTimes

	#Remove extraneous whitespace from professor field on ClassSearch
	@staticmethod
	def __sanitizeProf(profName):
		profName = profName.strip()
		profName = profName.replace("\n", "")
		return profName

	#Takes in the field on the main page of ClassSearch that contains the link to the class page, and returns the link
	@classmethod
	def __extractLinkToCoursePage(cls, linkField):
		elem = linkField.findAll('a')[0]
		pattern = re.compile("Servlet(\?[^']+)'")
		result = pattern.findall(str(elem))[0]
		result = result.replace('&amp;', '&')
		return cls.classSearchURL + result

if __name__ == '__main__':
	parser = ClassSearchParser()
	classes = parser.getAllSectionsForCourse("CSE 30331")