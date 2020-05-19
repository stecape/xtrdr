import React, { Component } from 'react'
import Container from './Container'
import ActContent from './ActContent'

export default class Act extends Component {
  constructor(props) {
    super(props)
    this.state = { }
  }

  static getDerivedStateFromProps(props, state) {
    if (props.tag && (props.tag.Name !== state.strName)) {
      return { 
        Name: props.tag.strName
      }
    }
    return {}
  }
  render() {
    return (
      <Container {...this.props} >
        <ActContent {...this.props} />
      </Container>
    )
  }
}