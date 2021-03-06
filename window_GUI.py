from pyfingerprint_pyfingerprint import PyFingerprint
drom tkinter import *
import pymysql
import time

    conn = pymysql.connect(host = "192.168.XX.XXX",
                                   user = "-------",
                                   password= "------",
                                   db = "------")
                                 
window = Tk()
window.title("fingerprint certification system")
window_width = 640
window_height = 600
window_geometry("640x600+50+50") # size, x,y
window.resizable(False, False)
mainFrame = Frame(window,relief = "solid", bd=0)
mainFrame.grid(row=0, column=0)
#화면에 글자출력을 위한 Canvas 생성
secu_Canvas = Canvas(mainFrame, width = window_width, height = window_height)
secu_Canvas.pack()

##센서 동작
try: 
    while True:
    
          f= PyFingerprint('/dev/ttyAMA0', 57600, 0xFFFFFFFF, 0x00000000)
          if (f.verifyPassword() == False ):
                    raise ValueError('The given fingerprint sensor password is wrong!')
              
              
           secu_Canvas.create_text(200, 100, text= "Waiting for finger...", font="Verdana 15 bold") 
           secu_Canvas.update()
           ##wait for finger read
           while(f.readImage() == False):
                  pass
           ## converts read image t0 charac and stors in charbuffer 1
           f.convertImage(0x01)
           cur = conn.cursor()
           sql = "select * from finger_template"
           cur.execute(sql)
           exist = False
           count = 1
           for row in cur.fetchall():
               f.uploadCharacteristics(0x02,eval(row[0]))
               score= f.compareCharacteristics()
               count = count + 1
               if score > 50:
                     exist = True
                      break
           conn.commit()
           secu_Canvas.delete(ALL)
           mainFrame.update()
           if exist:
           #등록된 지문이면 화면에 해당 지문 레벨 표시
                     secu_Canvass.create_text(200, 100, text = "access OK", font="Verdana 15 bold")
                     secu_Canvass.create_text(200, 100, text = "Level is" + str(row[1]), font="Verdana 15 bold")
                     secu_Canvas.update()
           else:
                     secu_Canvass.create_text(200, 100, text = "access Deny", font="Verdana 15 bold")
            
           secu_Canvas.update()
           time.sleep(3)
           secu_Canvas.delete(ALL)
           
except Exception as e:
      print('Operation failed!')
      print('Exception message:' + str(e))
      exit(1)
      
finally: 
      conn.close()
