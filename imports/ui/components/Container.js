import React, { Component } from 'react'
import Card from '@material-ui/core/Card'
import Grid from '@material-ui/core/Grid'
import Typography from '@material-ui/core/Typography'
import { withStyles } from '@material-ui/core'

const CSSTypography = withStyles({
  root: {
    marginBottom: '16px'
  },
})(Typography)

const CSSCard = withStyles({
  root: {
    paddingLeft: '16px',
    paddingRight: '16px',
    paddingTop: '16px',
    paddingBottom: '12px'
  },
})(Card)

export default class Container extends Component {
  constructor(props) {
    super(props)
    this.state = { }
  }

  static getDerivedStateFromProps(props, state) {
    if (props.tag && (props.tag.strName !== state.strName)) {
      return { 
        strName: props.tag.strName
      }
    }
    return {}
  }
  render() {
    return (
      <Grid item>
        <CSSCard>
          <CSSTypography variant="subtitle1">{this.state.strName}</CSSTypography>
          {this.props.children}
        </CSSCard>
      </Grid>
    )
  }
}