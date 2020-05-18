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

  'Setpoint.update'(varName, val) {
    var value = parseFloat(val)
    Setpoint.update(
      { varName: varName },
      { $set: { 
        'setpoint.HMIVal': value
      } }
    )
  },
  
  'Logic.update'(varName, val) {
    var value =  Math.pow(2,parseInt(val))
    Logic.update(
      { varName: varName },
      { $set: { 
        'cmd': value
      } }
    )
  },
  
  'Button.update'(varName, index, val) {
    var value =  Math.pow(2,parseInt(index))*(+val)
    Button.update(
      { varName: varName },
      { $set: { 
        'cmd': value
      } }
    )
  },
  
  'Button.clear'(varName) {
    Button.update(
      { varName: varName },
      { $set: { 
        'cmd': 0,
        'wd': 0
      } }
    )
  },
  
  'Button.wd'(varName) {
    Button.update(
      { varName: varName },
      { $inc: { 
        'wd': 1
      } }
    )
  },
  
  'Alarms.ack'() {
    Flag.update(
      { varName: "Ack" },
      { $set: { 
        'boCmd': true
      } }
    )
  }

})