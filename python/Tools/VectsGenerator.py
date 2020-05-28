import json


#Configurazione parte di react
with open('./server/vects.json', 'rt') as f:
  vectsr = json.load(f)
  f.close()

with open('./python/Tools/Output/rvects.json', 'wt') as rvects:
  for key in vectsr['set'].keys():
    del vectsr['set'][key]['Set']['inVal']
    del vectsr['set'][key]['Set']['inPrevVal']
    del vectsr['set'][key]['Limits']['inMin']
    del vectsr['set'][key]['Limits']['inMax']
    del vectsr['set'][key]['boInit']
    #print (vectsr['set'][key])
  for key in vectsr['act'].keys():
    del vectsr['act'][key]['Act']['inVal']
    del vectsr['act'][key]['Limits']['inMin']
    del vectsr['act'][key]['Limits']['inMax']
    #print (vectsr['act'][a])
  for key in vectsr['logic'].keys():
    del vectsr['logic'][key]['byPrevSt']
    del vectsr['logic'][key]['boQ0']
    del vectsr['logic'][key]['boQ1']
    del vectsr['logic'][key]['boQ2']
    del vectsr['logic'][key]['boQ3']
    del vectsr['logic'][key]['boQ4']
    del vectsr['logic'][key]['boQ5']
    del vectsr['logic'][key]['boQ6']
    del vectsr['logic'][key]['boQ7']
    del vectsr['logic'][key]['boInit']
    #print (vectsr['logic'][l])
  for key in vectsr['button'].keys():
    del vectsr['button'][key]['byPrevSt']
    del vectsr['button'][key]['boQ0']
    del vectsr['button'][key]['boQ1']
    del vectsr['button'][key]['boQ2']
    del vectsr['button'][key]['boQ3']
    del vectsr['button'][key]['boQ4']
    del vectsr['button'][key]['boQ5']
    del vectsr['button'][key]['boQ6']
    del vectsr['button'][key]['boQ7']
    #print (vectsr['button'][b])
  for key in vectsr['alarm'].keys():
    del vectsr['alarm'][key]['boTrigger']
    del vectsr['alarm'][key]['boQ']
    del vectsr['alarm'][key]['byPrevSt']
    del vectsr['alarm'][key]['byLastStSent']
    del vectsr['alarm'][key]['boAck']
    #print (vectsr['alarm'][key])

  sets = []
  for key in vectsr['set'].keys():
    sets.append(vectsr['set'][key])
  acts = []
  for key in vectsr['act'].keys():
    acts.append(vectsr['act'][key])
  logics = []
  for key in vectsr['logic'].keys():
    logics.append(vectsr['logic'][key])
  buttons = []
  for key in vectsr['button'].keys():
    buttons.append(vectsr['button'][key])
  alarms = []
  for key in vectsr['alarm'].keys():
    alarms.append(vectsr['alarm'][key])
  flags = []
  for key in vectsr['flag'].keys():
    flags.append(vectsr['flag'][key])

  vcts={'set': sets, 'act': acts, 'logic': logics, 'button': buttons, 'alarm': alarms, 'flag': flags}
  rvects.write(json.dumps(vcts))
  rvects.close()


#Configurazione parte di arduino
with open('./server/vects.json', 'rt') as f:
  vectsi = json.load(f)
  f.close()

l_HMI_L= len(vectsi['logic'].keys())
l_HMI_B= len(vectsi['button'].keys())
l_HMI_S= len(vectsi['set'].keys())
l_HMI_A= len(vectsi['act'].keys())
l_Alarms= len(vectsi['alarm'].keys())


lgcs=''
for key in vectsi['logic'].keys():
  lgcs = lgcs + "\n\tudtLogic *" + vectsi['logic'][key]['strVarName'] + " = &VectL[" + str(vectsi['logic'][key]['inIndex']) + "];"


btns=''
for key in vectsi['button'].keys():
  btns = btns + "\n\tudtButton *" + vectsi['button'][key]['strVarName'] + " = &VectB[" + str(vectsi['button'][key]['inIndex']) + "];"


sets=''
for key in vectsi['set'].keys():
  sets = sets + "\n\tudtSet *" + vectsi['set'][key]['strVarName'] + " = &VectS[" + str(vectsi['set'][key]['inIndex']) + "];"


acts=''
for key in vectsi['act'].keys():
  acts = acts + "\n\tudtAct *" + vectsi['act'][key]['strVarName'] + " = &VectA[" + str(vectsi['act'][key]['inIndex']) + "];"


alrms=''
for key in vectsi['alarm'].keys():
  alrms = alrms + "\n\tudtAlarm *" + vectsi['alarm'][key]['strVarName'] + " = &VectAl[" + str(vectsi['alarm'][key]['inIndex']) + "];"

setslim=''
for key in vectsi['set'].keys():
  setslim = setslim + "\n\tHMI_S->" + vectsi['set'][key]['strVarName'] + "->inMin=" + str(vectsi['set'][key]['Limits']['inMin']) + ";"
  setslim = setslim + "\n\tHMI_S->" + vectsi['set'][key]['strVarName'] + "->inMax=" + str(vectsi['set'][key]['Limits']['inMax']) + ";"

actslim=''
for key in vectsi['act'].keys():
  actslim = actslim + "\n\tHMI_A->" + vectsi['act'][key]['strVarName'] + "->inMin=" + str(vectsi['act'][key]['Limits']['inMin']) + ";"
  actslim = actslim + "\n\tHMI_A->" + vectsi['act'][key]['strVarName'] + "->inMax=" + str(vectsi['act'][key]['Limits']['inMax']) + ";"

alrmsreact=''
for key in vectsi['alarm'].keys():
  strReact = ""
  if (vectsi['alarm'][key]['byReaction']==1): strReact = "REACT_NORMAL_STOP"
  elif (vectsi['alarm'][key]['byReaction']==2): strReact = "REACT_FAST_STOP"
  elif (vectsi['alarm'][key]['byReaction']==3): strReact = "REACT_WARNING"
  elif (vectsi['alarm'][key]['byReaction']==4): strReact = "REACT_SLOW_SPEED"
  elif (vectsi['alarm'][key]['byReaction']==5): strReact = "REACT_NOTIFICATION"
  else: strReact = "REACT_WARNING"
  alrmsreact = alrmsreact + "\n\tAlarms->" + vectsi['alarm'][key]['strVarName'] + "->byReaction = " + strReact + ";"
  
with open('./python/Tools/Output/db_HMI.h', 'wt') as HMI:
  HMI.write(
'''#ifndef db_HMI_h
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

#endif'''
)

