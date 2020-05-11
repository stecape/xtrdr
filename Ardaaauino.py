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
  byteSendStr = bytearray(sendStr)
  print(byteSendStr)
  try:
    ser.write(byteSendStr) # change for Python3
  except:
    raise Unplugged("From sendToArduino() - Write timeout. Maybe arduino has been disconnected.")

#======================================

def recvFromArduino():
  global startMarker, endMarker, connectionOK
  
  ck = []
  x = "z" # any value that is not an end- or startMarker
  byteCount = -1 # to allow for the fact that the last increment will be one too many
  
  # wait for the start character
  try:
    while  x != startMarker:
      x = ser.read()
    ck.append(x)
    # save data until the end marker is found
    while x != endMarker:
      if x != startMarker:
        try:
          ck.append(x) # change for Python3
          byteCount += 1
        except:
          print("decoding error")
      x = ser.read()
    ck.append(x)
  except TypeError:
    raise Unplugged("From recvFromArduino()")
  return(ck)


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

byFlags =0

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
        ser = serial.Serial(port='COM4', baudrate=250000, timeout=1, writeTimeout=1) #
            
        #boFirstRound è la flag che indica che ci siamo appena connessi all'Arduino, dobbiamo quindi richiedere tutti i dati.
        byFirstRound=4
        #Flags {
        #   0: Wd,
        #   1: Ack,
        #   2: GimmeEverything
        # }
        byFlags = byFirstRound
        connectionOK=True
        
      except serial.SerialException:
        print("Failed... Try again in 1s...")
      time.sleep(1)
    print("Connected")
    #delimitatore di inizio trama "{"
    startMarker = b'{'
    #delimitatore di fine trama "}"
    endMarker = b'}'

    #trama da mandare al loop precedente. se quella nuova è diversa mando
    prevValue=""
    #dati ricevuti dall'arduino
    recData=""
    #flag che dice se trasmettere o ricevere
    waitingForReply = True
    #numero di eventi prima che il watchdog resetti il comando dei button
    wdN = 10


  ##################################################################################TRASMISSIONE
  try:
    if waitingForReply == False:
      waitingForReply = True
      
      #salvo il valore del bit gimme everything
      boGimmeEverything = byFirstRound==4

      #inizializzo il cursore e inizializzo il frame con lo starter e il byte dei flags, saltando la lunghezza della trama che la scrivo alla fine
      byBuffer=[0]*1024
      inCursor=0
      byBuffer[inCursor]=ord(startMarker)
      byBuffer[inCursor+3]=byFlags+byFirstRound
      inCursor+=4

      #Logics
      #il flag di "cambiamento nei valori" viene inizializzato al valore della flag gimme everything, così se fosse true siamo già a posto nel for che c'è dopo.
      boChanged=False
      inOffset=2
      byCounter=0

      data = LogicCol.find().sort('VectIndex')

      for x in data:
        if x['cmd']!=0:
          boChanged=True
          byBuffer[inCursor+inOffset]=x['VectIndex']
          byBuffer[inCursor+inOffset+1]=x['cmd']
          inOffset+=2      
          byCounter+=1      

        #dopo aver acquisito il comando dal database ed aggiornato la stringa, pulisco il DB
        LogicCol.update_one(
          {'VectIndex': x['VectIndex']},
          {'$set': {
            'cmd': int(0),
          }}
        )

      #Se qualcosa è cambiato nelle logiche allora metto la L ed avanzo col cursore, sennò rimango dove sono e procedo coi buttons
      if boChanged:
        byBuffer[inCursor]=ord('L')
        byBuffer[inCursor+1]=byCounter
        inCursor+=inOffset
        
      #Buttons
      #il flag di "cambiamento nei valori" viene inizializzato al valore della flag gimme everything, così se fosse true siamo già a posto nel for che c'è dopo.
      boChanged=False
      inOffset=2
      byCounter=0

      data = ButtonCol.find().sort('VectIndex')

      for x in data:

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
                  'cmdPrev': int(0),
                  'wd': int(0),
                  'wdPrev': int(0),
                  'wdCount': 0
                }}
              )
              boChanged=True
              byBuffer[inCursor+inOffset]=x['VectIndex']
              byBuffer[inCursor+inOffset+1]=bytes([0])
              inOffset+=2 
              byCounter+=1      
            #se non è ancora la Nesima volta di fila che capita
            else:
              #lascia tutto com'è e incrementa il wdCount
              ButtonCol.update_one(
                {'VectIndex': x['VectIndex']},
                {'$set': {
                  'wdCount': x['wdCount']+1,
                  'cmdPrev': 1
                }}
              )
              boChanged=True
              byBuffer[inCursor+inOffset]=x['VectIndex']
              byBuffer[inCursor+inOffset+1]=x['cmd']
              inOffset+=2
              byCounter+=1    
          #se il conteggio del wd è diverso dal ciclo precedente
          else:
            #aggiorna il wdPrev e resetta il wdCount
            ButtonCol.update_one(
              {'VectIndex': x['VectIndex']},
              {'$set': {
                'wdPrev': x['wd'],
                'wdCount': 0,
                'cmdPrev': 1
              }}
            )
            boChanged=True
            byBuffer[inCursor+inOffset]=x['VectIndex']
            byBuffer[inCursor+inOffset+1]=x['cmd']
            inOffset+=2
            byCounter+=1    
        #se il comando è a zero
        else:
          #resetta tutti i parametri del wd
          if x['cmdPrev']==1:
            boChanged=True
            byBuffer[inCursor+inOffset]=x['VectIndex']
            byBuffer[inCursor+inOffset+1]=x['cmd']
            inOffset+=2
            byCounter+=1    

          ButtonCol.update_one(
            {'VectIndex': x['VectIndex']},
            {'$set': {
              'wd': int(0),
              'wdPrev': int(0),
              'wdCount': 0,
              'cmdPrev': 0
            }}
          )

      #Se qualcosa è cambiato nei buttons allora metto la B ed avanzo col cursore, sennò rimango dove sono e procedo coi setpoints
      if boChanged:
        byBuffer[inCursor]=ord('B')
        byBuffer[inCursor+1]=byCounter
        inCursor+=inOffset
        
      #Setpoints
      #il flag di "cambiamento nei valori" viene inizializzato al valore della flag gimme everything, così se fosse true siamo già a posto nel for che c'è dopo.
      boChanged=boGimmeEverything
      inOffset=2
      byCounter=0

      #i setpoint vengono prima di tutto controllati a livello di limiti e fatto in modo che i valori di inizializzazione delle variabili ci rientrino
      data = SetCol.find().sort('VectIndex')
      for x in data:
        dec = x['decimals']
        rval = float(x['setpoint']['HMIVal'])
        ival = ivalPrev = int(x['setpoint']['PIVal'])
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

        if ival != ivalPrev or boGimmeEverything:
          boChanged=True
          byBuffer[inCursor+inOffset]=x['VectIndex']
          byBuffer[inCursor+inOffset+1]=ival.to_bytes(2, byteorder='big')[0]
          byBuffer[inCursor+inOffset+2]=ival.to_bytes(2, byteorder='big')[1]
          inOffset+=3
          byCounter+=1    

      #Se qualcosa è cambiato nei setpoints allora metto la S ed avanzo col cursore, sennò rimango dove sono e chiudo il pacchetto
      if boChanged:
        byBuffer[inCursor]=ord('S')
        byBuffer[inCursor+1]=byCounter
        inCursor+=inOffset
        
      #Lunghezza del pacchetto:
      byBuffer[1]=(inCursor+1).to_bytes(2, byteorder='big')[0]
      byBuffer[2]=(inCursor+1).to_bytes(2, byteorder='big')[1]
      
      #Qui viene chiuso il pacchetto completo da mandare all'arduino.
      byBuffer[inCursor]=ord(endMarker)

      value = byBuffer[0:inCursor+1]
      if value!=prevValue:
      #scrittura dei dati
        #print("Sent: ", value)
        sendToArduino(value)

      prevValue=value
      byFirstRound=0

    ##################################################################################RECEZIONE
    if waitingForReply == True:
      waitingForReply = False

      while ser.inWaiting() == 0:
        pass
        
      recData = recvFromArduino()
    
      #parte di recezione dati da arduino.

      #ricevuto qualcosa, viene decodificato. 
      try:

        #inizializzo il cursore
        inCursor = 0

        #ricavo la lunghezza della stringa
        inLength = recData[inCursor+1][0]*255+recData[inCursor+2][0]

        if recData.index(endMarker)-recData.index(startMarker)+1!=inLength:
          print("Frame corrotto: ", recData)
        
        else:
          #aggiornamento stato Flags
          #print("Rec: ", recData)
          byFlags=recData[inCursor+3][0]

          inCursor+=4
          
          while inCursor < inLength-1:
            inItemsN = ord(recData[inCursor+1])
            inCursor+=2
            if recData[inCursor-2]==b'L':
              for i in range(1, inItemsN):
                val = recData[inCursor+1][0]
                LogicCol.update_one(
                  {'VectIndex': recData[inCursor][0]},
                  {'$set': {'st': val}}
                )
                inCursor+=2
            
            
            elif recData[inCursor-2]==b'B':
              for i in range(1, inItemsN):
                val = recData[inCursor+1][0]
                ButtonCol.update_one(
                  {'VectIndex': recData[inCursor][0]},
                  {'$set': {'st': val}}
                )
                inCursor+=2
            
            
            elif recData[inCursor-2]==b'S':
              for i in range(1, inItemsN):
                dec = SetCol.find_one({'VectIndex': recData[inCursor][0]})['decimals']
                val = recData[inCursor+1][0]*255+recData[inCursor+2][0]
                SetCol.update_one(
                  {'VectIndex': recData[inCursor][0]},
                  {'$set': {
                    'setpoint':{'PIVal': val,'HMIVal': val/(10**dec)}
                  }}
                )
                inCursor+=3
            
            
            elif recData[inCursor-2]==b'A':
              for i in range(1, inItemsN):
                dec = ActCol.find_one({'VectIndex': recData[inCursor][0]})['decimals']
                val = recData[inCursor+1][0]*255+recData[inCursor+2][0]
                ActCol.update_one(
                  {'VectIndex': recData[inCursor][0]},
                  {'$set': {
                    'actual':{'PIVal': val,'HMIVal': val/(10**dec)}
                  }}
                )
                inCursor+=3
            
            
            elif recData[inCursor-2]==b'F':
              for i in range(1, inItemsN):
                val = recData[inCursor+1][0]
                AlarmCol.update_one(
                  {'VectIndex': recData[inCursor][0]},
                  {'$set': {'status': val}}
                )
                inCursor+=2



      except:
        print("Rec Except", recData)
        recData=""
  except Unplugged:
    print("Arduino has been unplugged")
    ser.close()
    del ser
    connectionOK=False
