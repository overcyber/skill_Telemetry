from core.base.model.AliceSkill import AliceSkill
from core.base.model.Intent import Intent
from core.dialog.model.DialogSession import DialogSession
from core.util.Decorators import IntentHandler
from core.util.model.TelemetryType import TelemetryType


class Telemetry(AliceSkill):
	"""
	Author: Psychokiller1888
	Description: Access your stored telemetry data
	"""

	def __init__(self):

		super().__init__()

		self._telemetryUnits = {
			'airQuality': '%',
			'co2': 'ppm',
			'gas': 'ppm',
			'gust_angle': '°',
			'gust_strength': 'km/h',
			'humidity': '%',
			'light': 'lux',
			'pressure': 'mb',
			'rain': 'mm',
			'temperature': '°C',
			'wind_angle': '°',
			'wind_strength': 'km/h'
		}


	@IntentHandler('GetTelemetryData')
	@IntentHandler('AnswerTelemetryType')
	def telemetryIntent(self, session: DialogSession):
		location = session.slotValue(slotName='Location')
		if not location:
			location = session.locationId
		else:
			locationObject = self.LocationManager.getLocation(locationName=location)
			if locationObject:
				location = locationObject.id
			else:
				self.endDialog(sessionId=session.sessionId, text=self.randomTalk('noData'))
				return

		telemetryType = session.slotValue('TelemetryType')

		if not telemetryType:
			self.continueDialog(
				sessionId=session.sessionId,
				text=self.randomTalk('noType'),
				intentFilter=[Intent('AnswerTelemetryType')],
				slot='Alice/TelemetryType'
			)
			return

		data = self.TelemetryManager.getData(ttype=TelemetryType(telemetryType), locationId=location)

		if data and 'value' in data[0].keys():
			finalData = data[0]
			answer = f"{finalData['value']} {self._telemetryUnits.get(telemetryType, '')}"
			self.endDialog(sessionId=session.sessionId, text=self.randomTalk(text='answerInstant', replace=[answer]))
		else:
			self.endDialog(sessionId=session.sessionId, text=self.randomTalk('noData'))


	def dontAlertWhenSleeping(self, event: str) -> bool:
		"""
		Don't alert the user if they are sleeping unless overridden by the exception list
		:param event - telemetry event name such as "NoiseAlert"
		"""
		if self.UserManager.checkIfAllUser('sleeping'):
			if event not in self.getConfig('alertWhenSleeping'):
				return True
			else:
				return False
		else:
			return False
