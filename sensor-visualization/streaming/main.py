from Visual import *
from Sensor import *

DEFAULT_SENSOR_TIMEOUT_MS = 100

def threads(callbackFunc, running, sensorTimeoutMs):
    sensor = Sensor(callbackFunc, running, sensorTimeoutMs)
    # Start threads
    sensor.start() # Run the thread to start collecting data

def main():
    #Set global flag
    event = threading.Event() # Create an event to communicate between threads
    event.set() # Set the event to True

    webVisual = Visual(threads, event, DEFAULT_SENSOR_TIMEOUT_MS)
    threads(webVisual, event, DEFAULT_SENSOR_TIMEOUT_MS)

main()