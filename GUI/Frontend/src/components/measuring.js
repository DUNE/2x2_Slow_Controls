import '../App.css';
import * as React from 'react';
import Button from '@mui/material/Button';
import { createTheme, colors, ThemeProvider } from '@mui/material';
import { useEffect } from 'react';

// GET BACKEND URL
const BACKEND_URL = process.env.REACT_APP_HOST_IP_ADDRESS;

// SETTING UP BUTTON THEME
const theme = createTheme({
    palette : {
      primary:{
        main: colors.green[700]
      },
      secondary:{
        main: colors.grey[500]
      },
      disabled:{
        main: colors.grey[700]
      }
    }
  })

// COMPONENT CONSTANT
const Measuring= ({ id, powering, channel, device_names, status, button_status }) => {
  //#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
  //# BUTTON STATUS CONFIGURATION
  //#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
  const [clicked, setClicked] = React.useState(!status);
  
  useEffect(() => {
    if (button_status === false){
      setClicked(!button_status);
    }
    
  }, [button_status]);

  useEffect(() => {
    setClicked(!status);
  }, [status]);

  const handleClick = () => {
    const message = "Are you sure you want to turn " + (status ? "OFF" : "ON") + " the " + device_names.split('-')[1].split('_').join(' ');
    const confirmed = window.confirm(message);
    if (confirmed) {
      setClicked((prevClicked) => !prevClicked);
      const endpoint = clicked ? `${BACKEND_URL}/attached_units/${id}/${powering}/${channel}/turn-on` : `${BACKEND_URL}/attached_units/${id}/${powering}/${channel}/turn-off`;
      fetch(endpoint, {method: "PUT"})
      .then(response => response.json())
      }
    }
  
  //#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
  //# RETURN MEASURING ROW
  //#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
  
  // Add this to the grafana link section
  // {grafana_link.map((link, index) => (
  //   <iframe key={index} src={link} frameBorder="0"></iframe>
  // ))}
  // This was at the beggining
  // <iframe src={grafana_link} frameBorder="0"></iframe>
  
  return (
      <div>
      <div className={clicked ? 'measuring-row-off' : 'measuring-row-on'}>
        <div className='measuring'>
          {device_names.split('-')[1].split('_').join(' ')}
        </div>
        <ThemeProvider theme={theme}>
        <div> 
          <Button color={clicked ? 'secondary' : 'primary'}
                  variant="contained"
                  style={{Width: '30px', height: 30, borderRadius: 0, fontSize: 10}}
                  onClick={handleClick}
                  disabled={!button_status}>
                  {clicked ? 'OFF' : 'ON'}
          </Button>
        </div>
        </ThemeProvider>
      </div>
      </div>

  )
}

export default Measuring;