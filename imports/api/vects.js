import { Mongo } from 'meteor/mongo'
import { Meteor } from 'meteor/meteor'

// vects definition
export const Setpoint = new Mongo.Collection('Set')
export const Actual = new Mongo.Collection('Act')
export const Logic = new Mongo.Collection('Logic')
export const Button = new Mongo.Collection('Button')
export const Alarm = new Mongo.Collection('Alarm')
export const Flag = new Mongo.Collection('Flag')

if (Meteor.isServer) {
    Meteor.publish('setpointData', function () {
      return Setpoint.find()
      // var data = Setpoint.find()
  
      // if ( data ) {
      //   return data
      // }
  
      // return this.ready()
    })
    Meteor.publish('actualData', function () {
      return Actual.find()
      // var data = Actual.find()
  
      // if ( data ) {
      //   return data
      // }
  
      // return this.ready()
    })
    Meteor.publish('logicData', function () {
      return Logic.find()
      // var data = Logic.find()
  
      // if ( data ) {
      //   return data
      // }
  
      // return this.ready()
    })
    Meteor.publish('buttonData', function () {
      return Button.find()
      // var data = Logic.find()
  
      // if ( data ) {
      //   return data
      // }
  
      // return this.ready()
    })
    Meteor.publish('alarmData', function () {
      return Alarm.find()
      // var data = Alarm.find()
  
      // if ( data ) {
      //   return data
      // }
  
      // return this.ready()
    })
}

if (Meteor.isClient) {
    Meteor.subscribe('setpointData')
    Meteor.subscribe('actualData')
    Meteor.subscribe('logicData')
    Meteor.subscribe('buttonData')
    Meteor.subscribe('alarmData')
}


Meteor.methods({

  'Setpoint.update'(strVarName, reHMIVal) {
    var val = parseFloat(reHMIVal)
    Setpoint.update(
      { strVarName: strVarName },
      { $set: { 
        'Set.reHMIVal': val
      } }
    )
  },
  
  'Logic.update'(strVarName, byCmd) {
    var value =  Math.pow(2,parseInt(byCmd))
    Logic.update(
      { strVarName: strVarName },
      { $set: { 
        'byCmd': value
      } }
    )
  },
  
  'Button.update'(strVarName, index, boVal) {
    var value =  Math.pow(2,parseInt(index))*(+boVal)
    Button.update(
      { strVarName: strVarName },
      { $set: { 
        'byCmd': value
      } }
    )
  },
  
  'Button.clear'(strVarName) {
    Button.update(
      { strVarName: strVarName },
      { $set: { 
        'byCmd': 0,
        'inWd': 0
      } }
    )
  },
  
  'Button.wd'(strVarName) {
    Button.update(
      { strVarName: strVarName },
      { $inc: { 
        'inWd': 1
      } }
    )
  },
  
  'Alarms.ack'() {
    Flag.update(
      { strVarName: "Ack" },
      { $set: { 
        'boCmd': true
      } }
    )
  }

})