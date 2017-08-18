class Payload(object):
	def __init__(self, payload_dict):
		super(Payload, self).__init__()
		self._type = payload_dict["type"]
		self._id = payload_dict["id"]
		self._data = payload_dict["data"]

	@property
	def type(self):
		return self._type

	@property
	def id(self):
		return self._id

	@property
	def data(self):
		return self._data
