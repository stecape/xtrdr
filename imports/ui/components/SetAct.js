import React, { Component } from 'react'
import Container from './Container'
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
        <SetContent tag={this.state.tagS} />
        <div style={{minHeight: '12px',width: '100%'}} />
        <ActContent tag={this.state.tagA} />
      </Container>
    )
  }
}