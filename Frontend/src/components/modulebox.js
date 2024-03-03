import '../App.css';
import * as React from 'react';
import Measuring from './measuring';
import { createTheme, colors, ThemeProvider } from '@mui/material';
import { useState, useEffect } from 'react';
import { v4 as uuidv4 } from 'uuid';

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
  //#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
    return (
      <div className="module-container">
        <h2 className="module-title">{title}</h2>
        {units.map((unitName, index1) => (
          <React.Fragment key={index1}>
            <div className='unit-name'>{unitName.slice(0, -1).toUpperCase() + '-' + unitName.slice(-1).toUpperCase()}</div>
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
                          status={Boolean(measuring[readoutName])}
                          button_status={status}
                          grafana_link={powering_dict[readoutName]["grafana-link"]}
                        />
                        <hr style={{ margin: '0.5px' }}></hr>
                      </div>
                    </React.Fragment>
                  ))}
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