I had to make a new Repository because the last on got corrupted
Project is on Branch: Master
Documents on Branch: Main

Please make the following adjustments to test the system:

1. Update the recipient_email address in the email handler with a new one.
2. Modify the Firebase handler since pushing the ServiceAccountKey file to GitHub poses security risks.

Note: Temporary internet outages may cause errors due to disruptions in the Firebase and Blynk connections.


The system includes a controller that operates three separate threads:

Motion Detection Thread (Thread 1): 
This thread detects motion, sends a message to the broker, and temporarily stores the image on the Raspberry Pi (RPI).

Data Thread (Thread 2): 
This thread refreshes data on the Blynk app every 10 seconds and checks for new messages from the broker. If motion is detected, the image is uploaded to a Firebase database, and both the image and current sensor data are emailed.

Controller Thread (Thread 3): 
This thread monitors for control inputs via the Blynk app, such as button presses. When activated, it captures an image and emails it along with the current sensor data.