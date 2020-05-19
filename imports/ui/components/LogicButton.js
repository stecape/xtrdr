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

export default class LogicButton extends Component {
  constructor(props) {
    super(props)
    this.state = {
      strName: '',
      strVarName: '',
      strLabels: ["Cmd"],
      byCmd: 0,
      bySt: 0
    }
    this.isActive = this.isActive.bind(this)
    this.logicButton = this.logicButton.bind(this)
    this.logicButtonClear = this.logicButtonClear.bind(this)
    this.logicButtonWd = this.logicButtonWd.bind(this)
  }

  //metodo che verifica che il bottone di indice index sia attivo
  isActive = (index) => {    
    return (Math.pow(2,index)&this.state.bySt)!==0
  }

  //metodo che chiama l'aggiornamento del wd lato server
  logicButtonWd = () => {
    this.props.tag.wdButton(this.state.strVarName)
  }

  //metodo che gestisce il timeout: se il pulsante è attivo setta il timer, se il pulsante è disattivo distrugge il timer
  wdTimeout = (val) => {
    if(val) {
      this.wdTO = setInterval(this.logicButtonWd, 500)
    } else {
      clearInterval(this.wdTO)
    }
  }

  //metodo che gestisce l'aggiornamento del valore del pulsante lato server e chiama la gestione del watchdog
  logicButton = (index, val) => {
    this.props.tag.updateButton(this.state.strVarName, index, val)
    this.wdTimeout(val)
  }

  //metodo che elimina gli event listener e distrugge il timer in caso di refresh pagina o di unmount del componente o catastrofe: chiede al server di resettare tutti i button
  logicButtonClear = () => {
    window.removeEventListener('beforeunload', this.logicButtonClear)
    this.props.tag.clearButton(this.state.strVarName)
    clearInterval(this.wdTO)
  }

  //aggiornamento dello stato in caso di cambiamento nelle props
  static getDerivedStateFromProps(props, state) {
    if (props.tag && (props.tag !== state)) {
      return props.tag
    }
    return {}
  }

  //al mount del componente creo la variabile globale che ospiterà il timer del watchdog e creo l'event listener del refresh pagina
  componentDidMount(){
    this.wdTO = null
    window.addEventListener('beforeunload', this.logicButtonClear)
  }

  //chiamo il clear di event listener button e timer
  componentWillUnmount(){
    this.logicButtonClear()
  }

  render() {
    return (
      <Container tag={this.state}>
        <Grid item>
          <CSSButtonGroup
            size="large"
          >
            {
              this.state.strLabels.map((item, index) =>{
                var active = this.isActive(index)
                return (
                  active ? (
                    <Button 
                      key={item}
                      color='primary'
                      variant='contained'
                      onMouseDown={() => this.logicButton(index, true)}
                      onMouseUp={() => this.logicButton(index, false)}
                      onMouseOut={() => {if (this.isActive(index)) this.logicButton(index, false)}}
                    >
                      {item}
                    </Button>
                  ) : ( 
                    <Button 
                      key={item}
                      onMouseDown={() => this.logicButton(index, true)}
                      onMouseUp={() => this.logicButton(index, false)}
                      onMouseOut={() => {if (this.isActive(index)) this.logicButton(index, false)}}
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
