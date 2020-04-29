import React, { Component } from 'react'
import Container from './Container'
import Grid from '@material-ui/core/Grid'
import SetContent from './SetContent'
import ActContent from './ActContent'


export default class SetAct extends Component {
  constructor(props) {
    super(props)
    this.state = { }
  }

  static getDerivedStateFromProps(props, state) {
    if ((props.tagS && (props.tagS !== state.tagS)) || (props.tagA && (props.tagA !== state.tagA))) {
      return { 
        tagS: props.tagS,
        tagA: props.tagA
      }
    }
    return {}
  }
  render() {
    return (
      <Container tag={this.state.tagS} >
        <Grid container spacing={1}>
          <Grid item xs={6}>
            <SetContent tag={this.state.tagS} />
          </Grid> 
          <Grid item xs={6}> 
            <ActContent tag={this.state.tagA} />
          </Grid>
        </Grid>
      </Container>
    )
  }
}


//<div style={{minHeight: '12px',width: '100%'}} />