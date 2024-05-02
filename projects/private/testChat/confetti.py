from sense_hat import SenseHat
import random
import time

sense = SenseHat()

def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def confetti():
    for _ in range(100):
        x = random.randint(0, 7)
        y = random.randint(0, 7)
        color = random_color()
        sense.set_pixel(x, y, color)
        time.sleep(0.1)


confetti()
