from pyfingerprint.pyfingerprint import PyFingerprint
import pymysql
conn=pymysql.connect(host="--.--.--.--",
                               user="---",
                               passwd="---",
                               db="---")
                               
try: 
    f= PyFingerprint('/dev/ttyAMA0', 57600, 0xFFFFFFFF, 0x00000000)
    if (f.verifyPassword() == False ):
              raise ValueError('The given fingerprint sensor password is wrong!')
            
except Exception as e:
        print('The fingerprint sensor could not be initialized!')
        print('Exception message:' + str(e))
        exit(1)
        
try: 
    print('Waiting for finger...')
  
    while(f.readImage() == False ):
          pass
 
 ##converts read image to characteristics and stores it in charbuffer 1
    f.convertImage(0x01)
 #지문의 특성을 문자열 형태로 변환
    characterics = str(f.downloadCharacteristics(0x01)).encode('utf-8')
    cur= conn.cursor()
    #지문을 DB에 저장
    #2,3 번째 컬럼은 등급과 ID 저장을 위함
    sql= "insert inti finger_template values(%s, %s, %s)"
    cur.execute(sql,(characteristics, '2', 'number2'))
    conn.commit()
    
except Exception as e:
    print('Operation failed!')
    print('Execption message:' + str(e))
    exit(1)
    
    
finally:
    conn.close()
