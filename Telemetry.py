from core.base.model.Intent import Intent
from core.base.model.AliceSkill import AliceSkill
from core.dialog.model.DialogSession import DialogSession
from core.util.model.TelemetryType import TelemetryType
from core.util.Decorators import IntentHandler


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

		locations = self.LocationManager.getLocationsForSession(sess=session, slotName='Location')
		siteId = session.slotValue('Location', defaultValue=session.siteId)
		telemetryType = session.slotValue('TelemetryType')

		if not telemetryType:
			self.continueDialog(
				sessionId=session.sessionId,
				text=self.randomTalk('noType'),
				intentFilter=[Intent('AnswerTelemetryType')],
				slot='Alice/TelemetryType'
			)
			return

		if len(locations) != 1:
			self.continueDialog(
				sessionId=session.sessionId,
				text="What location?!", #self.randomTalk('noType'),
				intentFilter=[Intent('AnswerTelemetryType')],
				slot='Alice/TelemetryType'
			)
			return

		# siteId=locations[0].name,
		data = self.TelemetryManager.getData(ttype=TelemetryType(telemetryType), location=locations[0])

		if data and 'value' in data.keys():
			answer = f"{data['value']} {self._telemetryUnits.get(telemetryType, '')}"
			self.endDialog(sessionId=session.sessionId, text=self.randomTalk(text='answerInstant', replace=[answer]))
		else:
			self.endDialog(sessionId=session.sessionId, text=self.randomTalk('noData'))


	def dontAlertWhenSleeping(self, event: str) -> bool:
		"""
		Dont alert the user if they are sleeping unless overriden by the exception list
		:param event - telemetry event name such as "NoiseAlert"
		"""
		if self.UserManager.checkIfAllUser('sleeping'):
			if event not in self.getConfig('alertWhenSleeping'):
				return True
			else:
				return False
		else:
			return False
