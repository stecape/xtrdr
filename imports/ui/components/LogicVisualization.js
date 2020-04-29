import React, { Component } from 'react'
import Container from './Container'
import ButtonGroup from '@material-ui/core/ButtonGroup'
import Button from '@material-ui/core/Button'
import Grid from '@material-ui/core/Grid'
import { withStyles } from '@material-ui/core'


const CSSButtonGroup = withStyles({
  root: {
    marginTop: '7px',
    marginBottom: '19px',
    width: '100%'
  },
})(ButtonGroup)
const CSSButton = withStyles({
  root: {
    cursor: 'default'
  }
})(Button)
const CSSButtonActive = withStyles({
  root: {
    cursor: 'default',
    fontWeight: 'bold'
  }
})(Button)

export default class LogicVisualization extends Component {
  constructor(props) {
    super(props)
    this.state = {
      Name: '',
      varName: '',
      labels: ['Off', 'On'],
      st: 0,
      classe: 'LogicVisualization'
    }
    this.isActive = this.isActive.bind(this)
  }

  isActive = (index) => {
    return (this.state.st & Math.pow(2, index)) !== 0
  }

  static getDerivedStateFromProps(props, state) {
    if (props.tag && (props.tag !== state)) {
      return props.tag
    }
    return {}
  }

  render() {
    return (
      <Container tag={this.state}>        
        <div style={{minHeight: '80px',width: '100%'}} />
        <Grid item>
          <CSSButtonGroup
            size="large"
            disableFocusRipple={true}
            disableRipple={true}
          >
            {
              this.state.labels.map((item, index) =>{
                var active = this.isActive(index)
                return (
                  active ? (
                    <CSSButtonActive
                      key={item}
                      color='primary'
                    >
                      {item}
                    </CSSButtonActive>
                  ) : ( 
                    <CSSButton
                      key={item}
                    >
                      {item}
                    </CSSButton>
                  )
                )
              })
            }
          </CSSButtonGroup>
        </Grid>
      </Container>
    )
  }
}