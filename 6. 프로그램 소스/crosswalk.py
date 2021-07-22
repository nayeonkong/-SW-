import RPi.GPIO as GPIO
import pygame
import time
import I2C_LCD_driver
from pirc522 import RFID 

mylcd = I2C_LCD_driver.lcd() #I2C_LCD 사용을 위한 드라이버

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD) 

led1=36 #횡단보도 Red
led2=38 #횡단보도 Green

R_LED=35 #차량 신호등 Red
Y_LED=33 #차량 신호등 Yellow
G_LED=31 #차량 신호등 Green

led_bar_G = 16 # 횡단보도 Green led bar
led_bar_R = 12 # 횡단보도 Red led bar

GPIO.setup(led1, GPIO.OUT) #횡단보도 LED 출력모드 설정
GPIO.setup(led2, GPIO.OUT)

GPIO.setup(R_LED, GPIO.OUT) #차량 신호등 LED 출력모드 설정
GPIO.setup(Y_LED,GPIO.OUT)
GPIO.setup(G_LED,GPIO.OUT)

GPIO.setup(led_bar_G, GPIO.OUT) #횡단보도 LED bar 출력모드 설
GPIO.setup(led_bar_R, GPIO.OUT)


s1 = 40 # 서보 모터

GPIO.setup(s1, GPIO.OUT)

Pin = 37 # 모션 감지
GPIO.setup(Pin, GPIO.IN) # 모션 감지 입력모드 설정

p=GPIO.PWM(s1, 50)
p.start(3)

RFID_UID = [81, 134, 135, 46, 126] # 등록된 카드 UID
rc522 = RFID()

pygame.mixer.init()
RV=pygame.mixer.Sound("/home/pi/Desktop/redlight.wav")
GV=pygame.mixer.Sound("/home/pi/Desktop/greenlight.wav")
MV=pygame.mixer.Sound("/home/pi/Desktop/ee.wav")


b = True
c = True

while True:
    if b == False: # 횡단보도 -> 초록불
        GPIO.output(R_LED, GPIO.LOW) 
        GPIO.output(Y_LED, GPIO.HIGH)  # 차량 신호등 -> 노란불 2초간 출력
        GPIO.output(G_LED, GPIO.LOW)
        time.sleep(2)
        GPIO.output(led1, False) 
        GPIO.output(led2, True)
        GPIO.output(led_bar_G, GPIO.HIGH) # Green led bar ON
        GPIO.output(led_bar_R, GPIO.LOW) # Red led bar OFF
        time.sleep(0.5)
        GPIO.output(R_LED, GPIO.HIGH) #차량 신호등 -> 빨간불
        GPIO.output(Y_LED, GPIO.LOW)
        GPIO.output(G_LED, GPIO.LOW)
        GV.play() #음성 플레이
        p.ChangeDutyCycle(7.5) #정지선 바리게이트
        time.sleep(0.5)
        a=5
        while True:
            rc522.wait_for_tag()  #RFID 인식
            (error, tag_type) = rc522.request()
    
            if not error :
                
                (error, uid) = rc522.anticoll()  
                if not error :
                    if RFID_UID == uid : # 등록된 카드일 경우
                        print('Registered {} card !'.format(uid)) 
                        a = a + 3 # 3초 연장
                        mylcd.lcd_display_string(" Registered card ",1) #I2C_LCD 시간초 출력
                        mylcd.lcd_display_string("     + 3 sec     ",2)
                        time.sleep(2)
                           
                    else :
                        print('Unregistered {} card !'.format(uid))
                        
                    time.sleep(1) 
                for i in range(a): # a초간 I2C_LCD에 시간초 출력
                    x=str(a)  
                    mylcd.lcd_display_string("   GREEN LIGHT   ",1)
                    mylcd.lcd_display_string("       "+x+"     ",2)
                    time.sleep(1) 
                    mylcd.lcd_clear()
                    a=a-1
                if a == 0:
                    break

            if b == False: # 카드 인식이 필요 없는 경우
                for i in range(a):  # a초간 I2C_LCD에 시간초 출력
                    x=str(a)  
                    mylcd.lcd_display_string("   GREEN LIGHT   ",1)
                    mylcd.lcd_display_string("       "+x+"     ",2)
                    time.sleep(1) 
                    mylcd.lcd_clear()
                    a=a-1
                if a == 0:
                    break
            
        time.sleep(0.5)
        b = True # 초록불 -> 빨간불

    if b == True: # 횡단보도 -> 빨간불
        GPIO.output(led1, True) 
        GPIO.output(led2, False)
        GPIO.output(led_bar_R, GPIO.HIGH) # Red led bar ON
        GPIO.output(led_bar_G, GPIO.LOW) # Green led bar OFF
        time.sleep(0.5)
        GPIO.output(R_LED, GPIO.LOW)
        GPIO.output(Y_LED, GPIO.LOW)
        GPIO.output(G_LED, GPIO.HIGH)  # 차량 신호등 -> 초록불
        RV.play() # 음성 플레이
        p.ChangeDutyCycle(3) # 바리게이트 치우기
        #print("RED")
        time.sleep(0.5)    
        time.sleep(5)
        b = False

    if GPIO.input(led1) == True: #횡단도보 빨간불? -> 사람이 감지되면? -> 음성&디스플레이 안내                                        
        if GPIO.input(Pin) == True:# I2C_LCD, MOTION, SOUND
            print("Motion detected!")  
            if c == True:
                for i in range(1): 
                    mylcd.lcd_display_string("    RED LIGHT    ",1)
                    mylcd.lcd_display_string("please step back!",2)            
                    MV.play()
                    time.sleep(5)
                    mylcd.lcd_clear()
                    c==False
            time.sleep(0.05)
        else:
            print ("No motiom")
            time.sleep(0.05)
            
        time.sleep(2)
