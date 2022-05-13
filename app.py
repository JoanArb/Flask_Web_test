
#La informació sobre la parte del Daily Motions está en el vídeo...  https://www.youtube.com/watch?v=X5E2SXOsr4E
#La información sobre la base de datos está en el vídeo... https://www.youtube.com/watch?v=IgCfZkR8wME
#Se utiliza la web https://bootswatch.com/
#Se utiliza la web https://getbootstrap.com/
#se utiliza la web https://uigradients.com/

from distutils.command.clean import clean
from fileinput import filename
from operator import pos
from turtle import begin_fill, clear, tiltangle, title
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, make_response
import requests
from flaskext.mysql import MySQL
# importing the module 
import pytube
from pytube import YouTube 
import numpy as np
import cv2 #VScode press Ctrl+Shift+P and then type "Python: Select Interpreter" then select your python Interpreter and Run it again.

#from tkinter import filedialog as FileDialog

from turtle import textinput
from datetime import datetime

#----------------------------------- Cairocoders ------------------------------------- 
#-------------------------------------------------------------------------------------
import os
from werkzeug.utils import secure_filename
#----------------------------------------------------------------------------------------
#----------------------------------- fi de Cairocoders ----------------------------------

from moviepy.editor import *
#from moviepy.editor import VideoFileClip

from tkinter import filedialog as FileDialog, messagebox

def test():
    fichero = FileDialog.asksaveasfile(
        title="Guardar un fichero", mode='w', defaultextension=".txt")

    if fichero is not None:
        fichero.write("Hola!")
        fichero.close()

def testsave():
    ruta = FileDialog.asksaveasfile(title="Guardar un fichero")
    #(ficherosave )


mysql = MySQL()
#app=Flask(__name__,template_folder='templates')
app = Flask(__name__)
app.config['MYSQL_DATABASE_HOST'] = 'localhost' 
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '' #si no hay ningún password debe estar vacío 
app.config['MYSQL_DATABASE_DB'] = 'salsa'
mysql.init_app(app)

#settings... es necesario iniciar una sesión para que funcione la base de datos:
app.secret_key = 'mysecretkey' #es para decirle como va ir protegida nuestra sesión.

dir_descargas = "c:/users/ideas/downloads/"

figura_total = [] #iniciación de la figura, el begin, el end,... que se está creando
solo_figura_total = [] #iniciación de la figura que se está creando
dancers_analizado = False #esta variable indica si ya se ha buscado (se ha pulsado la opción dancers) qué dancers hay actualmente 
bailarines_select = ['All_dancers'] #esta variable indica qué dancers juegan, siempre y cuando all_dancers sea False
bailarines = [] #bailarines es la matriz que indica los diferentes bailarines que hay en la tabla movements
bailarinas = [] #bailarinas es la matriz que indica las diferentes bailarinas que hay en la tabla movements
todos_bailarines = True #indica si se han elegido todos los bailarines (True) o no (False)
new_mov = ['','','','','','','','','','','','','','','']
social_workshop = 'social' 
log_in = False #indica si el usuario ha hecho el log in... inicializamos a false
log_in_name = 'Mi_cuenta'


#lista_positions = ['010501000000.png', '010502000000.png', '010502000002.png', '010503000000.png', '010506000000.png',
#    '010507000000.png', '010500000025.png', '010500000006.png', '010501160000.png', '010508000000.png', '010509000000.png',
#    '010504000000.png', '010505000000.png', '010509000010.png', '010503000026.png', '010505000300.png', '010502060000.png',
#    '010504060000.png', '010506060000.png', '010508060000.png', '010501050000.png', '010505050000.png', '010508090000.png',
#    '010508050000.png', '010508050013.png', '010504110000.png', '010511110000.png', '010504000500.png', '010507000500.png',
#    '010504070005.png', '010504070028.png', '010505080009.png', '010508080003.png', '010308170003.png',    
#    '020100000029.png', '020107000007.png', '020107000002.png', '020106000005.png', '020108000005.png', '020107010000.png',
#    '020108010000.png', '020101010000.png', '020102000007.png', '020103130000.png', '020104060000.png', '020104120000.png',
#    '020105080000.png', '020105120000.png', '020108100003.png', 
#    '020109060004.png',    
#    '020201000000.png', '020206000000.png', '020206001000.png', '020207000000.png', '020210000000.png', '020204001000.png', 
#    '020204000000.png', '020205000000.png', '020211000000.png', '020211000700.png', '020208001100.png', '020204000800.png',
#    '020204001300.png',       
#    '020405000000.png',
#    '030700000002.png', '030704060400.png', 
#   '030802000308.png', '030802000500.png', '030803000500.png', '030805050700.png', '030807000502.png', '030810000000.png',
#    '030811000500.png', '030811080500.png',
#   '040705000600.png', 
#    '040800000002.png', '040801070005.png', '040805050000.png', '040807000302.png', '040806000027.png',
#    '010606020000.png', '010608001500.png',
#    '011005050700.png']

#lista_positions = ['010500000000.png', '010501000000.png', '010502000000.png', '010502000002.png', '010503000000.png', '010506000000.png', '010507000000.png', '010500000025.png', '010500000006.png', '010500000007.png', '010501160000.png', '010508000000.png', '010509000000.png', '010504000000.png', '010505000000.png', '010509000010.png', '010503000026.png', '010505000300.png', '010502060000.png', '010504060000.png', '010506060000.png', '010508060000.png', '010501050000.png', '010505050000.png', '010508090000.png', '010508050000.png', '010507050000.png', '010508050013.png', '010504110000.png', '010511110000.png', '010508000500.png', '010504000500.png', '010507000500.png', '010505010007.png', '010504070005.png', '010504080009.png', '010504070028.png', '010505080009.png', '010508080003.png', '010308170003.png', '010500000031.png', '010502000031.png', '010506000014.png', '020100000017.png', '020100000029.png', '020100000013.png', '020107000007.png', '020107000002.png', '020106000005.png', '020106000009.png', '020108000005.png', '020107010000.png', '020108010000.png', '020101010000.png', '020102000007.png', '020103130000.png', '020104060000.png', '020104120000.png', '020105080000.png', '020105120000.png', '020108100003.png', '020109060004.png', '020201000000.png', '020202000000.png', '020206000000.png', '020206001000.png', '020207000000.png', '020210000000.png', '020204001000.png', '020204000000.png', '020205000000.png', '020211000000.png', '020211000700.png', '020208001100.png', '020204000800.png', '020204000900.png', '020204001300.png', '020300000015.png', '020300000018.png', '020405000000.png', '030700000002.png', '030704060400.png', '030802000308.png', '030802000500.png', '030803000500.png', '030805050700.png', '030807000502.png', '030810000000.png', '030811000500.png', '030811080500.png', '040705000600.png', '040800000002.png', '040804010002.png', '040800000030.png', '040801070005.png', '040805050000.png', '040807000302.png', '040806000027.png', '010606020000.png', '010608001500.png', '011005050700.png']

lista_positions = ['010500000000.png', '010501000000.png', '010502000000.png', '010502000002.png', '010503000000.png',
    '010506000000.png', '010507000000.png', '010500000025.png', '010500000006.png', '010500000007.png', '010501160000.png',
    '010508000000.png', '010509000000.png', '010504000000.png', '010505000000.png', '010509000010.png', '010503000026.png',
    '010505000300.png', '010502060000.png', '010504060000.png', '010506060000.png', '010508060000.png', '010501050000.png',
    '010505050000.png', '010508090000.png', '010508050000.png', '010507050000.png', '010508050013.png', '010504110000.png',
    '010511110000.png', '010508000500.png', '010504000500.png', '010507000500.png', '010505010007.png', '010504070005.png',
    '010504080009.png', '010504070028.png', '010505080009.png', '010508080003.png', '010308170003.png', '010500000031.png',
    '010502000031.png', '010506000014.png', '020100000017.png', '020100000029.png', '020100000013.png', '020107000007.png',
    '020107000002.png', '020106000005.png', '020106000009.png', '020108000005.png', '020107010000.png', '020108010000.png',
    '020101010000.png', '020102000007.png', '020103130000.png', '020104060000.png', '020104120000.png', '020105080000.png',
    '020105120000.png', '020108100003.png', '020109060004.png', '020201000000.png', '020202000000.png', '020206000000.png',
    '020206001000.png', '020207000000.png', '020210000000.png', '020204001000.png', '020204000000.png', '020205000000.png',
    '020211000000.png', '020211000700.png', '020208001100.png', '020204000800.png', '020204000900.png', '020204001300.png',
    '020300000015.png', '020300000018.png', '020405000000.png', '030700000002.png', '030704060400.png', '030802000308.png',
    '030802000500.png', '030803000500.png', '030805050700.png', '030807000502.png', '030810000000.png', '030811000500.png',
    '030811080500.png', '040705000600.png', '040800000002.png', '040804010002.png', '040800000030.png', '040801070005.png',
    '040805050000.png', '040807000302.png', '040806000027.png', '010606020000.png', '010608001500.png', '011005050700.png']


#---------------------------------------------------------------------------------------
#--------------------------------- Empiezan funciones (def) ---------------------------------
#---------------------------------------------------------------------------------------

def clean_list(): #función para borrar la lista de la variable global figura_total
    figura_total.clear()
    solo_figura_total.clear()

def Insertar_movimiento_nuevo_DataBase(nou):
    conn = mysql.connect()
    cursor = conn.cursor()
    print(nou[0])
    print(nou[1])
    print(nou[2])
    print(nou[13])

    sql = "INSERT INTO movements (name,title,begin,end,dancer_m,dancer_f,i_dancer_m,i_dancer_f,social,place,i_place,orig_video,web_video,i_web_video,sec_video) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    #sql = "INSERT INTO movements (name,title,begin,end) VALUES (%s, %s, %s, %s)"
    val = (str(nou[0]),str(nou[1]),str(nou[2]),str(nou[3]),str(nou[5]),str(nou[4]),str(nou[7]),str(nou[6]),str(nou[13]),str(nou[8]),str(nou[9]),str(nou[10]),str(nou[11]),str(nou[12]),str(nou[14]))

    #val = (str(nou[0]),str(nou[1]),str(nou[2]),str(nou[3]))
    cursor.execute(sql, val)
    conn.commit()

    sql = "INSERT INTO basic (name,title,begin,end,dancer_m,dancer_f,social) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = (str(nou[0]),str(nou[1]),str(nou[2]),str(nou[3]),str(nou[5]),str(nou[4]),str(nou[13]))
    cursor.execute(sql, val) 
    conn.commit()  
    
    flash('Movement added successfully')

    #cursor.execute("""INSERT INTO movements (name,title,begin,end,dancer_m,dancer_f,i_dancer_m,i_dancer_f,social,place,
    #    i_place,orig_video,web_video,i_web_video,del_date) 
    #    VALUES (str(nou[0]),str(nou[1]),str(nou[2]),str(nou[3]) ,str(nou[5]),str(nou[4]),str(nou[7]),str(nou[6]),str(nou[13]),
    #    str(nou[8]),str(nou[9]),str(nou[10]),str(nou[11]),str(nou[12])""")

    #cursor.execute("""INSERT INTO movements (name,title,begin) VALUES ('maria','esther','Itziar')""")

    #data = cursor.fetchall()
    #last = data[len(data)-1]
    #global new_mov
    #new_mov[12] = last[14]
    #print(last)
    #print(new_mov)

def Buscar_info_web(web):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM movements WHERE web_video = %s', (web))
    data = cursor.fetchall()
    last = data[len(data)-1]
    global new_mov
    new_mov[12] = last[14]
    print(last)
    print(new_mov)

def Buscar_info_location(local):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM movements WHERE place = %s', (local))
    data = cursor.fetchall()
    last = data[len(data)-1]
    global new_mov
    new_mov[9] = last[11]
    print(last)
    print(new_mov)

def Buscar_info_dancers(ballari,ballarina):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM movements WHERE dancer_m = %s', (ballari))
    data = cursor.fetchall()
    last = data[len(data)-1]
    global new_mov
    new_mov[7] = last[7]
    print(last)
    print(new_mov)

    cursor.execute('SELECT * FROM movements WHERE dancer_f = %s', (ballarina))
    data = cursor.fetchall()
    last = data[len(data)-1]
    new_mov[6] = last[8]
    print(last)
    print(new_mov)

def crear_lista_dancers():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT(dancer_m) FROM movements')
    data = cursor.fetchall()
    #print(data)

    global bailarines
    global bailarinas

    bailarines = []
    i = 0
    for dato in data:
        bailarin = data[i][0] #NOTA: fijarse que es data[i][0] no dato[i][0] 
        i = i + 1
        #print(bailarin)
        if bailarin == '':
            bailarin = 'Others'
        bailarines.append(bailarin)
    print(bailarines)

    cursor.execute('SELECT DISTINCT(dancer_f) FROM movements')
    data = cursor.fetchall()
    #print(data)
    bailarinas = []
    i = 0
    for dato in data:
        bailarina = data[i][0] #NOTA: fijarse que es data[i][0] no dato[i][0] 
        i = i + 1
        #print(bailarina)
        if bailarina == '':
            bailarina = 'Others'
        bailarinas.append(bailarina)
    print(bailarinas)

def contar_videos_position(lista):
    conn = mysql.connect()
    cursor = conn.cursor()
    num_mov = []
    #print(lista)
    
    for mov_begin in lista:
        basename = os.path.basename(mov_begin)
        file_name = os.path.splitext(basename)[0]
        #print(file_name)
        #print (mov_begin)
        cursor.execute('SELECT COUNT(*) FROM movements WHERE begin = %s', (file_name)) #formatear el id como un string 
        data = cursor.fetchall()
        #print(data[0][0])
        num_mov.append(data[0][0])
    print(lista)
    #print(num_mov)
    return num_mov

def contar_videos_position_dancers(posiciones,bailarines): #cuántos videos hay que COMIENCEN con una determinada posición
    conn = mysql.connect()
    cursor = conn.cursor()
    num_mov = []
    print(posiciones)
    print(bailarines)
    
    for mov_begin in posiciones:
        basename = os.path.basename(mov_begin)
        file_name = os.path.splitext(basename)[0]
        #print(file_name)
        #print (mov_begin)

        #se tiene que añadir una coma ',' para evitar problemas cuando sólo se elige un dancer... el problema es la función tuple()
        bailarines_select_fake = bailarines
        if len(bailarines) == 1:
            if bailarines[0] != 'All_dancers':
                #bailarines_select_fake.append("jghkrgj")
                bailarines_select_fake.append(",")  #añadimos una coma ','
        mytuple = tuple(bailarines_select_fake)
        print(bailarines_select_fake)
        print(bailarines)
        #mytuple = tuple(bailarines_select)
        #print(bailarines_select)
        print("estic a contar_videos_position_dancers")

        for sel in bailarines_select:
            if sel == 'All_dancers':
                cursor.execute('SELECT COUNT(*) FROM movements WHERE begin = ' + str(file_name))
            else:
                cursor.execute('SELECT COUNT(*) FROM movements WHERE begin = '+ str(file_name)+' AND ((dancer_m  IN '+str(mytuple)+')'+' OR (dancer_f IN '+str(mytuple)+'))')
        data = cursor.fetchall()
        num_mov.append(data[0][0])
    print(posiciones)
    #print(num_mov)
    return num_mov

def contar_videos_position_dancers_end(posiciones,bailarines): #cuántos videos hay que ACABEN con una determinada posición
    conn = mysql.connect()
    cursor = conn.cursor()
    num_mov = []
    print(posiciones)
    print(bailarines)
    
    for mov_end in posiciones:
        basename = os.path.basename(mov_end)
        file_name = os.path.splitext(basename)[0]
        #print(file_name)
        #print (mov_begin)

        #se tiene que añadir una coma ',' para evitar problemas cuando sólo se elige un dancer... el problema es la función tuple()
        bailarines_select_fake = bailarines
        if len(bailarines) == 1:
            if bailarines[0] != 'All_dancers':
                #bailarines_select_fake.append("jghkrgj")
                bailarines_select_fake.append(",")  #añadimos una coma ','
        mytuple = tuple(bailarines_select_fake)
        print(bailarines_select_fake)
        print(bailarines)
        #mytuple = tuple(bailarines_select)
        #print(bailarines_select)
        print("estic a contar_videos_position_dancers_end")

        for sel in bailarines_select:
            if sel == 'All_dancers':
                cursor.execute('SELECT COUNT(*) FROM movements WHERE end = ' + str(file_name))
            else:
                cursor.execute('SELECT COUNT(*) FROM movements WHERE end = '+ str(file_name)+' AND ((dancer_m  IN '+str(mytuple)+')'+' OR (dancer_f IN '+str(mytuple)+'))')
        data = cursor.fetchall()
        num_mov.append(data[0][0])
    print(posiciones)
    #print(num_mov)
    return num_mov

def contar_videos_position_dancers_both(posiciones,bailarines,posiciones_end): #cuántos videos hay que tengan el mismo COMIENZO y FIN
    conn = mysql.connect()
    cursor = conn.cursor()
    num_mov = []
    positions_both = []
    positions_s = []
    positions_e = []
    print(posiciones)
    print(bailarines)

    #se tiene que añadir una coma ',' para evitar problemas cuando sólo se elige un dancer... el problema es la función tuple()
    bailarines_select_fake = bailarines
    if len(bailarines) == 1:
        if bailarines[0] != 'All_dancers':
            #bailarines_select_fake.append("jghkrgj")
            bailarines_select_fake.append(",")  #añadimos una coma ','
    mytuple = tuple(bailarines_select_fake)
    print(bailarines_select_fake)
    print(bailarines)
    #mytuple = tuple(bailarines_select)
    #print(bailarines_select)
    print("estic a contar_videos_position_dancers_both")
    
    for mov_begin in posiciones:
        basename = os.path.basename(mov_begin)
        file_name = os.path.splitext(basename)[0]
        #print(file_name)
        #print (mov_begin)

        for mov_end in posiciones_end:
            basename_end = os.path.basename(mov_end)
            file_name_end = os.path.splitext(basename_end)[0]
            #print(file_name_end)
            #print (mov_end)

            for sel in bailarines_select:
                if sel == 'All_dancers':
                    #cursor.execute('SELECT COUNT(*) FROM movements WHERE begin = ' + str(file_name)+' AND (end = ' + str(file_name_end)+')')
                    cursor.execute('SELECT COUNT(*) FROM basic WHERE begin = ' + str(file_name)+' AND (end = ' + str(file_name_end)+')')
                else:
                    #cursor.execute('SELECT COUNT(*) FROM movements WHERE begin = '+ str(file_name)+' AND (end = ' + str(file_name_end)+')'+
                    cursor.execute('SELECT COUNT(*) FROM basic WHERE begin = '+ str(file_name)+' AND (end = ' + str(file_name_end)+')'+
                        ' AND ((dancer_m  IN '+str(mytuple)+')'+' OR (dancer_f IN '+str(mytuple)+'))')
        
            data = cursor.fetchall()
            if data[0][0] > 0:
                num_mov.append(data[0][0])
                positions_both.append("['"+str(file_name) + "','" + str(file_name_end)+"']")
                positions_s.append(str(file_name)+'.png')
                positions_e.append(str(file_name_end)+'.png')
    #print(posiciones)
    listSum = sum(num_mov)
    print(listSum)
    
    print(num_mov)
    print(positions_both)
    return num_mov, positions_s, positions_e

def datos_de_un_mov(nombre_video):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM movements WHERE title = %s', (nombre_video)) 
    print(nombre_video)
    data = cursor.fetchall()
    print(data)
    return data

def enviar_email_forgot_password(email_forgot,password_forgot):
    # Import smtplib for the actual sending function
    import smtplib

    #import email                                                                         #para hotmail
    ##msg = email.message_from_string('your password is: ' + password_forgot)             #para hotmail  crec NO FUNCIONA!!!
    #msg = 'your password is: ' + password_forgot                                         #para hotmail  FUNCIONA!!!
    #subject = "prueba de correo"                                                         #para hotmail
    #msg = 'Subject: {}\n\n{}'.format(subject, msg)                                       #para hotmail
    #server = smtplib.SMTP("smtp.live.com",587)                                           #para hotmail

    message = 'your password is: ' + password_forgot                #para gmail
    subject = "prueba de correo"                                    #para gmail
    message = 'Subject: {}\n\n{}'.format(subject, message)          #para gmail
    server = smtplib.SMTP('smtp.gmail.com',587)                     #para gmail
    
    server.starttls()

    #server.login('somdelmon@hotmail.com','ex12imasd99')                                 #para hotmail   
    ##server.sendmail('somdelmon@hotmail.com', email_forgot, msg.as_string())            #para hotmail  crec NO FUNCIONA!!!
    #server.sendmail('somdelmon@hotmail.com', email_forgot, msg)                         #para hotmail  FUNCIONA!!!!
    
    server.login('joan.arbussa@gmail.com','ex12imasd99')                                #para gmail
    server.sendmail('joan.arbussa@gmail.com','ideasydiversion@hotmail.com', message)    #para gmail

    server.quit()
    print("correo enviaado satisfactoriamente")
  

#---------------------------------------------------------------------------------------
#--------------------------------- Fin funciones (def) ---------------------------------
#---------------------------------------------------------------------------------------
   

#---------------------------------------------------------------------------------------
#----------------------------- Download videos youtube ---------------------------------
#---------------------------------------------------------------------------------------

@app.route('/download_youtube')
def download_youtube():
    url = 'youtube.com/watch?v=xva71wynxS0'
    youtube = pytube.YouTube(url)
    video = youtube.streams.first()
    video.download()
    return render_template('home.html')

@app.route('/download_youtube3')
def download_youtube3():
    link = "https://www.youtube.com/watch?v=w9TcErzdoTg"
    yt = YouTube(link) 
    try:
        yt.streams.filter(progressive = True, 
    file_extension = "mp4").first().download(output_path = dir_descargas, 
    filename =  "youtube_pepe")
    except:
        print("Some Error1!")
    print('Task Completed1!')
    return render_template('home.html')

@app.route('/download_youtube2')
def download_youtube2():
    # where to save 
    #SAVE_PATH = "E:/" #to_do 
    SAVE_PATH = dir_descargas + "youtube_pepe.mp4"
    # link of the video to be downloaded 
    link="https://www.youtube.com/watch?v=xWOoBJUqlbI"
    try: 
        # object creation using YouTube
        # which was imported in the beginning 
        yt = YouTube(link) 
    except: 
        print("Connection Error") #to handle exception 
    # filters out all the files with "mp4" extension 
    mp4files = yt.filter('mp4') 
    #to set the name of the file
    yt.set_filename('GeeksforGeeks Video')   
    # get the video with the extension and
    # resolution passed in the get() function 
    d_video = yt.get(mp4files[-1].extension,mp4files[-1].resolution) 
    try: 
        # downloading the video 
        d_video.download(SAVE_PATH) 
    except: 
        print("Some Error!") 
    print('Task Completed!') 
    return render_template('home.html')
#---------------------------------------------------------------------------------------
#---------------------------- Fin Download videos youtube ---------------------------------
#---------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------
#----------------------------------- inicio de Cairocoders --------------------------- 
#----------------------------------(de momento no se utiliza) ------------------------
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and displayed below')
        return render_template('index.html', filename=filename)
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)

@app.route('/display/<filename>')
def display_image(filename):
    #print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)

#----------------------------------------------------------------------------------------
#----------------------------------- fin de Cairocoders ----------------------------------

#----------------------------------- inicio de Daily Motion --------------------------- 
#----------------------------------(de momento no se utiliza) ------------------------
#ruta para mostrar los vídeos de Daily Motion
@app.route('/DailyMotion')
def DailyMotion():
    datosObtenidos = requests.get('https://api.dailymotion.com/videos?channel=sport&limit=10') #url del DailyMotion.com
    datosEnFormatoJSON = datosObtenidos.json()
    #print(datosEnFormatoJSON)
    #return render_template('index.html')
    return render_template('DailyMotion.html', datos=datosEnFormatoJSON['list'])


#ruta para mostrar los fotos uploads y textos Daily Motion
@app.route('/searchDailyMotion')
def searchDailyMotion():
    datosObtenidos = requests.get('https://api.dailymotion.com/videos?channel=sport&limit=10') #url del DailyMotion.com
    datosEnFormatoJSON = datosObtenidos.json()
    #print(datosEnFormatoJSON)
    #return render_template('index.html')
    return render_template('search_mov_con_DailyMotion.html', datos=datosEnFormatoJSON['list'], num=0)

#----------------------------------------------------------------------------------------
#----------------------------------- fin de Daily Motion ----------------------------------
#------------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------------------------------
#--------------------- inicio de la parte de diferentes posibilidades a una posición ----------------- 
#----------------------------------------------------------------------------------------------------------------

#para poder pasar una varioable de jquery a python usando json y ajax
#la información se sacó de: https://dataanalyticsireland.ie/es/2021/12/13/how-to-pass-a-javascript-variable-to-python-using-json/
import json

@app.route('/')
def home_barra():
    print('/home_barra')
    clean_list() #para empezar una nueva figura, después de pulsar exit... para borrar la variable global figura_total
    global log_in_name
    return render_template('index.html', log_in_name = log_in_name)

@app.route('/test', methods=['POST'])
def test():
    output = request.get_json()
    print(output) # This is the output that was stored in the JSON within the browser
    print(type(output))
    result = json.loads(output) #this converts the json output to a python dictionary
    print(result) # Printing the new dictionary
    print(type(result))#this shows the json converted as a python dictionary
    dancerines = result.values()

    print(dancerines)
    danzarinas = list(result.values())[0]
    print(danzarinas)
    return result

@app.route('/home')
def home():
    global log_in_name
    return render_template('home.html', log_in_name = log_in_name)

@app.route('/ver_video')
def ver_video():
    #import numpy as np
    #import cv2

    cap = cv2.VideoCapture("https://www.youtube.com/watch?v=fcBRIcVCsOU")
    #cap = cv2.VideoCapture("static/videos_retallar/Nery_cloe.mp4")

    while(cap.isOpened()):
        ret, frame = cap.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        cv2.imshow('frame',gray)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        cap.release()
    cv2.destroyAllWindows()

    return render_template('home.html')

@app.route('/zoom')
def zoom():
    return render_template('demo.html')


#----------------------------------------------------------------------------------------------------------------
#---------------------------------------- Empezar registro usuarios ---------------------------------------------
#----------------------------------------------------------------------------------------------------------------

@app.route('/register')
def register():
    useremails = []
    i = 0
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios')
    data = cursor.fetchall()
    for dato in data:
        useremail = data[i][2] #NOTA: fijarse que es data[i][0] no dato[i][0] 
        i = i + 1
        print(useremail)        
        useremails.append(useremail)
    print(data)
    #print(useremails)
    global log_in_name
    return render_template('register_disseny.html', email_usuaris = useremails, log_in_name = log_in_name)
    #return render_template('register_disseny.html')

@app.route('/myaccount')
def myaccount():
    print("myaccount")
    useremails = []
    userpasswords = []
    i = 0
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios')
    data = cursor.fetchall()
    for dato in data:
        useremail = data[i][2] #NOTA: fijarse que es data[i][0] no dato[i][0] 
        userpassword = data[i][3]
        i = i + 1
        print(useremail)  
        print(userpassword)      
        useremails.append(useremail)
        userpasswords.append(userpassword)
    print(data)
    global log_in_name
    #print(data)
    #return render_template('register.html', usuaris = data)
    #print(useremails)
    return render_template('register_HMA.html', email_usuaris = useremails, password_usuaris = userpasswords, log_in_name = log_in_name)
    #return render_template('register_Geek2.html')

@app.route('/hma')
def hma():
    useremails = []
    userpasswords = []
    i = 0
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios')
    data = cursor.fetchall()
    for dato in data:
        useremail = data[i][2] #NOTA: fijarse que es data[i][0] no dato[i][0] 
        userpassword = data[i][3]
        i = i + 1
        print(useremail)  
        print(userpassword)      
        useremails.append(useremail)
        userpasswords.append(userpassword)
    print(data)
    global log_in_name
    #print(data)
    #return render_template('register.html', usuaris = data)
    #print(useremails)
    return render_template('register_HMA.html', email_usuaris = useremails, password_usuaris = userpasswords, log_in_name = log_in_name)
    #return render_template('register_Geek2.html')

@app.route('/add_user', methods=['POST']) #el formulario de register.html se manda a través de POST
def add_user():
    print('/add_user')
    output = request.get_json()
    result = json.loads(output) #this converts the json output to a python dictionary  
    usuario = list(result.values())[0]
    print(usuario)

    username = usuario[0]
    email = usuario[1]
    password = usuario[2]
    date_created = datetime.today()
    print(username)
    print(email)
    print(password)
    print(date_created)

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO usuarios (username,email,password,date_created) VALUES (%s,%s,%s,%s)',
    (username,email,password,date_created)) #elssegundo id coincide con el parámetro de la función (def)
    conn.commit()
    flash('Movement added successfully')
    return redirect(url_for('register'))#después de insertar un elemento a la tabla, volvemos a la posición inicial (form vacío)

@app.route('/login_user', methods=['POST']) #el formulario de register.html se manda a través de POST
def login_user():
    print('login user')
    output = request.get_json()
    result = json.loads(output) #this converts the json output to a python dictionary  
    usuario = list(result.values())[0]
    print(usuario)

    email = usuario[0]
    password = usuario[1]
    print(email)
    print(password)

    conn = mysql.connect()
    cursor = conn.cursor()
    rows_count = cursor.execute("SELECT * FROM usuarios where email=%s and password=%s",(email,password))    
    #rows_count sirve para contar cuantas veces se cumple el SELECT. En nuestro caso máximo 1
    data = cursor.fetchall()
    global log_in_name
    log_in_name = data[0][1] #es el apodo del usuario que acaba de realizar el log in
    print(log_in_name)

    global log_in
    log_in = True #el usuario ha realizado el log in con éxito
    #return render_template('register_HMA.html', log_in_name = log_in_name)
    return redirect(url_for('hma', log_in_name = log_in_name))

@app.route('/forgot_password', methods=['POST']) #el formulario de register.html se manda a través de POST
def forgot_password():
    print('forgot_password')
    output = request.get_json()
    result = json.loads(output) #this converts the json output to a python dictionary  
    usuario = list(result.values())[0]
    print(usuario)

    email = usuario[0]
    #password = usuario[1]
    print(email)
    #print(password)

    conn = mysql.connect()
    cursor = conn.cursor()
    rows_count = cursor.execute("SELECT * FROM usuarios where email=%s",(email)) 
    print(rows_count)
    #rows_count sirve para contar cuantas veces se cumple el SELECT. En nuestro caso máximo 1
    data = cursor.fetchall()
    password = data[0][3] #es el password del usuario que acaba de realizar el log in
    print(password)

    #enviar email con el password
    enviar_email_forgot_password(email,password)

    return render_template('register_HMA.html')

#----------------------------------------------------------------------------------------------------------------
#-------------------------------------------- Fin registro usuarios ---------------------------------------------
#----------------------------------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------------------------------
#--------------------------------- Añadir nuevo movimiento a la base de datos salsa -----------------------------
#----------------------------------------------------------------------------------------------------------------

#ruta para mostrar las posibles posiciones del baile... sirve para añadir un nuevo movimiento a la base de datos
@app.route('/positions_begin')
def positions_begin():
    print('/positions_begin')
    clean_list() #para empezar una nueva figura, después de pulsar exit... para borrar la variable global figura_total
    #lista_poses = os.listdir("static/uploads/positions/")
    #lista_poses.pop() #eliminar el último elemento de la lista ya que es un directorio (modelo del movimeinto inicial y final)
    print(lista_positions)
    return render_template('positions_begin.html', poses=lista_positions)
    #return render_template('positions_begin.html', poses=lista_poses)

#ruta para mostrar las posibles posiciones del baile... sirve para añadir un nuevo movimiento a la base de datos
@app.route('/positions_end')
def positions_end():
    print('/positions_end')
    clean_list() #para empezar una nueva figura, después de pulsar exit... para borrar la variable global figura_total
    #lista_poses = os.listdir("static/uploads/positions/")
    #lista_poses.pop() #eliminar el último elemento de la lista ya que es un directorio (modelo del movimeinto inicial y final)    
    print(lista_positions)
    return render_template('positions_end.html', poses=lista_positions)
    #return render_template('positions_end.html', poses=lista_poses)
    
@app.route('/new_movement')
def new_movement():
    global log_in
    if (log_in == True):  #es necesario que el usuario esté loggeado (log_in)
        global new_mov
        global log_in_name

        crear_lista_dancers()

        #clip = VideoFileClip("static/videos_retallar/Nery_cloe.mp4") 
        #clip = VideoFileClip("https://www.youtube.com/watch?v=fcBRIcVCsOU")
        #clip = clip.subclip(55, 95)   
        #clip.ipython_display(width = 480) 
        #clip.write_videofile("static/videos_retallar/retall.mp4")
        if ((new_mov[2] == "") or (new_mov[2] == "pre/mov_inicial")):
            new_mov[2] = "pre/mov_inicial";
        if ((new_mov[3] == "") or (new_mov[3] == "pre/mov_final")):
            new_mov[3] = "pre/mov_final";

        print(new_mov)
        return render_template('new_movement.html', vid=new_mov[0], title=new_mov[1], mov_s=new_mov[2], mov_e=new_mov[3],
            elena=new_mov[4], mariano=new_mov[5], info_f_d=new_mov[6], info_m_d=new_mov[7], loc=new_mov[8], info_loc=new_mov[9],
            v_ori=new_mov[10], web_orig=new_mov[11], info_web_orig=new_mov[12], social=new_mov[13], sec_video=new_mov[14],
            log_in_name = log_in_name)
    else:
        return render_template('no_new_movement.html', log_in_name = log_in_name)
        #return redirect(url_for('new_movement'), vid=new_mov[0], title=new_mov[1], sec_s=new_mov[2],  sec_e=new_mov[3],
        #    mov_s=new_mov[4], mov_e=new_mov[5], elena=new_mov[6], mariano=new_mov[7],  loc=new_mov[8],  v_ori=new_mov[9])

        #return redirect('/retardo')
        #return render_template('new_movement.html')

#ruta para VOLVER a new_movement.html cuando ya hemos introducido datos y hemos salido por culpa de dancers,... Refreshing
@app.route('/new_movement_in', methods=['POST'])
def new_movement_in():
    print(new_movement_in)
    output = request.get_json()
    result = json.loads(output) #this converts the json output to a python dictionary  
    #bailarines_select = list(result.values())[0]
    global new_mov
    llista_new = list(result.values())[0]
    print(llista_new)
    print('hola')
    i = 0
    for dato in llista_new:
        new_mov[i] = llista_new[i]
        i = i + 1 
        print(dato)
        print(str(i))
        #print(new_mov)

    #new_mov[0] = llista[0]
    #new_mov[1] = llista[1]

    print(llista_new)
    print(new_mov)
    return 'marianico'
    #return render_template('new_movement.html')

#ruta para añadir a la variable new_mov la opción elegida como posición inicial del nuevo movimiento a insertar en la base de datos
@app.route('/search_begin/<string:file_path>')
def search_begin(file_path):
    print('/search_begin/<string:file_path>')
    print('display_image filename: ' + file_path)
    file_path = os.path.splitext(file_path)[0] #quitar el path del fichero (creo que ya no había)
    file_name = file_path.split('/')[-1] #quitar la extensión del fichero
    print(file_name)
    print('hola')
    global new_mov
    new_mov[2] = file_name
    #return render_template('new_movement.html')
    return redirect(url_for('new_movement'))

#ruta para añadir a la variable new_mov la opción elegida como posición final del nuevo movimiento a insertar en la base de datos
@app.route('/search_end/<string:file_path>')
def search_end(file_path):
    print('/search_end/<string:file_path>')
    print('display_image filename: ' + file_path)
    file_path = os.path.splitext(file_path)[0] #quitar el path del fichero (creo que ya no había)
    file_name = file_path.split('/')[-1] #quitar la extensión del fichero
    print(file_name)
    print('hola')
    global new_mov
    new_mov[3] = file_name
    #return render_template('new_movement.html')
    return redirect(url_for('new_movement'))


@app.route('/web_new_movement', methods=['POST'])
def web_new_movement():
    print('/web_new_movement')
    #global bailarines_select
    global new_mov

    output = request.get_json()
    result = json.loads(output) #this converts the json output to a python dictionary  
    #bailarines_select = list(result.values())[0]
    nou_web = [' ']
    nou_web = list(result.values())[0]
    #print(bailarines_select[0])
    #print(bailarines_select[1])
    print(nou_web[0])
    print('hola')
    if nou_web[0] == ' ':
        new_mov[11]="others"
    else: 
        new_mov[11] = nou_web[0]

    Buscar_info_web(new_mov[11])
    print(new_mov)
    #return render_template('new_movement.html',elena=new_mov[6], mariano=new_mov[7])
    #return redirect(url_for('new_movement'), elena=new_mov[6], mariano=new_mov[7])
    return redirect("/new_movement")

@app.route('/location_new_movement', methods=['POST'])
def location_new_movement():
    print('/location_new_movement')
    #global bailarines_select
    global new_mov

    output = request.get_json()
    result = json.loads(output) #this converts the json output to a python dictionary  
    #bailarines_select = list(result.values())[0]
    nou_location = [' ']
    nou_location = list(result.values())[0]
    #print(bailarines_select[0])
    #print(bailarines_select[1])
    print(nou_location[0])
    print('hola')
    if nou_location[0] == ' ':
        new_mov[8]="others"
    else: 
        new_mov[8] = nou_location[0]

    Buscar_info_location(new_mov[8])
    print(new_mov)
    #return render_template('new_movement.html',elena=new_mov[6], mariano=new_mov[7])
    #return redirect(url_for('new_movement'), elena=new_mov[6], mariano=new_mov[7])
    return redirect("/new_movement")

#ruta para añadir a la variable new_mov los bailarines del nuevo movimiento a insertar en la base de datos
@app.route('/dancers_new_movement', methods=['POST'])
def dancers_new_movement():
    print('/dancers_new_movement')
    #global bailarines_select
    global new_mov

    output = request.get_json()
    result = json.loads(output) #this converts the json output to a python dictionary  
    #bailarines_select = list(result.values())[0]
    nous_ballari_ballarina = [' ',' ']
    nous_ballari_ballarina = list(result.values())[0]
    #print(bailarines_select[0])
    #print(bailarines_select[1])
    print(nous_ballari_ballarina[0])
    print('hola')
    if nous_ballari_ballarina[0] == ' ':
        new_mov[5]="others"
    else: 
        new_mov[5] = nous_ballari_ballarina[0]

    if nous_ballari_ballarina[1] == ' ':
        new_mov[4]="others"
    else: 
        new_mov[4] = nous_ballari_ballarina[1]

    #new_mov[7] = bailarines_select[0]
    #new_mov[6] = bailarines_select[1]

    Buscar_info_dancers(new_mov[5],new_mov[4])


    print(new_mov)

    #return render_template('new_movement.html',elena=new_mov[6], mariano=new_mov[7])
    #return redirect(url_for('new_movement'), elena=new_mov[6], mariano=new_mov[7])
    return redirect("/new_movement")

#ruta para insertar el nuevo movimiento en la base de datos
@app.route('/new_movement_saved', methods=['POST'])
def new_movement_saved():
    print('/new_movement_saved')
    output = request.get_json()
    result = json.loads(output) #this converts the json output to a python dictionary  
    movimiento_nuevo = list(result.values())[0]
    print(movimiento_nuevo)
    Insertar_movimiento_nuevo_DataBase(movimiento_nuevo)
   
    #return render_template('new_movement.html')
    return 'res'

#ruta para insertar el nuevo movimiento en la base de datos
@app.route('/new_movement_cancel')
def new_movement_cancel():
    print('/new_movement_cancel')
    global new_mov
    new_mov = ['','','','','','','','','','','','','','','']

    if ((new_mov[2] == "") or (new_mov[2] == "pre/mov_inicial")):
        new_mov[2] = "pre/mov_inicial";
    if ((new_mov[3] == "") or (new_mov[3] == "pre/mov_final")):
        new_mov[3] = "pre/mov_final";

    print(new_mov)
    return render_template('new_movement.html', vid=new_mov[0], title=new_mov[1], mov_s=new_mov[2], mov_e=new_mov[3],
        elena=new_mov[4], mariano=new_mov[5], info_f_d=new_mov[6], info_m_d=new_mov[7], loc=new_mov[8], info_loc=new_mov[9],
        v_ori=new_mov[10], web_orig=new_mov[11], info_web_orig=new_mov[12], social=new_mov[13], sec_video=new_mov[14],
        log_in_name = log_in_name)

    #new_mov[4] = "pre/mov_inicial";
    #new_mov[5] = "pre/mov_final";
    #return render_template('new_movement.html', vid=new_mov[0], title=new_mov[1], sec_s=new_mov[2],  sec_e=new_mov[3],
        #mov_s=new_mov[4], mov_e=new_mov[5], elena=new_mov[6], mariano=new_mov[7],  loc=new_mov[8],  v_ori=new_mov[9])

#ruta para añadir elementos (vídeos de movimientos de salsa) a la tabla movements de la base de datos salsa
@app.route('/add_mov_ext', methods=['POST']) #el formulario de index_db.html se manda a través de POST
def add_mov_ext():
    print('/add_mov_ext')
    if request.method == 'POST':
        name = request.form['name']
        title = request.form['title']
        start = request.form['start']
        finish = request.form['finish']
        start_mov = request.form['start_movement']
        end_mov = request.form['end_movement']
        dancer_m = request.form['dancer_m']
        dancer_f = request.form['dancer_f']
        place = request.form['place']
        orig_video = request.form['orig_video']
        #sec_video = request.form['sec_video']
        print(name)
        print(title)
        print(dancer_m)
        print(dancer_f)
        print(place)
        
        #conn = mysql.connect()
        #cursor = conn.cursor()
        #cursor.execute('INSERT INTO movements (name,title,start,finish,start_movement,end_movement,dancer_m,dancer_f,place,orig_video) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)',
        #(name,title,start,finish,start_mov,end_mov,dancer_m,dancer_f,place,orig_video)) #elssegundo id coincide con el parámetro de la función (def)
        #conn.commit()
        #flash('Movement added successfully')
    return redirect(url_for('index_db')) #después de insertar un elemento a la tabla, volvemos a la posición inicial (form vacío)

#----------------------------------------------------------------------------------------------------------------
#--------------------- Fin de añadir nuevo movimiento a la base de datos salsa ----------------- 
#----------------------------------------------------------------------------------------------------------------    

@app.route('/dancers_insert')
def dancers_insert():
    print('/dancers_insert')

    #conn = mysql.connect()
    #cursor = conn.cursor()
    ##cursor.execute('SELECT * FROM movements WHERE dancer_m = %s', (pos_inicial))
    ##cursor.execute('SELECT * FROM movements WHERE begin = %s', (pos_inicial)) #comparamos el begin (que es la posición de inicio)
    #cursor.execute('SELECT DISTINCT(dancer_m) FROM movements')
    #data = cursor.fetchall()
    #print(data)

    global bailarines
    global bailarinas

    ##------ como trabajar con tuplas ----------
    #bailarines = []
    #i = 0
    #for dato in data:
    #    bailarin = data[i][0] #NOTA: fijarse que es data[i][0] no dato[i][0] 
    #    i = i + 1
    #    print(bailarin)
    #    if bailarin == '':
    #        bailarin = 'Others'
    #    bailarines.append(bailarin)
    #print(bailarines)
    ##------ fin de como trabajar con tuplas ----------

    #cursor.execute('SELECT DISTINCT(dancer_f) FROM movements')
    #data = cursor.fetchall()
    #print(data)
    #bailarinas = []
    #i = 0
    #for dato in data:
    #    bailarina = data[i][0] #NOTA: fijarse que es data[i][0] no dato[i][0] 
    #    i = i + 1
    #    print(bailarina)
    #    if bailarina == '':
    #        bailarina = 'Others'
    #    bailarinas.append(bailarina)
    #print(bailarinas)
      
    return render_template('dancers_insert.html', dancers_m=bailarines, dancers_f=bailarinas)


@app.route('/web_insert')
def web_insert():
    print('/web_insert')

    conn = mysql.connect()
    cursor = conn.cursor()
    #cursor.execute('SELECT * FROM movements WHERE dancer_m = %s', (pos_inicial))
    #cursor.execute('SELECT * FROM movements WHERE begin = %s', (pos_inicial)) #comparamos el begin (que es la posición de inicio)
    cursor.execute('SELECT DISTINCT(web_video) FROM movements')
    data = cursor.fetchall()
    print(data)

    global web

    #------ como trabajar con tuplas ----------
    web = []
    i = 0
    for dato in data:
        pagina= data[i][0] #NOTA: fijarse que es data[i][0] no dato[i][0] 
        i = i + 1
        print(pagina)
        if pagina == '':
            pagina = 'Others'
        web.append(pagina)
    print(web)
    #------ fin de como trabajar con tuplas ----------
    #global localitzacio     
    return render_template('web_insert.html', web=web)


@app.route('/location_insert')
def location_insert():
    print('/location_insert')

    conn = mysql.connect()
    cursor = conn.cursor()
    #cursor.execute('SELECT * FROM movements WHERE dancer_m = %s', (pos_inicial))
    #cursor.execute('SELECT * FROM movements WHERE begin = %s', (pos_inicial)) #comparamos el begin (que es la posición de inicio)
    cursor.execute('SELECT DISTINCT(place) FROM movements')
    data = cursor.fetchall()
    print(data)

    global localitzacio

    #------ como trabajar con tuplas ----------
    localitzacio = []
    i = 0
    for dato in data:
        local = data[i][0] #NOTA: fijarse que es data[i][0] no dato[i][0] 
        i = i + 1
        print(local)
        if local == '':
            local = 'Others'
        localitzacio.append(local)
    print(localitzacio)
    #------ fin de como trabajar con tuplas ----------
    #global localitzacio     
    return render_template('location_insert.html', localitzacio=localitzacio)

@app.route('/dancers_selected', methods=['POST'])
def dancers_selected():
    print('/dancers_selected')
    global bailarines_select
    global todos_bailarines
    global bailarines
    global bailarinas
    global social_workshop

    output = request.get_json()
    result = json.loads(output) #this converts the json output to a python dictionary  
    bailarines_select = list(result.values())[0]
    social_workshop = bailarines_select.pop() #quitamos de la lista la que será la variable social_workshop
    print(social_workshop)
    print(bailarines_select)

    num_select = len(bailarines_select)
    num_total = len(bailarines) + len(bailarinas)
    print("num_select: "+str(num_select))
    print("num_total: "+str(num_total))

    if num_select >= (num_total + 1): #ponemos +1 ya que el checkbox All_dancers también está seleccionado cuando loestán todos
        todos_bailarines = True  
    else:
        todos_bailarines = False

    print(bailarines_select)
    print(todos_bailarines)
    return render_template('index.html')

@app.route('/dancers')
def dancers():
    print('/dancers')

    conn = mysql.connect()
    cursor = conn.cursor()
    #cursor.execute('SELECT * FROM movements WHERE dancer_m = %s', (pos_inicial))
    #cursor.execute('SELECT * FROM movements WHERE begin = %s', (pos_inicial)) #comparamos el begin (que es la posición de inicio)
    cursor.execute('SELECT DISTINCT(dancer_m) FROM movements')
    data = cursor.fetchall()
    print(data)

    global bailarines
    global bailarinas

    #------ como trabajar con tuplas ----------
    bailarines = []
    i = 0
    for dato in data:
        bailarin = data[i][0] #NOTA: fijarse que es data[i][0] no dato[i][0] 
        i = i + 1
        print(bailarin)
        if bailarin == '':
            bailarin = 'Others'
        bailarines.append(bailarin)
    print(bailarines)
    #------ fin de como trabajar con tuplas ----------

    cursor.execute('SELECT DISTINCT(dancer_f) FROM movements')
    data = cursor.fetchall()
    print(data)
    bailarinas = []
    i = 0
    for dato in data:
        bailarina = data[i][0] #NOTA: fijarse que es data[i][0] no dato[i][0] 
        i = i + 1
        print(bailarina)
        if bailarina == '':
            bailarina = 'Others'
        bailarinas.append(bailarina)
    print(bailarinas)
    global log_in_name
      
    return render_template('dancers.html', dancers_m=bailarines, dancers_f=bailarinas, log_in_name = log_in_name)


#ruta para analizar la imágene de positions.html (static/uploads/) que se ha pulsado 
@app.route('/search/<string:file_path>')
def search(file_path):
    print('/search/<string:file_path>')
    print('display_image filename: ' + file_path)
    file_path = os.path.splitext(file_path)[0] #quitar el path del fichero (creo que ya no había)
    file_name = file_path.split('/')[-1] #quitar la extensión del fichero
    print(file_name)

    global bailarines_select
     
    pos_inicial = file_name
    print(pos_inicial)

    conn = mysql.connect()
    cursor = conn.cursor()

    #se tiene que añadir una coma ',' para evitar problemas cuando sólo se elige un dancer... el problema es la función tuple()
    bailarines_select_fake = bailarines_select    
    if len(bailarines_select) == 1:  
        if bailarines_select[0] != 'All_dancers':
            #bailarines_select_fake.append("jghkrgj")
            bailarines_select_fake.append(",") #añadimos una coma ','
    mytuple = tuple(bailarines_select_fake)
    print(bailarines_select_fake)
    print(bailarines_select)

    #mytuple = tuple(bailarines_select)
    #print(bailarines_select)
    print('hola 1')

    for sel in bailarines_select:
    #for sel in bailarines_select_fake:
        print(sel)
        print(str(pos_inicial))
        print(mytuple)
        if sel == 'All_dancers':
            #cursor.execute("SELECT * FROM movements WHERE dancer_m IN " +  str(mytuple))
            cursor.execute('SELECT * FROM movements WHERE begin = ' + str(pos_inicial))
        else:
            #cursor.execute('SELECT * FROM movements WHERE begin = ' + str(pos_inicial) + ' AND (dancer_m OR dancer_f) IN ' + str(mytuple))
            cursor.execute('SELECT * FROM movements WHERE begin = '+str(pos_inicial)+' AND ((dancer_m  IN '+str(mytuple)+')'+' OR (dancer_f IN '+str(mytuple)+'))')

    data = cursor.fetchall()
    print(data)
    print('hola')
    pos_inicial = pos_inicial + '.png'
    print(pos_inicial)
    return render_template('search_mov.html', datos=data, filnom=pos_inicial)

#ruta para analizar la imágene de positions.html (static/uploads/) que se ha pulsado 
@app.route('/search_both/<string:file_path>')
def search_both(file_path):
    print('/search_both/<string:file_path>')

    file_name = file_path.split(',')[0]
    file_name_end =  file_path.split(',')[1]
    file_name = file_name.split('.')[0]
    file_name_end = file_name_end.split('.')[0]
    print('file_name: ' + file_name)
    print('file_name_end: ' + file_name_end)

#    print('display_image filename: ' + file_path)
#    file_path = os.path.splitext(file_path)[0] #quitar el path del fichero (creo que ya no había)
#    file_name = file_path.split('/')[-1] #quitar la extensión del fichero
#    print(file_name)
#    pos_inicial = file_name
#    print(pos_inicial)

    global bailarines_select
  
    conn = mysql.connect()
    cursor = conn.cursor()

    #se tiene que añadir una coma ',' para evitar problemas cuando sólo se elige un dancer... el problema es la función tuple()
    bailarines_select_fake = bailarines_select    
    if len(bailarines_select) == 1:  
        if bailarines_select[0] != 'All_dancers':
            #bailarines_select_fake.append("jghkrgj")
            bailarines_select_fake.append(",") #añadimos una coma ','
    mytuple = tuple(bailarines_select_fake)
    print(bailarines_select_fake)
    print(bailarines_select)

    #mytuple = tuple(bailarines_select)
    #print(bailarines_select)
    print('hola 1')

    for sel in bailarines_select:
    #for sel in bailarines_select_fake:
        print(sel)
        #print(str(pos_inicial))
        print(mytuple)
        if sel == 'All_dancers':
            #cursor.execute("SELECT * FROM movements WHERE dancer_m IN " +  str(mytuple))
            cursor.execute('SELECT * FROM movements WHERE begin = ' + str(file_name)+' AND (end = ' + str(file_name_end)+')')
        else:
            #cursor.execute('SELECT * FROM movements WHERE begin = ' + str(pos_inicial) + ' AND (dancer_m OR dancer_f) IN ' + str(mytuple))
            cursor.execute('SELECT * FROM movements WHERE begin = '+str(file_name)+' AND (end = ' + str(file_name_end)+')'+
                    ' AND ((dancer_m  IN '+str(mytuple)+')'+' OR (dancer_f IN '+str(mytuple)+'))')

    data = cursor.fetchall()
    print(data)
    print('hola')
    file_name = file_name + '.png'
    print(file_name)
    return render_template('search_mov_both.html', datos=data, filnom=file_name)



#ruta para analizar la imágen de positions.html (static/uploads/) que se ha pulsado, pero que partimos de end a beginning
@app.route('/search_e/<string:file_path>')
def search_e(file_path):
    print('/search_e/<string:file_path>')
    print('display_image filename: ' + file_path)
    file_path = os.path.splitext(file_path)[0] #quitar el path del fichero (creo que ya no había)
    file_name = file_path.split('/')[-1] #quitar la extensión del fichero
    print(file_name)

    global bailarines_select
     
    pos_inicial = file_name
    print(pos_inicial)

    conn = mysql.connect()
    cursor = conn.cursor()

    #se tiene que añadir una coma ',' para evitar problemas cuando sólo se elige un dancer... el problema es la función tuple()
    bailarines_select_fake = bailarines_select    
    if len(bailarines_select) == 1:  
        if bailarines_select[0] != 'All_dancers':
            #bailarines_select_fake.append("jghkrgj")
            bailarines_select_fake.append(",") #añadimos una coma ','
    mytuple = tuple(bailarines_select_fake)
    print(bailarines_select_fake)
    print(bailarines_select)

    #mytuple = tuple(bailarines_select)
    #print(bailarines_select)
    print('hola 1')

    for sel in bailarines_select:
    #for sel in bailarines_select_fake:
        print(sel)
        print(str(pos_inicial))
        print(mytuple)
        if sel == 'All_dancers':
            #cursor.execute("SELECT * FROM movements WHERE dancer_m IN " +  str(mytuple))
            cursor.execute('SELECT * FROM movements WHERE end = ' + str(pos_inicial))
        else:
            #cursor.execute('SELECT * FROM movements WHERE begin = ' + str(pos_inicial) + ' AND (dancer_m OR dancer_f) IN ' + str(mytuple))
            cursor.execute('SELECT * FROM movements WHERE end = '+str(pos_inicial)+' AND ((dancer_m  IN '+str(mytuple)+')'+' OR (dancer_f IN '+str(mytuple)+'))')

    data = cursor.fetchall()
    print(data)
    print('hola')
    pos_inicial = pos_inicial + '.png'
    print(pos_inicial)
    return render_template('search_mov_e.html', datos=data, filnom=pos_inicial)


#ruta para analizar la imágene de positions.html (static/uploads/) que se ha pulsado 
@app.route('/search_fig/<string:file_path>')
def search_fig(file_path):                
    print('/search_fig/<string:file_path>')
    print('display_image filename: ' + file_path)
    file_path = os.path.splitext(file_path)[0] #quitar el path del fichero (creo que ya no había)
    file_name = file_path.split('/')[-1] #quitar la extensión del fichero
    print(file_name)
    pos_inicial = file_name
    print(pos_inicial)

    conn = mysql.connect()
    cursor = conn.cursor()
    #cursor.execute('SELECT * FROM movements WHERE dancer_m = %s', (pos_inicial))
    #cursor.execute('SELECT * FROM movements WHERE begin = %s', (pos_inicial)) #comparamos el begin (que es la posición de inicio)

    mytuple = tuple(bailarines_select)
    print(bailarines_select)

    for sel in bailarines_select:
        if sel == 'All_dancers':
            #cursor.execute('SELECT * FROM movements WHERE begin = %s', (pos_inicial)) 
            cursor.execute('SELECT * FROM movements WHERE begin = ' + str(pos_inicial))
        else:
            #cursor.execute('SELECT * FROM movements WHERE begin = ' + str(pos_inicial) + ' AND (dancer_m OR dancer_f) IN ' + str(mytuple))
            cursor.execute('SELECT * FROM movements WHERE begin = '+str(pos_inicial)+' AND ((dancer_m  IN '+str(mytuple)+')'+' OR (dancer_f IN '+str(mytuple)+'))')

    data = cursor.fetchall()
    print(data)
    pos_inicial = pos_inicial+'.png'
    print(pos_inicial)
    return render_template('search_mov_fig.html', datos=data, filnom=pos_inicial)

#ruta para analizar la imágene de positions.html (static/uploads/) que se ha pulsado 
@app.route('/continue_fig')
def continue_fig():
    print('/continue_fig')

    #primeramente se debe buscar cuál fue el último movimeinto
    global figura_total
    global solo_figura_total
    print(figura_total)
    print(solo_figura_total)
    num_mov=len(figura_total)
    #print('num_muv= '+ str(num_mov) + ' vamos a hacer un pop()')
    #file_path = figura_total.pop(num_mov-1)

    file_path = figura_total[num_mov-1]
    file_path_solo = solo_figura_total[num_mov-1]
    num_mov=len(figura_total)
    #print('num_muv= '+ str(num_mov) + ' hemos hecho un pop()')

    #print('file_path= '+ file_path)
    #filename = os.path.splitext(file_path)[0] #quitar el path del fichero (creo que ya no había)
    #pos_inicial = filename.split('/')[-1] #quitar la extensión del fichero
    #print(pos_inicial)

    filename_begin_end = figura_total[num_mov-1].split('ttststs')
    print(filename_begin_end)

    print("filename: " + filename_begin_end[0])
    print("begin: " + filename_begin_end[1])
    print("end: " + filename_begin_end[2])
    end = filename_begin_end[2]
    solo_video = filename_begin_end[0]
    
    #y después buscar cuáles son las opciones para el siguiente movimiento
    conn = mysql.connect()
    cursor = conn.cursor()
    #cursor.execute('SELECT * FROM movements WHERE begin = %s', (end))
    
    global bailarines_select
    mytuple = tuple(bailarines_select)
    print(bailarines_select)

    for sel in bailarines_select:
        if sel == 'All_dancers':
            #cursor.execute('SELECT * FROM movements WHERE begin = %s', (pos_inicial)) 
            cursor.execute('SELECT * FROM movements WHERE begin = ' + str(end))
        else:
            #cursor.execute('SELECT * FROM movements WHERE begin = ' + str(pos_inicial) + ' AND (dancer_m OR dancer_f) IN ' + str(mytuple))
            cursor.execute('SELECT * FROM movements WHERE begin = '+str(end)+' AND ((dancer_m  IN '+str(mytuple)+')'+' OR (dancer_f IN '+str(mytuple)+'))')

    data = cursor.fetchall()
    print(data)
    end = end + '.png'
    print(end)
    return render_template('search_mov_fig_after_selected.html', datos=data, filnom=end)
    #return render_template('search_mov_fig.html', datos=data)

#ruta para mostrar el movimiento elegido en una ventana modal
@app.route('/selected_and_search_mov_fig/<filename>')
def selected_and_search_mov_fig(filename):
    filename_begin_end = filename.split('ttststs')
    print(filename_begin_end)

    print('/selected_and_search_mov_fig/<filename>')
    print("filename: " + filename_begin_end[0])
    print("begin: " + filename_begin_end[1])
    print("end: " + filename_begin_end[2])
    end = filename_begin_end[2]
    solo_video = filename_begin_end[0]

    print("filename: " + filename)
    global figura_total 
    global solo_figura_total
    figura_total.append(filename)    
    solo_figura_total.append(solo_video)
    print(figura_total)
    print(solo_figura_total)
    filename = os.path.splitext(filename)[0] #quitar el path del fichero (creo que ya no había)
    pos_inicial = filename.split('/')[-1] #quitar la extensión del fichero
    print(pos_inicial)


    #y después buscamos el siguiente movimiento
    conn = mysql.connect()
    cursor = conn.cursor()
    #cursor.execute('SELECT * FROM movements WHERE begin = %s', (end))
    
    global bailarines_select
    mytuple = tuple(bailarines_select)
    print(bailarines_select)

    for sel in bailarines_select:
        if sel == 'All_dancers':
            #cursor.execute('SELECT * FROM movements WHERE begin = %s', (pos_inicial)) 
            cursor.execute('SELECT * FROM movements WHERE begin = ' + str(end))
        else:
            #cursor.execute('SELECT * FROM movements WHERE begin = ' + str(pos_inicial) + ' AND (dancer_m OR dancer_f) IN ' + str(mytuple))
            cursor.execute('SELECT * FROM movements WHERE begin = '+str(end)+' AND ((dancer_m  IN '+str(mytuple)+')'+' OR (dancer_f IN '+str(mytuple)+'))')

    data = cursor.fetchall()
    print('cuántas opciones de movimiento hay?')

    print(data)
    end = end + '.png'
    print(end)
    return render_template('search_mov_fig_after_selected.html', datos=data, filnom=end)
    #return render_template('search_mov_fig.html', datos=data)


#ruta para mostrar las fotos de static/uploads... que son las de las posibles posiciones del baile
@app.route('/positions')
def positions():
    print('/positions')
    clean_list() #para empezar una nueva figura, después de pulsar exit... para borrar la variable global figura_total
    lista_poses = os.listdir("static/uploads/positions/")
    lista_poses.pop() #eliminar el último elemento de la lista ya que es un directorio (modelo del movimeinto inicial y final)
    print('lista_positions')
    print(lista_positions) #la lista_positions está definida como un array con todas las posiciones posibles 

    global bailarines_select

    num_mov = contar_videos_position_dancers(lista_positions,bailarines_select)

    #num_mov = contar_videos_position(lista_poses)
    #num_mov = contar_videos_position(lista_positions)
    print(num_mov)
    global log_in_name

    #finalmente ordenamos de más moviemientos a menos los movimientos de comienzo con múltiples fin
    numero_mov = []
    position = []

    for n_m, p_s in sorted(zip(num_mov, lista_positions), reverse = True):
        numero_mov.append(n_m)
        position.append(p_s)

    #return render_template('positions.html', poses=lista_poses, num_mov=num_mov, tot_mov=sum(num_mov))
    return render_template('positions.html', poses=position, num_mov=numero_mov, tot_mov=sum(num_mov), log_in_name = log_in_name)

@app.route('/positions_e_s')
def positions_e_s():
    print('/positions_e_s')
    clean_list() #para empezar una nueva figura, después de pulsar exit... para borrar la variable global figura_total
    lista_poses = os.listdir("static/uploads/positions/")
    lista_poses.pop() #eliminar el último elemento de la lista ya que es un directorio (modelo del movimeinto inicial y final)
    print('lista_positions')
    print(lista_positions) #la lista_positions está definida como un array con todas las posiciones posibles 

    global bailarines_select

    num_mov = contar_videos_position_dancers_end(lista_positions,bailarines_select)

    #num_mov = contar_videos_position(lista_poses)
    #num_mov = contar_videos_position(lista_positions)
    print(num_mov)
    global log_in_name

        #finalmente ordenamos de más moviemientos a menos los movimientos de fin con múltiples comienzos
    numero_mov = []
    position_e = []

    for n_m, p_e in sorted(zip(num_mov, lista_positions), reverse = True):
        numero_mov.append(n_m)
        position_e.append(p_e)

    #return render_template('positions.html', poses=lista_poses, num_mov=num_mov, tot_mov=sum(num_mov))
    return render_template('positions_e_s.html', poses=position_e, num_mov=numero_mov, tot_mov=sum(num_mov), log_in_name = log_in_name)

#ruta para mostrar las fotos de static/uploads... que son las de las posibles posiciones del baile
@app.route('/positions_both')
def positions_both():
    print('/positions_both')
    clean_list() #para empezar una nueva figura, después de pulsar exit... para borrar la variable global figura_total
    lista_poses = os.listdir("static/uploads/positions/")
    lista_poses.pop() #eliminar el último elemento de la lista ya que es un directorio (modelo del movimeinto inicial y final)
    print('lista_positions')
    print(lista_positions) #la lista_positions está definida como un array con todas las posiciones posibles 

    global bailarines_select

    num_mov,positions_s,positions_e = contar_videos_position_dancers_both(lista_positions,bailarines_select,lista_positions)

    #print(num_mov)
    #print(positions_both)
    global log_in_name


    #finalmente ordenamos de más moviemientos a menos los movimientos de comienzo y fin
    numero_mov = []
    position_s = []
    position_e = []

    for n_m, p_s, p_e in sorted(zip(num_mov, positions_s, positions_e), reverse = True):
        numero_mov.append(n_m)
        position_s.append(p_s)
        position_e.append(p_e)

    #return render_template('positions_both.html', poses=lista_positions, num_mov=num_mov, tot_mov=sum(num_mov), log_in_name = log_in_name)
    #return render_template('positions_both.html', poses=positions_s, poses_e=positions_e, num_mov=num_mov, tot_mov=sum(num_mov), log_in_name = log_in_name)
    return render_template('positions_both.html', poses=position_s, poses_e=position_e, num_mov=numero_mov, tot_mov=sum(num_mov), log_in_name = log_in_name)



#ruta para mostrar las fotos de static/uploads... que son las de las posibles posiciones del baile
@app.route('/creating_fig')
def creating_fig():
    print('/creating_fig')
    clean_list() #para empezar una nueva figura, después de pulsar exit... para borrar la variable global figura_total
    lista_poses = os.listdir("static/uploads/positions/")
    lista_poses.pop() #eliminar el último elemento de la lista ya que es un directorio (modelo del movimeinto inicial y final)
    num_mov = contar_videos_position(lista_poses)
    print(num_mov)
    global log_in_name
    #return render_template('creating_fig.html', poses=lista_poses)
    return render_template('creating_fig.html', poses=lista_poses, num_mov=num_mov, tot_mov=sum(num_mov), log_in_name = log_in_name)

#ruta para mostrar el movimiento elegido en una ventana modal
@app.route('/selected_mov/<filename>')
def selected_mov(filename):
    print('/selected_mov/<filename>')
    print(filename)
    print('/static/videos/'+filename)
    data = datos_de_un_mov(filename)
    print(data)
    print(data[0])
    return render_template('video_mov.html', movimiento=filename, dades=data[0])
    #return render_template('video_mov.html')

#ruta para mostrar el movimiento elegido en una ventana modal
@app.route('/selected_mov_fig/<filename>')
def selected_mov_fig(filename):
    print('/selected_mov_fig/<filename>')
    print("filename: " + filename)
    global figura_total 
    global solo_figura_total
    figura_total.append(filename)
    solo_figura_total.append(filename)
    print(figura_total)
    print(solo_figura_total)
    return render_template('video_mov_fig.html', movimiento=filename)
    #return render_template('video_mov.html')

#ruta para mostrar el movimiento elegido en una ventana modal
@app.route('/pre_selected_mov_fig/<filename>')
def pre_selected_mov_fig(filename):

    print('filename now: '+filename)
    filename_begin_end = filename.split('ttststs')
    print(filename_begin_end)

    print('/pre_selected_mov_fig/<filename>')
    print("filename: " + filename_begin_end[0])
    print("begin: " + filename_begin_end[1])
    print("end: " + filename_begin_end[2])

    data = datos_de_un_mov(filename_begin_end[0])
    print(data)
    print(data[0])

    #return render_template('video_mov_fig.html', movimiento=filename)
    return render_template('video_mov_fig.html', movimiento=filename_begin_end, dades=data[0])

@app.route('/save_fig/<filename>')
def save_fig(filename):
    print('/save_fig/<filename>')

    #name = textinput("Name", "Please enter your name:")

    #print("Hello", name + "!")
    
    #ruta = FileDialog.asksaveasfilename(title="Guardar un fichero")
    #print(ruta)
    print('abacacac')
    print(filename)

    #global figura_total
    global solo_figura_total
    final_clip = VideoFileClip("static/videos/Countdown.mp4") #es un vídeo para inicializar la variable final_clip...podría ser publicidad
    #final_clip = VideoFileClip("static/videos/sm3_11_6.mp4")
    #final_clip = VideoFileClip("https://youtu.be/J4yVVJGFBo0")
    #final_clip = VideoFileClip("https://www.youtube.com/watch?v=Q3uKIRRWbLM")
    #for mov in figura_total:
    for mov in solo_figura_total:
        clip=VideoFileClip("static/videos/"+mov)
        final_clip = concatenate_videoclips([final_clip,clip])
        #final_clip.write_videofile(dir_descargas + "pepe.mp4")
        #final_clip.write_videofile(str(ruta))
        final_clip.write_videofile(filename+'.mp4')

    return render_template('video_figure.html',figura_actual=solo_figura_total)
    #return render_template('video_figure.html',figura_actual=figura_total)

@app.route('/watching_fig')
def watching_fig():
    print('/watching_fig')
    global figura_total
    global solo_figura_total
    print(figura_total)
    print(solo_figura_total)
    num_mov=len(figura_total)
    print("num_mov: " + str(num_mov))
    return render_template('video_figure.html',figura_actual=solo_figura_total)
    #return render_template('video_figure.html',figura_actual=figura_total)

@app.route('/delete_mov_fig')
def delete_mov_fig():
    print('/delete_mov_fig')
    global figura_total
    global solo_figura_total
    print(figura_total)
    print(solo_figura_total)
    num_mov=len(figura_total)
    del figura_total[num_mov-1]
    del solo_figura_total[num_mov-1]
    num_mov=len(figura_total)
    print(figura_total)
    print(solo_figura_total)
    print("num_mov: " + str(num_mov))
    if num_mov == 0: 
        return redirect(url_for('creating_fig'))
    else:
        return render_template('video_figure.html',figura_actual=solo_figura_total)
        #return render_template('video_figure.html',figura_actual=figura_total)

#-----------------------------------------------------------------------------------------------------------
#---- rutas para insertar, editar, borrar,... elementos de la tabla movements de la base de datos salsa ----
#-----------------------------------------------------------------------------------------------------------

#ruta para mostrar el formulario
@app.route('/index_db')
def index_db():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM movements')
    data = cursor.fetchall()
    #print(data)
    global log_in_name
    return render_template('index_db.html', moviments = data, log_in_name = log_in_name)

#ruta para añadir elementos (vídeos de movimientos de salsa) a la tabla movements de la base de datos salsa
@app.route('/add_mov', methods=['POST']) #el formulario de index_db.html se manda a través de POST
def add_mov():
    print('/add_mov')
    if request.method == 'POST':
        name = request.form['name']
        title = request.form['title']
        begin = request.form['begin']
        end = request.form['end']
        dancer_m = request.form['dancer_m']
        dancer_f = request.form['dancer_f']
        place = request.form['place']
        orig_video = request.form['orig_video']
        #sec_video = request.form['sec_video']
        print(name)
        print(title)
        
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO movements (name,title,begin,end,dancer_m,dancer_f,place,orig_video) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)',
        (name,title,begin,end,dancer_m,dancer_f,place,orig_video)) #elssegundo id coincide con el parámetro de la función (def)
        conn.commit()
        flash('Movement added successfully')
    return redirect(url_for('index_db')) #después de insertar un elemento a la tabla, volvemos a la posición inicial (form vacío)

#ruta para editar elementos (vídeos de movimientos de salsa) a la tabla movements de la base de datos salsa
@app.route('/edit_mov/<id>')
def get_mov(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM movements WHERE id = %s', (id)) #formatear el id como un string 
    data = cursor.fetchall()
    print(data) #se puede ver que data es una dupla dentro de una dupla, es decir una lista dentro de una lista
    print(data[0]) #se puede ver que data[0] es la parte de data que nos interesa
    return render_template('edit_mov.html',moviment=data[0])

@app.route('/update_mov/<id>',methods=['POST']) #el formulario de edit_mov.html se manda a través de POST
def update_mov(id):
    if request.method == 'POST':
        name = request.form['name']
        title = request.form['title']
        begin = request.form['begin']
        end = request.form['end']
        dancer_m = request.form['dancer_m']
        dancer_f = request.form['dancer_f']
        i_dancer_m = request.form['i_dancer_m']
        i_dancer_f = request.form['i_dancer_f']
        social = request.form['social'] 
        place = request.form['place']
        i_place = request.form['i_place']
        orig_video = request.form['orig_video']
        web_video = request.form['web_video']
        i_web_video = request.form['i_web_video']
        sec_video = request.form['sec_video']
        del_date = request.form['del_date']

        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE movements
            SET name = %s,
                title = %s,
                begin = %s,
                end = %s,
                dancer_m = %s,
                dancer_f = %s,
                i_dancer_m = %s,
                i_dancer_f = %s,
                social = %s,
                place = %s,
                i_place = %s,
                orig_video = %s,
                web_video = %s,
                i_web_video = %s,
                sec_video = %s,
                del_date = %s
            WHERE id = %s
        """,(name, title, begin, end, dancer_m, dancer_f, i_dancer_m, i_dancer_f, social, place, i_place, orig_video, web_video, i_web_video, sec_video, del_date, id))    
        conn.commit()    

        #flash('Movement removed successfully')
        return redirect(url_for('index_db'))


#ruta para eliminar elementos (vídeos de movimientos de salsa) a la tabla movements de la base de datos salsa
@app.route('/del_mov/<string:id>')
def del_mov(id):
    #print(id)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM movements WHERE id = {0}'.format(id)) #formatear el id como un string
    conn.commit()
    flash('Movement removed successfully')
    #return render_template('index_db.html', moviments = data)
    return redirect(url_for('index_db')) #después de insertar un elemento a la tabla, volvemos a la posición inicial (form vacío)



#ejecutar la rura
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
 