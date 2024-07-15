import '../App.css';
import * as React from 'react';
import Measuring from './measuring';
import { createTheme, colors, ThemeProvider } from '@mui/material';
import Button from '@mui/material/Button';
import { useState, useEffect } from 'react';

// SETTING UP BUTTON THEME
const theme = createTheme({
  palette : {
    primary:{
      main: colors.green[700]
    },
    secondary:{
      main: colors.grey[500]
    }
  }
})

// GET BACKEND URL
const BACKEND_URL = process.env.REACT_APP_HOST_IP_ADDRESS;

// COMPONENT FUNCTION
function ModuleBox({ id, title, units, crate_status, measuring, powering_dict }) {

  const [clicked, setClicked] = React.useState(!crate_status);

  useEffect(() => {
    if (crate_status === false){
      setClicked(!crate_status);
    }
    
  }, [crate_status]);

  useEffect(() => {
    setClicked(!crate_status);
  }, [crate_status]);

  const handleClick = () => {
    const message = "Are you sure you want to turn " + (crate_status ? "OFF" : "ON") + " the MPOD crate?";
    const confirmed = window.confirm(message);
    if (confirmed) {
      setClicked((prevClicked) => !prevClicked);
      const endpoint = clicked ? `${BACKEND_URL}/attached_units/${id}/turn-on-crate` : `${BACKEND_URL}/attached_units/${id}/turn-off-crate`;
      fetch(endpoint, {method: "PUT"})
      .then(response => response.json())
      }
    }

  //#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
  //# RETURN CARD
  //# Note: Crate status has been disabled temporarilly
  //#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
    return (
      <div className="module-container">
        <div className="module-title">{title}</div>

        {units.map((unitName, index1) => (
          <React.Fragment key={index1}>
              <div className='unit-row'>
              <div className='unit-name'>{unitName.slice(0, -1).toUpperCase() + '-' + unitName.slice(-1).toUpperCase()}</div>
              <ThemeProvider theme={theme}>
                <div> 
                  <Button color={!crate_status ? 'secondary' : 'primary'}
                          variant="contained"
                          style={{Width: '30px', height: 30, borderRadius: 0, fontSize: 10, boxShadow: 'none'}}
                          onClick={handleClick}
                          disabled={false}>
                          {!crate_status ? 'Crate OFF' : 'Crate ON'}
                  </Button>
                </div>
              </ThemeProvider>
              </div>
              <div>
              {Object.keys(powering_dict).map((readoutName, index2) => (
                <React.Fragment key={index2}>
                  <div className='readout-group-title'>{readoutName}</div>

                  <div style={{ display: 'flex', flexWrap: 'wrap' }}>
                  {Object.keys((measuring[readoutName])).map((channel, index3) => (
                    <React.Fragment key={index3}>
                      <div style={{ width: '50%' }}>
                        <Measuring
                          id={id}
                          powering={readoutName}
                          channel={channel}
                          device_names={powering_dict[readoutName]["channels"][channel]["name"]}
                          status={Boolean(measuring[readoutName][channel])}
                          button_status={crate_status}    
                        />
                        <hr style={{ margin: '0.5px' }}></hr>
                      </div>
                    </React.Fragment>
                    ))
                  }
                </div>
                <div className="grafana-card-module">
                  {powering_dict[readoutName]["grafana-link"] && powering_dict[readoutName]["grafana-link"].length > 0 && (
                    <a href={powering_dict[readoutName]["grafana-link"]} target="_blank" rel="noopener noreferrer">
                      <iframe src={powering_dict[readoutName]["grafana-link"]} frameBorder="0" height="240px"></iframe>
                    </a>
                  )}
                </div>

                </React.Fragment>
              ))}  
              </div>
          </React.Fragment>
        ))}
      </div>
    );
  }

export default ModuleBox;