import React, { Component } from 'react'
import Container from './Container'
import SetContent from './SetContent'

export default class Set extends Component {
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
      <Container {...this.props} >
        <SetContent {...this.props} />
      </Container>
    )
  }
}