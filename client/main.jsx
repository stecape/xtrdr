import React from 'react';
import { Meteor } from 'meteor/meteor';
import { render } from 'react-dom';
import { BrowserRouter } from 'react-router-dom'
import CssBaseline from '@material-ui/core/CssBaseline';
import App from '/imports/ui/layout/App';

Meteor.startup(() => {
  render(
  <BrowserRouter>
    <CssBaseline />
    <App />
  </BrowserRouter>, 
document.getElementById('root'));
});