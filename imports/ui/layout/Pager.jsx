import React, { Component } from 'react'
import { Route, Switch, Redirect } from 'react-router-dom'
import { withTracker } from 'meteor/react-meteor-data'

import { Setpoint, Actual, Logic, Button, Alarm } from '/imports/api/vects'

import Home from '../pages/Home'
import Alarms from '../pages/Alarms'
import Advanced from '../pages/Advanced'



class Pager extends Component {
  constructor(props) {
    super(props)
    this.state = {
    }
  }

  static getDerivedStateFromProps(nextProps, prevState){
    if (nextProps.Alarm !== prevState.Alarm){
        
      //counting Alarms number
      var alarmsNumber = 0;
      Object.keys(nextProps.Alarm).map(key => {
        if (nextProps.Alarm[key].bySt != 0){alarmsNumber++}}
      )
      
      nextProps.returnAlarmsNumber(alarmsNumber)

    }
	  if (nextProps !== prevState) {
      
	    return {
	    	Setpoint: nextProps.Setpoint,
	    	Actual: nextProps.Actual,
	    	Logic: nextProps.Logic,
	    	Button: nextProps.Button,
	    	Alarm: nextProps.Alarm
	    }
	  }
	  return null
  }

  render() {
    var Data = {
      Actual: this.state.Actual.reduce((obj, item) => (obj[item.strVarName] = {...item}, obj), {}),
      Setpoint: this.state.Setpoint.reduce((obj, item) => (obj[item.strVarName] = {...item, updateSetpoint: (strVarName, val) => Meteor.call('Setpoint.update', strVarName, val)}, obj), {}),
      Logic: this.state.Logic.reduce((obj, item) => (obj[item.strVarName] = {...item, updateLogic: (strVarName, val) => Meteor.call('Logic.update', strVarName, val)}, obj), {}),
      Button: this.state.Button.reduce((obj, item) => (obj[item.strVarName] = {
        ...item,
        updateButton: (strVarName, index, boVal) => Meteor.call('Button.update', strVarName, index, boVal),
        clearButton: (strVarName) => Meteor.call('Button.clear', strVarName),
        wdButton: (strVarName) => Meteor.call('Button.wd', strVarName)
      }, obj), {}),
      Alarm: this.state.Alarm.reduce((obj, item) => (obj[item.strVarName] = {...item}, obj), {})
    }

    return (
      <Switch >
        <Redirect from='/main.html' to='/'/>
        <Route exact path="/" render={() => <Home {...Data} />}/>
        <Route path="/Alarms" render={() => <Alarms {...Data} />}/>
        <Route path="/Advanced" render={() => <Advanced {...Data} />}/>
      </Switch>
    )
  }
}
export default withTracker((props) => {
  

  return {
    Setpoint: Setpoint.find({}).fetch(),
    Actual: Actual.find({}).fetch(),
    Logic: Logic.find({}).fetch(),
    Button: Button.find({}).fetch(),
    Alarm: Alarm.find({}, { sort: { ts: -1 }}).fetch()
  }
})(Pager)
