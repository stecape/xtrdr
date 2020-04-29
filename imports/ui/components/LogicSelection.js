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
  }
})(ButtonGroup)

export default class LogicSelection extends Component {
  constructor(props) {
    super(props)
    this.state = {
      Name: '',
      varName: '',
      labels: ['On', 'Off'],
      cmd: 0,
      st: 0,
      classe: 'LogicSelection'
    }
    this.isActive = this.isActive.bind(this)
    this.logicSelection = this.logicSelection.bind(this)
  }

  isActive = (index) => {
    return (this.state.st & Math.pow(2, index)) !== 0
  }

  logicSelection = (index) => {
    this.props.tag.updateLogic(this.state.varName, index)
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
        <Grid item>
          <CSSButtonGroup
            size="large"
          >
            {
              this.state.labels.map((item, index) =>{
                var active = this.isActive(index)
                return (
                  active ? (
                    <Button 
                      key={item}
                      color='primary'
                      variant='contained'
                      onClick={() => this.logicSelection(index)}
                    >
                      {item}
                    </Button>
                  ) : ( 
                    <Button 
                      key={item}
                      onClick={() => this.logicSelection(index)}
                    >
                      {item}
                    </Button>
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