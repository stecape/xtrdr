import React, { Component } from 'react'
import Typography from '@material-ui/core/Typography'
import { styled } from '@material-ui/core/styles';

import ErrorIcon from '@material-ui/icons/Error'
import WarningIcon from '@material-ui/icons/Warning'
import FeedbackIcon from '@material-ui/icons/Feedback'
import DoneIcon from '@material-ui/icons/Done'

import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import { red, yellow, blue } from '@material-ui/core/colors'

import Fab from '@material-ui/core/Fab';


const Ack = styled(Fab)({
  position: 'absolute',
  bottom: 16,
  right: 16,
})

const columns = [
  { id: 'reaction', label: ''},
  { id: 'ts', label: 'Timestamp' },
  { id: 'VectIndex', label: 'ID' },
  { id: 'Name', label: 'Alarm', minWidth: 10 },
  {
    id: 'description',
    label: 'Description',
    minWidth: 170,
    format: (value) => value.toLocaleString('en-US'),
  },
  {
    id: 'st',
    label: 'Status',
    format: (value) => value.toLocaleString('en-US'),
  }
];

export default class Alarms extends Component {  
  constructor(props) {
    super(props)
    this.state = { 
    }
  }

  
  static getDerivedStateFromProps(nextProps, prevState){
	  if (nextProps.Alarm !== prevState.Alarm) {
	    return {
	    	Alarm: nextProps.Alarm
	    }
	  }
	  return null
  }
  
  getCell = (column, value, status) =>{
    switch (column.id){

      case "ts":
        var d = new Date (value)
        var datestring = d.getDate()  + "-" + (d.getMonth()+1) + "-" + d.getFullYear() + " " + d.getHours() + ":" + d.getMinutes() + ":" + d.getSeconds()
        return datestring
      case "reaction": 
        return this.getIcon(value, status)
      default:
        return column.format && typeof value === 'number' ? column.format(value) : value
    
    }
  }

  getIcon = (value, status) =>{
    switch(value) { 
      case 1:
      case 2:
      case 4: 
        return(
          status != 2 ?
            <ErrorIcon style={{ color: red[800] }}/>
          :
            <ErrorIcon color="disabled"/>
        )
        break
      case 3:  
        return(
          status != 2 ?
            <WarningIcon style={{ color: yellow[700] }}/>
          :
            <WarningIcon color="disabled"/>
        )
        break
      case 5:   
        return(
          status != 2 ?
            <FeedbackIcon style={{ color: blue[500] }}/>
          :
            <FeedbackIcon color="disabled"/>
        )
        break
    }
  }

  ack = () => {
    Meteor.call('Alarms.ack')
  }

  render() {
    return (
      <div>
      <Ack color="primary" aria-label="ack" onClick={this.ack}>
        <DoneIcon />
      </Ack>
        <Typography variant="h4" color="inherit">
          Alarms
        </Typography>

        <TableContainer>
        <Table stickyHeader aria-label="sticky table">
          <TableHead>
            <TableRow>
              {columns.map((column) => (
                <TableCell
                  key={column.id}
                  align={column.align}
                  style={{ minWidth: column.minWidth }}
                >
                  {column.label}
                </TableCell>
              ))}
            </TableRow>
          </TableHead>
          <TableBody>
            {Object.keys(this.state.Alarm).map((key, index) => {
              var alarm = this.state.Alarm[key]
              const status = alarm["st"];
              return (
                status != 0 ?
                  <TableRow hover role="checkbox" tabIndex={-1} key={index}>
                    {columns.map((column) => {
                      const value = alarm[column.id]
                      return (
                        <TableCell key={column.id} align={column.align} style={status!=2 ? {fontWeight:"bold"} : {} }>
                          {this.getCell(column, value, status)}
                        </TableCell>
                      );
                    })}
                  </TableRow>
                :
                  false
              );
            })}
          </TableBody>
        </Table>
      </TableContainer>

      </div>
    )
  }
}
