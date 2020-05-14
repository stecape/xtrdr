import time
import pymongo
import json
from pySerialTransfer import pySerialTransfer as txfer
from python.DBInit import ActCol, AlarmCol, ButtonCol, LogicCol, SetCol


if __name__ == '__main__':
    try:    
        while True:
            try:
                stLink = txfer.SerialTransfer('COM12', baud=250000)
                print("here")
                stLink.open()
                
                #Al primo giro richiede ad Ino tutti i dati di HMI
                boFirstRound=True
                #Dopodichè manda tutti i Setpoint aggiornati
                boRefreshInoData=False
                #inizializzo la flag di coonessione ok con l'arudino a false
                boConnectionOK = True
                #numero di eventi prima che il watchdog resetti il comando dei button
                wdN = 10

                time.sleep(2) # allow some time for the Arduino to completely reset

                while boConnectionOK:
                    
                    ###################################################################
                    # Wait for a response and report any errors while receiving packets
                    ###################################################################
                    while not stLink.available():
                        if stLink.status < 0:
                            if stLink.status == -1:
                                print('ERROR: CRC_ERROR')
                            elif stLink.status == -2:
                                print('ERROR: PAYLOAD_ERROR')
                            elif stLink.status == -3:
                                print('ERROR: STOP_BYTE_ERROR')

                    ###################################################################
                    # Parse received list
                    ###################################################################
                    byRecList = stLink.rx_obj(obj_type=list,
                                            obj_byte_size=stLink.bytesRead,
                                            list_format='c')
                    #print("Rec: ", byRecList)
                    byFlag = ord(byRecList[0])
                    inCursor = 1
                    while inCursor < stLink.bytesRead-1:

                        #Salvo il numero di items dall'elemento lettera +1
                        inItemsN = ord(byRecList[inCursor+1])
                        inCursor+=2
                        #Switch case sull'elemento lettera
                        if byRecList[inCursor-2] == 'L':
                            for i in range(0, inItemsN):
                                LogicCol.update_one(
                                    {'VectIndex': ord(byRecList[inCursor])},
                                    {'$set': {'st': ord(byRecList[inCursor+1])}}
                                )
                                inCursor+=2
                        
                        if byRecList[inCursor-2] == 'B':
                            for i in range(0, inItemsN):
                                ButtonCol.update_one(
                                    {'VectIndex': ord(byRecList[inCursor])},
                                    {'$set': {'st': ord(byRecList[inCursor+1])}}
                                )
                                inCursor+=2
                        
                        if byRecList[inCursor-2] == 'S':
                            for i in range(0, inItemsN):
                                dec = SetCol.find_one({'VectIndex': ord(byRecList[inCursor])})['decimals']
                                val = ord(byRecList[inCursor+1])*256+ord(byRecList[inCursor+2])
                                SetCol.update_one(
                                    {'VectIndex': ord(byRecList[inCursor])},
                                    {'$set': {
                                        'setpoint':{'PIVal': val,'HMIVal': val/(10**dec)}
                                    }}
                                )
                                inCursor+=3
                        
                        if byRecList[inCursor-2] == 'A':
                            for i in range(0, inItemsN):
                                dec = ActCol.find_one({'VectIndex': ord(byRecList[inCursor])})['decimals']
                                val = ord(byRecList[inCursor+1])*256+ord(byRecList[inCursor+2])
                                ActCol.update_one(
                                    {'VectIndex': ord(byRecList[inCursor])},
                                    {'$set': {
                                        'actual':{'PIVal': val,'HMIVal': val/(10**dec)}
                                    }}
                                )
                                inCursor+=3
                        
                        if byRecList[inCursor-2] == 'F':
                            for i in range(0, inItemsN):
                                AlarmCol.update_one(
                                    {'VectIndex': ord(byRecList[inCursor])},
                                    {'$set': {'st': ord(byRecList[inCursor+1])}}
                                )
                                inCursor+=2



                    
                    ###################################################################
                    # First handshake after connection
                    ###################################################################
                    if boFirstRound:
                        if byFlag & 0x07 == 0:
                            byFlag+=1
                            
                        elif byFlag & 0x07 == 1:
                            byFlag+=1
                            
                        elif byFlag & 0x07 == 2:
                            byFlag+=1
                            
                        elif byFlag & 0x07 == 3:
                            byFlag+=1
                            
                        elif byFlag & 0x07 == 4:
                            byFlag+=1
                            
                        elif byFlag & 0x07 == 5:
                            byFlag-=5
                            boFirstRound=False
                            boRefreshInoData=True

                        byList = [byFlag & 0xFF]
                    ###################################################################
                    # Normal send operations
                    ###################################################################  
                    
                    

                    else:

                        byList = [0x00]
                    
                    ###################################################################
                    # Logic
                    ################################################################### 
                    
                    
                        byListL = [ord('L'), 0x00]

                        #Logics
                        #il flag di "cambiamento nei valori" viene inizializzato al valore della flag gimme everything, così se fosse true siamo già a posto nel for che c'è dopo.
                        boChanged=False
                        byCounter=0

                        data = LogicCol.find().sort('VectIndex')

                        for x in data:
                            if x['cmd']!=0:
                                boChanged=True
                                byListL.append(x['VectIndex'] & 0xFF)
                                byListL.append(x['cmd'] & 0xFF)
                                byCounter+=1     

                                #dopo aver acquisito il comando dal database ed aggiornato la stringa, pulisco il DB
                                LogicCol.update_one(
                                    {'VectIndex': x['VectIndex']},
                                    {'$set': {
                                    'cmd': int(0),
                                    }}
                                    )

                        #Se qualcosa è cambiato nelle logiche allora attacco byListL
                        if boChanged:
                            byListL[1]=byCounter & 0xFF
                            byList+=byListL
                    

                    
                    ###################################################################
                    # Buttons
                    ################################################################### 
                    
                        #Buttons
                        #il flag di "cambiamento nei valori" viene inizializzato al valore della flag gimme everything, così se fosse true siamo già a posto nel for che c'è dopo.
                        byListB = [ord('B'), 0x00]
                        boChanged = False
                        byCounter = 0

                        data = ButtonCol.find().sort('VectIndex')
                        
                        for x in data:
                            #Watchdog
                            #Se il comando è attivo (quindi se il bottone è premuto)
                            if x['cmd']!=0:
                                #se il conteggio del wd è uguale a quello del ciclo precedente
                                if x['wd']==x['wdPrev']:
                                    #e sta cosa è successa per N volte di fila
                                    if x['wdCount']==wdN:
                                        #resetta il comando, che qualcosa è andato storto nel DB o nella webApp
                                        #e resetta tutti i parametri del wd
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
                                        byListB.append(x['VectIndex'] & 0xff)
                                        byListB.append(0x00)
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
                                        byListB.append(x['VectIndex'] & 0xFF)
                                        byListB.append(x['cmd'] & 0xFF)
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
                                    byListB.append(x['VectIndex'] & 0xFF)
                                    byListB.append(x['cmd'] & 0xFF)
                                    byCounter+=1    
                            #se il comando è a zero e il giro prima era a uno
                            else:
                            #resetta tutti i parametri del wd
                                if x['cmdPrev']==1:
                                    boChanged=True
                                    byListB.append(x['VectIndex'] & 0xFF)
                                    byListB.append(x['cmd'] & 0xFF)
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

                        #Se qualcosa è cambiato nei buttons allora attacco byListB
                        if boChanged:
                            byListB[1]=byCounter & 0xFF
                            byList+=byListB
                    

                    
                    ###################################################################
                    # Setpoints
                    ################################################################### 
                
                        #Setpoints
                        #il flag di "cambiamento nei valori" viene inizializzato al valore della flag gimme everything, così se fosse true siamo già a posto nel for che c'è dopo.
                        byListS = [ord('S'), 0x00]

                        #inizializzo changed a refreshInoData in modo che appena va a true (appena dopo l'handshake iniziale)
                        #trasmette tutti i set
                        boChanged=boRefreshInoData
                        byCounter=0

                        #i setpoint vengono prima di tutto controllati a livello di limiti e fatto in modo che i valori di inizializzazione delle variabili ci rientrino
                        #bugia! ho spostato il controllo limiti nell'arduino
                        data = SetCol.find().sort('VectIndex')

                        for x in data:
                            dec = x['decimals']
                            rval = float(x['setpoint']['HMIVal'])
                            ivalPrev = int(x['setpoint']['PIVal'])
                            ival = int(rval*(10**dec))

                            if ival != ivalPrev or boRefreshInoData:
                                SetCol.update_one(
                                    {'VectIndex': x['VectIndex']},
                                    {'$set': {'setpoint.PIVal': ival}}
                                )
                                boChanged=True
                                byListS.append(x['VectIndex'] & 0xff)
                                byListS+=([ival >> i & 0xff for i in (8,0)])
                                byCounter+=1    

                        #Se qualcosa è cambiato nei setpoints allora metto la S ed avanzo col cursore, sennò rimango dove sono e chiudo il pacchetto
                        if boChanged:
                            byListS[1]=byCounter & 0xff
                            byList+=byListS

                        #quindi resetto boRefreshInoData per il prossimo loop
                        boRefreshInoData=False

                    ###################################################################
                    # Transmit all the data to send in a single packet
                    ###################################################################

                    byList = "".join(map(chr, byList))
                    inListSize = stLink.tx_obj(byList)
                    stLink.send(inListSize)
                    
                    #print('SENT: {}'.format(byList))
        
        
            except:
                import traceback
                traceback.print_exc()
            
                stLink.close()

    except KeyboardInterrupt:
        stLink.close()