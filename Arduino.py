import serial
import time
import pymongo
import json
from python.DBInit import ActCol, AlarmCol, ButtonCol, LogicCol, SetCol


#=====================================

#  Exceptions Definitions

#=====================================

# class Unplugged is derived from super class Exception 
class Unplugged(Exception): 
  
    # Constructor or Initializer 
    def __init__(self, value): 
        self.value = value 
  
    # __str__ is to print() the value 
    def __str__(self): 
        return(repr(self.value)) 

#=====================================

#  Function Definitions

#=====================================

connectionOK = False

def sendToArduino(sendStr):
  global connectionOK
  try:
    ser.write(sendStr.encode('utf-8')) # change for Python3
  except:
    raise Unplugged("From sendToArduino() - Write timeout. Maybe arduino has been disconnected.")

#======================================

def recvFromArduino():
  global startMarker, endMarker, connectionOK
  
  ck = ""
  x = "z" # any value that is not an end- or startMarker
  byteCount = -1 # to allow for the fact that the last increment will be one too many
  
  # wait for the start character
  try:
    while  ord(x) != startMarker:
      x = ser.read()
    # save data until the end marker is found
    while ord(x) != endMarker:
      if ord(x) != startMarker:
        try:
          ck = ck + x.decode('utf-8') # change for Python3
          byteCount += 1
        except:
          print("decoding error")
      x = ser.read()
    
  except TypeError:
    raise Unplugged("From recvFromArduino()")
  return("{"+ck+"}")


#============================

""" def waitForArduino():

    # wait until the Arduino sends 'Arduino Ready' - allows time for Arduino reset
    # it also ensures that any bytes left over from a previous message are discarded
    
    global startMarker, endMarker
    
    msg = ""
    while msg.find("Arduino is ready") == -1:

        while ser.inWaiting() == 0:
            pass
        
        msg = recvFromArduino()

        print ("waitin"+msg) # python3 requires parenthesis
        print () """
        
#======================================


      
#======================================

# THE PROGRAM STARTS HERE

#======================================

print ()
print ()

while 1:
  #creazione serial

  try:
    ser
  except NameError:
    connectionOK = False
    while not connectionOK:
      print("attempting to connect to Arduino...")
      time.sleep(1)
      try:
        ser = serial.Serial(port='COM4', baudrate=250000, timeout=1, writeTimeout=1)
        connectionOK=True
      except serial.SerialException:
        print("Failed... Try again in 1s...")
      time.sleep(1)
    print("Connected")
    #delimitatore di inizio trama "{"
    startMarker = 123
    #delimitatore di fine trama "}"
    endMarker = 125

    #trama da mandare al loop precedente. se quella nuova è diversa mando
    prevValue=""
    #dati ricevuti dall'arduino
    recData=""
    #flag che dice se trasmettere o ricevere
    waitingForReply = True
    #numero di eventi prima che il watchdog resetti il comando dei button
    wdN = 10
    #wdIno è il watchdog ricevuto da arduino
    wdIno = 0

  ##################################################################################TRASMISSIONE
  try:
    if waitingForReply == False:
      waitingForReply = True
      
      #si parte con la logica, viene composta la stringa che verrà spedita all'arduino: comprende tutti i comandi logici uno dopo l'altro
      data = LogicCol.find().sort('VectIndex')
      l=""
      for x in data:
        #il [2:] è per scartare il 0X della notazione HEX
        tk=str(hex(x['cmd']))[2:]
        while len(tk) <2:
          tk= "0"+tk
        l+=tk
        #dopo aver acquisito il comando dal database ed aggiornato la stringa, pulisco il DB
        LogicCol.update_one(
          {'VectIndex': x['VectIndex']},
          {'$set': {
            'cmd': int(0),
          }}
        )
        
      #passo ai button, viene composta la stringa che verrà spedita all'arduino: comprende tutti i comandi dei button uno dopo l'altro
      data = ButtonCol.find().sort('VectIndex')
      b=""
      for x in data:
        #il [2:] è per scartare il 0X della notazione HEX

        #Watchdog
        #Se il comando è attivo (quindi se il bottone è premuto)
        if x['cmd']!=0:
          #se il conteggio del wd è uguale a quello del ciclo precedente
          if x['wd']==x['wdPrev']:
            #e sta cosa è successa per N volte di fila
            if x['wdCount']==wdN:
              #resetta il comando, che qualcosa è andato storto, e resetta tutti i parametri del wd
              ButtonCol.update_one(
                {'VectIndex': x['VectIndex']},
                {'$set': {
                  'cmd': int(0),
                  'wd': int(0),
                  'wdPrev': int(0),
                  'wdCount': 0
                }}
              )
            #se non è ancora la Nesima volta di fila che capita
            else:
              #lascia tutto com'è e incrementa il wdCount
              ButtonCol.update_one(
                {'VectIndex': x['VectIndex']},
                {'$set': {
                  'wdCount': x['wdCount']+1
                }}
              )
          #se il conteggio del wd è diverso dal ciclo precedente
          else:
            #aggiorna il wdPrev e resetta il wdCount
            ButtonCol.update_one(
              {'VectIndex': x['VectIndex']},
              {'$set': {
                'wdPrev': x['wd'],
                'wdCount': 0
              }}
            )
        #se il comando è a zero
        else:
          #resetta tutti i parametri del wd
          ButtonCol.update_one(
            {'VectIndex': x['VectIndex']},
            {'$set': {
              'wd': int(0),
              'wdPrev': int(0),
              'wdCount': 0
            }}
          )

        tk=str(hex(x['cmd']))[2:]
        while len(tk) <2:
          tk= "0"+tk
        b+=tk
        
      #i setpoint vengono prima di tutto controllati a livello di limiti e fatto in modo che i valori di inizializzazione delle variabili ci rientrino
      s=""
      data = SetCol.find().sort('VectIndex')
      for x in data:
        dec = x['decimals']
        rval = float(x['setpoint']['HMIVal'])
        ival = int(x['setpoint']['PIVal'])
        imin = int(x['limits']['HMIMin']*(10**dec))
        imax = int(x['limits']['HMIMax']*(10**dec))
        rmin = float(x['limits']['HMIMin'])
        rmax = float(x['limits']['HMIMax'])
        if ival < imin:
          ival=imin
          SetCol.update_one(
            {'VectIndex': x['VectIndex']},
            {'$set': {'setpoint.PIVal': ival}}
          )
        elif ival>imax:
          ival=imax
          SetCol.update_one(
            {'VectIndex': x['VectIndex']},
            {'$set': {'setpoint.PIVal': ival}}
          )

        #dopodiché si controlla che il valore impostato da HMI sia nei limiti: se si, il valore viene accettato, convertito in valore intero per arduino
        #se no, si prende il valore di arduino, lo si converte in reale e lo si riscrive al posto di quello imputato.
        if rval < rmin:
          rval = ival/(10**dec)
          SetCol.update_one(
            {'VectIndex': x['VectIndex']},
            {'$set': {'setpoint.HMIVal': rval}}
          )
        elif rval > rmax:
          rval = ival/(10**dec)
          SetCol.update_one(
            {'VectIndex': x['VectIndex']},
            {'$set': {'setpoint.HMIVal': rval}}
          )
        else:
          ival = int(rval*(10**dec))
          SetCol.update_one(
            {'VectIndex': x['VectIndex']},
            {'$set': {'setpoint.PIVal': ival}}
          )

        #a questo punto viene composta la stringa dei valori da mandare all'arduino, infilati uno dopo l'altro    
        #il [2:] è per scartare il 0X della notazione HEX
        tk=str(hex(ival))[2:]
        while len(tk) <4:
          tk= "0"+tk
        s+=tk

      #Qui viene composto il pacchetto completo da mandare all'arduino.
      #sarà qualcosa del genere: {"W":1,"L":"0100000000","B":"11001","S":"00140014001400320014"}

      value = '{"L":"'+l+'","B":"'+b+'","S":"'+s+'"}'
      #print(value)
      if len(set(b))>1 or value!=prevValue:
      #scrittura dei dati
        sendToArduino(value)

      prevValue=value

    ##################################################################################RECEZIONE
    if waitingForReply == True:
      waitingForReply = False

      while ser.inWaiting() == 0:
        pass
        
      recData = recvFromArduino()
      
              
      #print ("Data Received  " + recData)
    
      #parte di recezione dati da arduino.

      #sarà qualcosa del genere: b'{"Logic":"00020002000200020002","Act":"00280028002800640028","Alarm":"01010"}\r\n'
    
      #ricevuto qualcosa, viene decodificato. 
      try:
        data=json.loads(recData)

        #aggiornamento stato Watchdog
        wdIno=data["Wd"]

        #aggiornamento stato logiche
        l=data["Logic"]
        for i in range(0, len(l), 4):
          #gestione logiche
          LogicCol.update_one(
            {'VectIndex': int(i/4)},
            {'$set': {
              'st': int(l[i+2:i+4], base=16),
            }}
          )

        #aggiornamento stato buttons
        b=data["Button"]
        for i in range(0, len(b), 2):
          #gestione logiche
          ButtonCol.update_one(
            {'VectIndex': int(i/2)},
            {'$set': {
              'st': int(b[i:i+2], base=16),
            }}
          )

        #aggiornamento act con conversione in reale del valore intero che mi arriva da arduino        
        a=data["Act"]
        for i in range(0, len(a), 4):
          dec = ActCol.find_one({'VectIndex': int(i/4)})['decimals']
          val = int(a[i:i+4], base=16)
          ActCol.update_one(
            {'VectIndex': int(i/4)},
            {'$set': {
              'actual':{'PIVal': val,'HMIVal': val/(10**dec)}
            }}
          )

        #aggiornamento allarmi    
        al=data["Alarm"]
        for i in range(0, len(al), 1):
          AlarmCol.update_one(
            {'VectIndex': int(i)},
            {'$set': {'status': bool(al[i:i+1])}}
          )
      except:
        print("Except", recData)
        recData=""
  except Unplugged:
    print("Arduino has been unplugged")
    ser.close()
    del ser
    connectionOK=False
