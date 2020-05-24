import React, { Component } from 'react'
import Typography from '@material-ui/core/Typography'
import Setpoint from "../components/Set"
import Actual from "../components/Act"
import SetAct from "../components/SetAct"
import LogicSelection from "../components/LogicSelection"
import LogicButton from "../components/LogicButton"
import LogicVisualization from "../components/LogicVisualization"
import Grid from '@material-ui/core/Grid'


export default class Advanced extends Component {  
  constructor(props) {
    super(props)
    this.state = { 
    }
  }
  
  static getDerivedStateFromProps(nextProps, prevState){
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
    return (
      <div>
        <Typography variant="h4" color="inherit">
          Advanced
        </Typography>
        <Grid container spacing={3} >
          <Grid item xs={12} sm={6} md={4} lg={3} xl={2}>
            <Grid container spacing={1} direction="column" alignItems="stretch">
              <Setpoint tag={this.state.Setpoint.Speed0}/>
              <Setpoint tag={this.state.Setpoint.Speed1}/>
              <Setpoint tag={this.state.Setpoint.Speed2}/>
              <Setpoint tag={this.state.Setpoint.Speed3}/>
              <SetAct tagS={this.state.Setpoint.Speed4} tagA={this.state.Actual.Current4}/>
              <Actual tag={this.state.Actual.Current0}/>
              <Actual tag={this.state.Actual.Current1}/>
              <Actual tag={this.state.Actual.Micrometer1}/>
              <Actual tag={this.state.Actual.Current3}/>
              <Actual tag={this.state.Actual.CycleTime}/>
            </Grid>
          </Grid>
          <Grid item xs={12} sm={6} md={4} lg={3} xl={2}>
            <Grid container spacing={1} direction="column" alignItems="stretch">
              <LogicSelection tag={this.state.Logic.Motor0}/>
              <LogicSelection tag={this.state.Logic.Motor1}/>
              <LogicSelection tag={this.state.Logic.Motor2}/>
              <LogicSelection tag={this.state.Logic.Motor3}/>
              <LogicButton tag={this.state.Button.Jog0}/>
              <LogicButton tag={this.state.Button.Jog1}/>
              <LogicButton tag={this.state.Button.Jog2}/>
              <LogicButton tag={this.state.Button.Jog3}/>
              <LogicVisualization tag={this.state.Button.Jog4}/>
            </Grid>
          </Grid>
        </Grid>
      </div>
    )
  }
}