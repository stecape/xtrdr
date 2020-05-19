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
      strVarName: '',
      strName: '',
      strUnit: '',
      inDecimals: 0,
      Limits: {
        reMin: 0,
        reMax: 0
      },
      Set: {
        reHMIVal: 0,
        inHMIVal: 0
      },
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
    this.props.tag.updateSetpoint(this.state.strVarName, this.state.internalVal)
  }

  componentWillUnmount() {
    clearTimeout(this.timeOut)
  }

  handleFocusIn() {
    this.timeOut = setTimeout(() => { 
      this.setState({ internalVal: this.state.Set.reHMIVal })
      this.inputDOM.blur()
    }, 20000)    
  }

  static getDerivedStateFromProps(props, state) {
    if (props.tag && (props.tag !== state)) {
      var obj = { 
        strName: props.tag.strName,
        strVarName: props.tag.strVarName,
        Limits: props.tag.Limits,
        strUnit: props.tag.strUnit,
        inDecimals: props.tag.inDecimals,
        Set: props.tag.Set
      }
      if (props.tag.Set.reHMIVal.toString() !== state.Set.reHMIVal.toString()){
        obj["internalVal"] = props.tag.Set.reHMIVal
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
            id={this.state.strVarName}
            name={this.state.strName}
            onFocus={this.handleFocusIn}
            inputRef={(inputDOM) => { this.inputDOM = inputDOM }}
            onChange={this.handleChange}
            value={this.state.internalVal}
            type="number"
            inputProps={inputProps}
            InputProps={{
              startAdornment: <InputAdornment position="start">{this.state.strUnit}</InputAdornment>,
            }}
            variant="filled"
          />
        </form>
      </Grid>
    )
  }
}