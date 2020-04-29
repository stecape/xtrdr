import React, { Component } from 'react'
import TextField from '@material-ui/core/TextField'
import InputAdornment from '@material-ui/core/InputAdornment'
import Grid from '@material-ui/core/Grid'
import { withStyles } from '@material-ui/core'


const CSSTextField = withStyles({
  root: {
    marginBottom: '12px',
    width: '100%',
    cursor: 'default',
    '& input': {
      cursor: 'default',    
    },
    '& p': {
      cursor: 'default',    
    },
    '& div': {
      cursor: 'default',    
    },
    '& label': {
      cursor: 'default',    
    }
  },

})(TextField)

export default class ActContent extends Component {

  constructor(props) {
    super(props)
    this.state = {
      Name: '',
      varName: '',
      limits: {
        HMIMin: 0,
        HMIMax: 0
      },
      actual: {
        PIVal: 0,
        HMIVal: 0
      },
      unit: '',
      decimals: 0,
      classe: 'Act',
      internalVal: 0
    }
  }

  static getDerivedStateFromProps(props, state) {
    if (props.tag && (props.tag !== state)) {
      return { 
        Name: props.tag.Name,
        varName: props.tag.varName,
        limits: props.tag.limits,
        classe: props.tag.classe,
        unit: props.tag.unit,
        decimals: props.tag.decimals,
        actual: props.tag.actual
      }
    }
    return {}
  }

  render() {
    return (
      <Grid item>
        <CSSTextField
          id={this.state.varName}
          name={this.state.Name}
          value={this.state.actual.HMIVal}
          type="number"
          variant="outlined"
          InputProps={{
            startAdornment: <InputAdornment position="start">{this.state.unit}</InputAdornment>,
            readOnly: true,
          }}
        />
      </Grid>
    )
  }
}