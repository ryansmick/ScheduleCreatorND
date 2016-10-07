# ComplexJSONEncoder.py
# This module defines a subclass of JSONEncoder to encode the complex objects used in this package into JSON

import json
from abc import ABC, abstractmethod

# This class is used to represent objects in this package in JSON
# Call json.dumps(obj, cls=ClassSchedulerJSONEncoder) to properly encode objects into JSON
class ClassSchedulerJSONEncoder(json.JSONEncoder):
	def default(self, obj):
		if hasattr(obj, '_toJSON'):
			return obj._toJSON()
		else:
			return json.JSONEncoder.default(self, obj)

# This class is used as an interface that classes can extend which will allow them to be encoded as a JSON string
class JSONEncoderInterface(ABC):
	# Function to return a JSON string representing the given object
	def toJSON(self):
		return json.dumps(self._toJSON(), cls=ClassSchedulerJSONEncoder)

	@abstractmethod
	def _toJSON(self):
		raise NotImplementedError