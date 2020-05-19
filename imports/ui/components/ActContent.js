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
      strVarName: '',
      strName: '',
      strUnit: '',
      inDecimals: 0,
      Limits: {
        reMin: 0,
        reMax: 0
      },
      Act: {
        reHMIVal: 0,
        inHMIVal: 0
      },
      internalVal: 0
    }
  }

  static getDerivedStateFromProps(props, state) {
    if (props.tag && (props.tag !== state)) {
      return { 
        strName: props.tag.strName,
        strVarName: props.tag.strVarName,
        Limits: props.tag.Limits,
        strUnit: props.tag.strUnit,
        inDecimals: props.tag.inDecimals,
        Act: props.tag.Act
      }
    }
    return {}
  }

  render() {
    return (
      <Grid item>
        <CSSTextField
          id={this.state.strVarName}
          name={this.state.strName}
          value={this.state.Act.reHMIVal}
          type="number"
          variant="outlined"
          InputProps={{
            startAdornment: <InputAdornment position="start">{this.state.strUnit}</InputAdornment>,
            readOnly: true,
          }}
        />
      </Grid>
    )
  }
}