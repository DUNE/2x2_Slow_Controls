import '../App.css';
import * as React from 'react';
import Button from '@mui/material/Button';
import { createTheme, colors, ThemeProvider } from '@mui/material';
import { useEffect } from 'react';

// GETTING SERVER NAME FROM PODMAN COMPOSE FILE
const prodServer = process.env.PROD_SERVER;

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
    },
    error:{
      main: colors.red[700]
    }
  }
})

// COMPONENT CONSTANT
const Card = ({ id, title, on_message, off_message, error_message, crate_status, grafana_links, error_status }) => {

  //#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
  //# BUTTON STATUS CONFIGURATION
  //#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
  console.log(grafana_links);

  //const [status, setStatus] = React.useState(false); // Initialize status
  const [clicked, setClicked] = React.useState();
  const handleClick = () => {
    setClicked((prevClicked) => !prevClicked);
    const endpoint = clicked ? `http://localhost:8000/other_units/${id}/turn-on` : `http://localhost:8000/other_units/${id}/turn-off`;
    fetch(endpoint, {method: "PUT"})
    .then(response => response.json())
    }

  useEffect(() => {
    setClicked(!crate_status);
  }, [crate_status]);
  
  const buttonStyle = {
    width: 82,
    height: 30,
    borderRadius: 5,
  };

  if (off_message === "Disabled") {
    buttonStyle.color = "disabled";
  }
  
  //#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
  //# RETURN CARD
  //#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
    return (
      <div className={error_status ? 'card-error' : (clicked ? 'card-off' : 'card-on')}>
        <div style={{display : 'flex', justifyContent : 'space-between', width : '100%'}}>
          <div className="card-title">{title.replace(/_/g, ' ')}</div>
          <div style={{marginTop : '8px', paddingRight : '8px'}}>
            <ThemeProvider theme={theme}>
              <div>
                <Button color={error_status ? 'error' : (clicked ? 'secondary' : 'primary')}
                        variant="contained"
                        style={buttonStyle}
                        onClick={handleClick}
                        disabled={title === "GIZMO"}>
                        {clicked ? 'OFF' : 'ON'}
                </Button>
              </div>
            </ThemeProvider>
          </div>
        </div>
        <p className={`${clicked ? 'card-text-off' : 'card-text-on'} ${error_status ? 'card-text-error' : ''}`}>
        {error_status ? error_message : (clicked ? off_message : on_message)}
        </p>
      
      {/* Map over the grafana_links and render only the links */}
      {Object.values(grafana_links).map(item => (
          <div key={item.measurements}>
            <div className="grafana-card">
              {item["grafana-link"] && (
                <a href={item["grafana-link"]} target="_blank" rel="noopener noreferrer">
                  <iframe src={item["grafana-link"]} frameBorder="0"></iframe>
                </a>
              )}
            </div>
          </div>
        ))
      }

      </div>
    );
  };

export default Card;