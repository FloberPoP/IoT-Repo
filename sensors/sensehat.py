from sense_hat import SenseHat

def read_sensehat_data():
    sense = SenseHat()

    temperature = sense.get_temperature()
    humidity = sense.get_humidity()
    pressure = sense.get_pressure()
    
    return {"temperature": temperature, "humidity": humidity, "pressure": pressure}