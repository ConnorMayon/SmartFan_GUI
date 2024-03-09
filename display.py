import os
import time
while True:
	time.sleep(5)
	os.popen('bash backlight_off.sh')
	time.sleep(5)
	os.popen('bash backlight_on.sh')
	
