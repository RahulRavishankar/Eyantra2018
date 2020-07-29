import serial
import time
if __name__ == "__main__":
    ser = serial.Serial("COM5", 9600, timeout=None) #timeout=0.005
    while True:
        user_input = input("Enter key: ")
        ########## ENTER YOUR CODE HERE ############
        #s=ser.read(50)
        ser.write(user_input.encode('utf-8'))


        print(ser.read(50))
        ser.close()
        ############################################
                  
