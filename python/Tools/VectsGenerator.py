import json


#Configurazione parte di react
with open('./server/vects.json', 'rt') as f:
  vectsr = json.load(f)
  f.close()

with open('./python/Tools/Output/rvects.json', 'wt') as rvects:
  for s in range(0, len(vectsr['set'])):
    del vectsr['set'][s]['Set']['inVal']
    del vectsr['set'][s]['Set']['inPrevVal']
    del vectsr['set'][s]['Limits']['inMin']
    del vectsr['set'][s]['Limits']['inMax']
    del vectsr['set'][s]['boInit']
    #print (vectsr['set'][s])
  for a in range(0, len(vectsr['act'])):
    del vectsr['act'][a]['Act']['inVal']
    del vectsr['act'][a]['Limits']['inMin']
    del vectsr['act'][a]['Limits']['inMax']
    #print (vectsr['act'][a])
  for l in range(0, len(vectsr['logic'])):
    del vectsr['logic'][l]['byPrevSt']
    del vectsr['logic'][l]['boQ0']
    del vectsr['logic'][l]['boQ1']
    del vectsr['logic'][l]['boQ2']
    del vectsr['logic'][l]['boQ3']
    del vectsr['logic'][l]['boQ4']
    del vectsr['logic'][l]['boQ5']
    del vectsr['logic'][l]['boQ6']
    del vectsr['logic'][l]['boQ7']
    del vectsr['logic'][l]['boInit']
    #print (vectsr['logic'][l])
  for b in range(0, len(vectsr['button'])):
    del vectsr['button'][b]['byPrevSt']
    del vectsr['button'][b]['boQ0']
    del vectsr['button'][b]['boQ1']
    del vectsr['button'][b]['boQ2']
    del vectsr['button'][b]['boQ3']
    del vectsr['button'][b]['boQ4']
    del vectsr['button'][b]['boQ5']
    del vectsr['button'][b]['boQ6']
    del vectsr['button'][b]['boQ7']
    #print (vectsr['button'][b])
  for f in range(0, len(vectsr['alarm'])):
    del vectsr['alarm'][f]['boTrigger']
    del vectsr['alarm'][f]['boQ']
    del vectsr['alarm'][f]['byPrevSt']
    del vectsr['alarm'][f]['byLastStSent']
    del vectsr['alarm'][f]['boAck']
    #print (vectsr['alarm'][f])


  rvects.write(json.dumps(vectsr))
  rvects.close()


#Configurazione parte di arduino
with open('./server/vects.json', 'rt') as f:
  vectsi = json.load(f)
  f.close()

l_HMI_L= len(vectsi['logic'])
l_HMI_B= len(vectsi['button'])
l_HMI_S= len(vectsi['set'])
l_HMI_A= len(vectsi['act'])
l_Alarms= len(vectsi['alarm'])


lgcs=''
for l in range(0, len(vectsi['logic'])):
  lgcs = lgcs + "\n\tudtLogic *" + vectsi['logic'][l]['strVarName'] + " = &VectL[" + str(l) + "];"


btns=''
for b in range(0, len(vectsi['button'])):
  btns = btns + "\n\tudtButton *" + vectsi['button'][b]['strVarName'] + " = &VectB[" + str(b) + "];"


sets=''
for s in range(0, len(vectsi['set'])):
  sets = sets + "\n\tudtSet *" + vectsi['set'][s]['strVarName'] + " = &VectS[" + str(s) + "];"


acts=''
for a in range(0, len(vectsi['act'])):
  acts = acts + "\n\tudtAct *" + vectsi['act'][a]['strVarName'] + " = &VectA[" + str(a) + "];"


alrms=''
for f in range(0, len(vectsi['alarm'])):
  alrms = alrms + "\n\tudtAlarm *" + vectsi['alarm'][f]['strVarName'] + " = &VectAl[" + str(f) + "];"

setslim=''
for sl in range(0, len(vectsi['set'])):
  setslim = setslim + "\n\tHMI_S->" + vectsi['set'][sl]['strVarName'] + "->inMin=" + str(vectsi['set'][sl]['Limits']['inMin']) + ";"
  setslim = setslim + "\n\tHMI_S->" + vectsi['set'][sl]['strVarName'] + "->inMax=" + str(vectsi['set'][sl]['Limits']['inMax']) + ";"

actslim=''
for al in range(0, len(vectsi['act'])):
  actslim = actslim + "\n\tHMI_A->" + vectsi['act'][al]['strVarName'] + "->inMin=" + str(vectsi['act'][al]['Limits']['inMin']) + ";"
  actslim = actslim + "\n\tHMI_A->" + vectsi['act'][al]['strVarName'] + "->inMax=" + str(vectsi['act'][al]['Limits']['inMax']) + ";"

alrmsreact=''
for ar in range(0, len(vectsi['alarm'])):
  strReact = ""
  if (vectsi['alarm'][ar]['byReaction']==1): strReact = "REACT_NORMAL_STOP"
  elif (vectsi['alarm'][ar]['byReaction']==2): strReact = "REACT_FAST_STOP"
  elif (vectsi['alarm'][ar]['byReaction']==3): strReact = "REACT_WARNING"
  elif (vectsi['alarm'][ar]['byReaction']==4): strReact = "REACT_SLOW_SPEED"
  elif (vectsi['alarm'][ar]['byReaction']==5): strReact = "REACT_NOTIFICATION"
  else: strReact = "REACT_WARNING"
  alrmsreact = alrmsreact + "\n\tAlarms->" + vectsi['alarm'][ar]['strVarName'] + "->byReaction = " + strReact + ";"
  
with open('./python/Tools/Output/db_HMI.h', 'wt') as HMI:
  HMI.write('''
#ifndef db_HMI_h
#define db_HMI_h

#include "..\\70_udt\\_70_udt_Include.h"

//Vects length definition
const int l_HMI_L= '''+str(l_HMI_L)+''';
const int l_HMI_B= '''+str(l_HMI_B)+''';
const int l_HMI_S= '''+str(l_HMI_S)+''';
const int l_HMI_A= '''+str(l_HMI_A)+''';
const int l_Alarms= '''+str(l_Alarms)+''';


//Machine reactions definition
const byte REACT_NORMAL_STOP = 1;
const byte REACT_FAST_STOP = 2;
const byte REACT_WARNING = 3;
const byte REACT_SLOW_SPEED = 4;
const byte REACT_NOTIFICATION = 5;


//Logic vars. lVecL is the lenght of the Logic variables array.
udtLogic VectL[l_HMI_L];

//Here you can give a name to the variable in the vect, for an easier use in the program. Only Logic type is allowed in this array.
struct db_HMI_L {''' + lgcs + '''  
};

db_HMI_L _HMI_L, *HMI_L = &_HMI_L;




//Button vars. lVecB is the lenght of the Button variables array.
udtButton VectB[l_HMI_B];

//Here you can give a name to the variable in the vect, for an easier use in the program. Only Button type is allowed in this array.
struct db_HMI_B {''' + btns + '''  
};

db_HMI_B _HMI_B, *HMI_B = &_HMI_B;




//Setpoint vars. lVecS is the lenght of the Setpoint variables array.
udtSet VectS[l_HMI_S];

//Here you can give a name to the variable in the vect, for an easier use in the program. Only Set type is allowed in this array.
struct db_HMI_S {''' + sets + '''  
};

db_HMI_S _HMI_S, *HMI_S = &_HMI_S;




//Actual vars. lVecS is the lenght of the Setpoint variables array.
udtAct VectA[l_HMI_A];

//Here you can give a name to the variable in the vect, for an easier use in the program. Only Act type is allowed in this array.
struct db_HMI_A {''' + acts + '''
};

db_HMI_A _HMI_A, *HMI_A = &_HMI_A;




//Alarm vars. lVecAl is the lenght of the Alarm variables array.
udtAlarm VectAl[l_Alarms];

//Here you can give a name to the variable in the vect, for an easier use in the program. Only Alarm type is allowed in this array.
struct db_Alarms {''' + alrms + '''
};

db_Alarms _Alarms, *Alarms = &_Alarms;
udtMachineReactions _MachineReactions, *MachineReactions = &_MachineReactions;

//Setpoints limits and indexes initialization
void fb_HMIInit(){


  //Inizializzazione indici Logiche
  for(int i=0; i<l_HMI_L; i++) {
      udtLogic *lVar = &VectL[i];
      lVar->inIndex = i;
  }
  
  //Inizializzazione indici setpoints
  for(int i=0; i<l_HMI_S; i++) {
      udtSet *sVar = &VectS[i];
      sVar->inIndex = i;
  }

  //Inizializzazione Limiti Setpoints''' + setslim + '''

  //Inizializzazione reazioni Allarmi''' + alrmsreact + '''
}

#endif
'''
)

