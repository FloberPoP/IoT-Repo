from sense_hat import SenseHat
import time

# Initialize Sense HAT
sense = SenseHat()

def display_sensor_data():
    # Get sensor data
    temperature = sense.get_temperature()
    humidity = sense.get_humidity()
    pressure = sense.get_pressure()

    # Round the values for better display
    temperature = round(temperature, 1)
    humidity = round(humidity, 1)
    pressure = round(pressure, 1)

    # Create a message to display
    message = f'Temp: {temperature}C\nHumidity: {humidity}%\nPressure: {pressure}hPa'

    # Display the message on the Sense HAT
    sense.show_message(message, scroll_speed=0.05)

# Run the program in a loop
while True:
    display_sensor_data()
    time.sleep(5)  # Update every 5 seconds
