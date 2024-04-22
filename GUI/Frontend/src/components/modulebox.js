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
      main: colors.red[700]
    }
  }
})

// COMPONENT FUNCTION
function ModuleBox({ id, title, units, crate_status, measuring, powering_dict }) {

  const [status, setStatus] = useState();
  useEffect(() => {
    setStatus(crate_status);
  }, [crate_status]);

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
                  <Button color={!status ? 'secondary' : 'primary'}
                          variant="contained"
                          style={{Width: '30px', height: 30, borderRadius: 0, fontSize: 10}}
                          onClick={() => setStatus(!status)}
                          disabled={true}>
                          {!status ? 'Crate OFF' : 'Crate ON'}
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
                          button_status={status}    
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