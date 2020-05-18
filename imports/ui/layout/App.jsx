import React, { Component } from 'react'
import { Link } from 'react-router-dom'


import MenuListItems from './MenuListItems'
import Pager from './Pager'

import Drawer from '@material-ui/core/Drawer'
import List from '@material-ui/core/List'
import Paper from '@material-ui/core/Paper'
import { withStyles } from '@material-ui/core/styles'
import AppBar from '@material-ui/core/AppBar'
import Toolbar from '@material-ui/core/Toolbar'
import Typography from '@material-ui/core/Typography'
import IconButton from '@material-ui/core/IconButton'
import MenuIcon from '@material-ui/icons/Menu'
import Badge from '@material-ui/core/Badge'
import NotificationsIcon from '@material-ui/icons/Notifications'
import { MuiThemeProvider, createMuiTheme } from '@material-ui/core/styles'

const theme = createMuiTheme({
  palette: {
    primary: {
      light: '#f9683a',
      main: '#bf360c',
      dark: '#870000',
      contrastText: '#fff',
    },
    secondary: {
      light: '#a7c0cd',
      main: '#78909c',
      dark: '#4b636e',
      contrastText: '#f5f5f5',
    },
  },
})

const styles = {
  root: {
    flexGrow: 1,
  },
  flex: {
    flex: 1,
  },
  menuButton: {
    marginLeft: -12,
    marginRight: 20,
  },
  paperContent: {
    padding: 10,
    margin: 10,
  },
  paper: {
    margin: 8,
  }
}

class App extends Component {
  constructor(props) {
    super(props)
    this.state = {
      drawer: false,
      alarmsNumber: 0,
    }
    this.returnAlarmsNumber = this.returnAlarmsNumber.bind(this)
  }

  toggleDrawer = (open) => () => {
    this.setState({
      drawer: open
    })
  }

  returnAlarmsNumber = (numb) => {
    this.setState({alarmsNumber: numb})
  }

  render() {
    return (
      <MuiThemeProvider theme={theme}>
        <AppBar position="sticky">
          <Toolbar>
            <IconButton className={this.props.classes.menuButton} color="inherit" onClick={this.toggleDrawer(true)} >
              <MenuIcon />
            </IconButton>
            <Typography variant="h6" color="inherit" className={this.props.classes.flex}>
              xtrd
            </Typography>
            <IconButton component={Link} to="/Alarms" aria-label="show alarms" disabled={this.state.alarmsNumber==0} color="inherit">
              <Badge badgeContent={this.state.alarmsNumber} color="secondary">
                <NotificationsIcon />
              </Badge>
            </IconButton>
          </Toolbar>
        </AppBar>
        <div className={this.props.classes.paper}>
          <Paper>
            <Drawer open={this.state.drawer} onClose={this.toggleDrawer(false)}>
              <div
                tabIndex={0}
                onClick={this.toggleDrawer(false)}
                onKeyDown={this.toggleDrawer(false)}
              >
                <List><MenuListItems/></List>
              </div>
            </Drawer>
            <div className={this.props.classes.paperContent}>
              <Pager returnAlarmsNumber={this.returnAlarmsNumber}/>
            </div>
          </Paper>
        </div>
      </MuiThemeProvider>
    )
  }
}

export default withStyles(styles)(App)