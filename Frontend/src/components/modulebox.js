import '../App.css';
import * as React from 'react';
import Measuring from './measuring';
import { createTheme, colors, ThemeProvider } from '@mui/material';
import { useState, useEffect } from 'react';

// SETTING UP BUTTON THEME
const theme = createTheme({
  palette : {
    primary:{
      main: colors.green[700]
    },
    secondary:{
      main: colors.red[700]
    }
  }
})

// COMPONENT FUNCTION
function ModuleBox({ id, title, units, crate_status, measuring }) {

  const [status, setStatus] = useState();
  useEffect(() => {
    setStatus(crate_status);
  }, [crate_status]);
  
  //#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
  //# RETURN CARD
  //#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
    return (
      <div className="module-container">
        <h2 className="module-title">{title}</h2>
        {units.map((unitName, index) => (
          <React.Fragment key={index}>
            <div className='unit-name'>{unitName.slice(0, -1).toUpperCase() + '-' + unitName.slice(-1).toUpperCase()}</div>
            <div>
            {Object.keys(measuring).map((readoutName, index2) => (
              <React.Fragment key={index2}>
                <Measuring id={id}
                           title={readoutName}
                           status={Boolean(measuring[readoutName])}
                           button_status={status}/>
                <hr style={{margin : '0.5px'}}></hr>
              </React.Fragment>
            ))}  
            </div>
          </React.Fragment>
        ))}
      </div>
    );
  }

export default ModuleBox;