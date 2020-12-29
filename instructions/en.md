# Telemetry skill

## General operation

The telemetry skill recieves your telemtry data from configured sensors and stores those values in the database. When
this skill recieves new data Alice will alert you if the incoming data exceeds or equals the values you have set in the
skill settings.

## Configuration

Configuration is simple. Go to the skill settings and adjust the values in the list to your desired alert values

- EG: You want to be alerted if temperature equals or exceeds 40c..
	- Set "TemperatureAlertHigh" to value of 40

## Exclude list while sleeping

When Alice knows your sleeping (because you've said good night to her) she will not alert you at silly oclock in the
morning if for example, the humidity reading inside is at the high value.

However you can bypass that and get alerted despite being in sleep mode by adding the event you want alerted to in the "
alertWhenSleeping" field found in the skill settings

The format is comma seperated strings.

Example:

- TemperatureAlertHigh, CO2AlertHigh, GasAlertHigh

In this above example you will get alerted while sleeping for high readings of Temperature, CO2 and Gas readings but not
alerted for Humidty, wind, rain etc.
