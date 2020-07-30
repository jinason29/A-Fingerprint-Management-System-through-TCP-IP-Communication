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
    cur= conn.cursor()
    sql = "select * from finger_template"
    # finger template 이름의 table
    cur. execute(sql)
    for row in cur.fetchall():
        print(f.uploadCharacteristics(0x02, eval(row[0])))
        score-f.compareCharacteristics()
        print(score)  ##두 지문간 특성을 비교하여 유사도를 정수형으로 score 변수에 저장
    
execpt Execption as e:
    print('Operation failed!')
    print('Execption message:' + str(e))
    exit(1)
    
finally:
    conn.close()
