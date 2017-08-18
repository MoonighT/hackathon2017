class PayloadManager(object):
	def __init__(self):
		super(PayloadManager, self).__init__()
		self._payloads = []

	def create_payload_task(self, type, id):
		if not (type, id) in self._payloads:
			self._payloads.append((type, id))

	def has_payload_task(self, type, id):
		return (type, id) in self._payloads

	def remove_payload_task(self, type, id):
		if (type, id) in self._payloads:
			self._payloads.remove((type, id))