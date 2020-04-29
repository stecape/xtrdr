import React, { Component } from 'react'
import { Link } from 'react-router-dom'
import { withRouter, matchPath } from 'react-router'
import MenuItem from '@material-ui/core/MenuItem'
import ListItemIcon from '@material-ui/core/ListItemIcon'
import ListItemText from '@material-ui/core/ListItemText'
import HomeIcon from '@material-ui/icons/Home'
import CachedIcon from '@material-ui/icons/Cached'

class MenuListItems extends Component {
  render () {
    var isSelected = (path) => {
      const match = !!matchPath(this.props.location.pathname, {
        path: path,
        exact: true,
        strict: false
      })
      return match
    }
    return(
      <div>
        <MenuItem button divider component={Link} to="/" selected={isSelected("/")} >
          <ListItemIcon>
            <HomeIcon />
          </ListItemIcon>
          <ListItemText primary="Home" />
        </MenuItem>
        <MenuItem button component={Link} to="/Advanced" selected={isSelected("/Advanced")}>
          <ListItemIcon>
            <CachedIcon />
          </ListItemIcon>
          <ListItemText primary="Advanced" />
        </MenuItem>
      </div>
    )
  }
}

export default withRouter(MenuListItems)