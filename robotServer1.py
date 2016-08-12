import socket
import serial
import RPi.GPIO as GPIO
import time
 
HOST = ''
PORT = 9999
TRIG = 23
ECHO = 24

# Set GPIO mode
GPIO.setmode(GPIO.BCM)

# Open a socket.
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
sock.bind((HOST, PORT))
sock.listen(1)
print "Listening on port " + str(PORT)

# Open a serial connection to Roomba.
ser = serial.Serial(port='/dev/ttyUSB0', baudrate=115200)

def checkBehind():
   GPIO.setup(TRIG,GPIO.OUT)
   GPIO.setup(ECHO,GPIO.IN)

   GPIO.output(TRIG, False)
   print "Waiting For Sensor To Settle"
   time.sleep(2)

   GPIO.output(TRIG, True)
   time.sleep(0.00001)
   GPIO.output(TRIG, False)

   while GPIO.input(ECHO)==0:
     pulse_start = time.time()

   while GPIO.input(ECHO)==1:
     pulse_end = time.time()

   pulse_duration = pulse_end - pulse_start
   distance = pulse_duration * 17150
   distance = round(distance, 2)
   #print "Distance",distance
   if distance < 40:
      print "Distance",distance
      ser.write('\x8c\x01\x07\x43\x08\x40\x08\x3c\x16\x3c\x16\x3c\x16\x3e\x16\x40\x08\x8d\x01')
      #ser.write('\x91\x00\x96\x07\xD0')
      #ser.write('\x89\x00\x00\x00\x00')
      #ser.write('910a10a1')
      #ser.write('890000')

   GPIO.cleanup()

checkBehind()

# beging listening loop
try:
    while True: # wait for socket to connect
        conn, addr = sock.accept()
        print '%s:%s connected.' % addr
	
        while True:
            try:
                data = conn.recv(1024)
		#checkBehind()
            except Exception:
                print "Ran out of data."
                data = False
            if not data:
                break
            print len(data), data.encode("hex"),
            # do something with the data here
            ser.write(data)

        conn.close()
        print '%s:%s disconnected.' % addr
        
except Exception:
    sock.shutdown(socket.SHUT_RDWR)
    sock.close()
    ser.close()
    print "Goodbye."
