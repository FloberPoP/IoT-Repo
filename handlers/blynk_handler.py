import BlynkLib

BLYNK_AUTH = 'MRsKDiiQJEaKivtQhmU-jFIUH-HtDWxE'
blynk = BlynkLib.Blynk(BLYNK_AUTH)

button_pressed = False

def set_event(data):
    blynk.run()
    blynk.virtual_write(1, round(data['temperature'], 2))
    blynk.virtual_write(2, round(data['humidity'], 2))
    blynk.virtual_write(3, round(data['pressure'], 2))

def set_motion(image_url):
    blynk.run()
    print("URL Picture: "+image_url)
    blynk.set_property(4, "url", 0, image_url)
    blynk.virtual_write(4, 0)
    blynk.log_event("motion","Attention Motion Detected '" + image_url + "'")
    

@blynk.on("V5")
def my_button_handler(value):
    global button_pressed
    if int(value[0]) == 1 and button_pressed == False:
        button_pressed = True

def check_button_press():
    blynk.run()
    global button_pressed
    if button_pressed:
        button_pressed = False 
        return True
    return False