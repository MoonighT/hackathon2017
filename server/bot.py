from pymessenger import Bot


class BetterBot(Bot):
	def send_list(self, user_id, elements):
		payload = {
			'recipient': {
				'id': user_id
			},
			'message': {
				"attachment": {
					"type": "template",
					"payload": {
						"template_type": "list",
						"top_element_style": "compact",
						"elements": elements
					}
				}
			}
		}
		self.send_raw(payload)