#ifndef db_HMI_h
#define db_HMI_h

#include "..\70_udt\_70_udt_Include.h"

//Vects length definition
const int l_HMI_L= 5;
const int l_HMI_B= 5;
const int l_HMI_S= 5;
const int l_HMI_A= 6;
const int l_Alarms= 5;


//Machine reactions definition
const byte REACT_NORMAL_STOP = 1;
const byte REACT_FAST_STOP = 2;
const byte REACT_WARNING = 3;
const byte REACT_SLOW_SPEED = 4;
const byte REACT_NOTIFICATION = 5;


//Logic vars. lVecL is the lenght of the Logic variables array.
udtLogic VectL[l_HMI_L];

//Here you can give a name to the variable in the vect, for an easier use in the program. Only Logic type is allowed in this array.
struct db_HMI_L {
	udtLogic *Motor0 = &VectL[0];
	udtLogic *Motor1 = &VectL[1];
	udtLogic *Motor2 = &VectL[2];
	udtLogic *Motor3 = &VectL[3];
	udtLogic *Motor4 = &VectL[4];  
};

db_HMI_L _HMI_L, *HMI_L = &_HMI_L;




//Button vars. lVecB is the lenght of the Button variables array.
udtButton VectB[l_HMI_B];

//Here you can give a name to the variable in the vect, for an easier use in the program. Only Button type is allowed in this array.
struct db_HMI_B {
	udtButton *Jog0 = &VectB[0];
	udtButton *Jog1 = &VectB[1];
	udtButton *Jog2 = &VectB[2];
	udtButton *Jog3 = &VectB[3];
	udtButton *Jog4 = &VectB[4];  
};

db_HMI_B _HMI_B, *HMI_B = &_HMI_B;




//Setpoint vars. lVecS is the lenght of the Setpoint variables array.
udtSet VectS[l_HMI_S];

//Here you can give a name to the variable in the vect, for an easier use in the program. Only Set type is allowed in this array.
struct db_HMI_S {
	udtSet *Speed0 = &VectS[0];
	udtSet *Speed1 = &VectS[1];
	udtSet *Speed2 = &VectS[2];
	udtSet *Speed3 = &VectS[3];
	udtSet *Speed4 = &VectS[4];  
};

db_HMI_S _HMI_S, *HMI_S = &_HMI_S;




//Actual vars. lVecS is the lenght of the Setpoint variables array.
udtAct VectA[l_HMI_A];

//Here you can give a name to the variable in the vect, for an easier use in the program. Only Act type is allowed in this array.
struct db_HMI_A {
	udtAct *Current0 = &VectA[0];
	udtAct *Current1 = &VectA[1];
	udtAct *Micrometer1 = &VectA[2];
	udtAct *Current3 = &VectA[3];
	udtAct *Current4 = &VectA[4];
	udtAct *CycleTime = &VectA[5];
};

db_HMI_A _HMI_A, *HMI_A = &_HMI_A;




//Alarm vars. lVecAl is the lenght of the Alarm variables array.
udtAlarm VectAl[l_Alarms];

//Here you can give a name to the variable in the vect, for an easier use in the program. Only Alarm type is allowed in this array.
struct db_Alarms {
	udtAlarm *Alarm0 = &VectAl[0];
	udtAlarm *Alarm1 = &VectAl[1];
	udtAlarm *Alarm2 = &VectAl[2];
	udtAlarm *Alarm3 = &VectAl[3];
	udtAlarm *Alarm4 = &VectAl[4];
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

  //Inizializzazione Limiti Setpoints
	HMI_S->Speed0->inMin=20;
	HMI_S->Speed0->inMax=600;
	HMI_S->Speed1->inMin=20;
	HMI_S->Speed1->inMax=600;
	HMI_S->Speed2->inMin=20;
	HMI_S->Speed2->inMax=600;
	HMI_S->Speed3->inMin=20;
	HMI_S->Speed3->inMax=600;
	HMI_S->Speed4->inMin=20;
	HMI_S->Speed4->inMax=600;

  //Inizializzazione reazioni Allarmi
	Alarms->Alarm0->byReaction = REACT_WARNING;
	Alarms->Alarm1->byReaction = REACT_NORMAL_STOP;
	Alarms->Alarm2->byReaction = REACT_WARNING;
	Alarms->Alarm3->byReaction = REACT_WARNING;
	Alarms->Alarm4->byReaction = REACT_NOTIFICATION;
}

#endif