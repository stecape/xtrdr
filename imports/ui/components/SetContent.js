import React, { Component } from 'react'
import TextField from '@material-ui/core/TextField'
import InputAdornment from '@material-ui/core/InputAdornment'
import Grid from '@material-ui/core/Grid'
import { withStyles } from '@material-ui/core'


const CSSTextField = withStyles({
  root: {
    marginBottom: '12px',
    width: '100%'
  },
})(TextField)

export default class SetContent extends Component {
  constructor(props) {
    super(props)
    this.state = {
      Name: '',
      varName: '',
      limits: {
        HMIMin: 0,
        HMIMax: 0
      },
      setpoint: {
        PIVal: 0,
        HMIVal: 0
      },
      unit: '',
      decimals: 0,
      classe: 'Set',
      internalVal: 0
    }

    this.handleChange = this.handleChange.bind(this)
    this.set = this.set.bind(this)
    this.handleFocusIn = this.handleFocusIn.bind(this)
  }

  handleChange = (event) => {
    this.setState({ internalVal: event.target.value })
  }


  set = (event) => {
    //chiamata a funzione di set lato Python
    event.preventDefault()
    event.stopPropagation()
    this.props.tag.updateSetpoint(this.state.varName, this.state.internalVal)
  }

  componentWillUnmount() {
    clearTimeout(this.timeOut)
  }

  handleFocusIn() {
    this.timeOut = setTimeout(() => { 
      this.setState({ internalVal: this.state.setpoint.HMIVal })
      this.inputDOM.blur()
    }, 20000)    
  }

  static getDerivedStateFromProps(props, state) {
    if (props.tag && (props.tag !== state)) {
      var obj = { 
        Name: props.tag.Name,
        varName: props.tag.varName,
        limits: props.tag.limits,
        classe: props.tag.classe,
        unit: props.tag.unit,
        decimals: props.tag.decimals,
        setpoint: props.tag.setpoint
      }
      if (props.tag.setpoint.HMIVal.toString() !== state.setpoint.HMIVal.toString()){
        obj["internalVal"] = props.tag.setpoint.HMIVal
      }
      return obj
    }
    return {}
  }

  render() {
    const inputProps = {
      step: 'any',
    }
    return (
      <Grid item>
        <form method="post" onSubmit={this.set}>
          <CSSTextField
            id={this.state.varName}
            name={this.state.Name}
            onFocus={this.handleFocusIn}
            inputRef={(inputDOM) => { this.inputDOM = inputDOM }}
            onChange={this.handleChange}
            value={this.state.internalVal}
            type="number"
            inputProps={inputProps}
            InputProps={{
              startAdornment: <InputAdornment position="start">{this.state.unit}</InputAdornment>,
            }}
            variant="filled"
          />
        </form>
      </Grid>
    )
  }
}