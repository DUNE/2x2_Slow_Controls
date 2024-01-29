import '../App.css';
import * as React from 'react';
import Button from '@mui/material/Button';
import { createTheme, colors, ThemeProvider } from '@mui/material';
import { useEffect } from 'react';

// SETTING UP BUTTON THEME
const theme = createTheme({
  palette : {
    primary:{
      main: colors.green[700]
    },
    secondary:{
      main: colors.red[700]
    },
    disabled:{
      main: colors.red[700]
    }
  }
})

// COMPONENT CONSTANT
const Card = ({ id, title, on_message, off_message, crate_status }) => {

  //#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
  //# BUTTON STATUS CONFIGURATION
  //#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---

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
    borderRadius: 0,
  };

  if (off_message === "Disabled") {
    buttonStyle.color = "disabled";
  }
  
  //#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
  //# RETURN CARD
  //#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
    return (
      <div className={clicked ? 'card-off' : 'card-on'}>
        <div style={{display : 'flex', justifyContent : 'space-between', width : '100%'}}>
          <div className="card-title">{title}</div>
          <div style={{marginTop : '8px', paddingRight : '8px'}}>
            <ThemeProvider theme={theme}>
              <div>
                <Button color={clicked ? 'secondary' : 'primary'}
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
        <p className={clicked ? 'card-text-off' : 'card-text-on'}>
        {clicked ? off_message : on_message}
        <iframe src="http://localhost:3000/d-solo/PgnNuQSIz/gizmo-minos?orgId=1&from=1706551252427&to=1706554852427&panelId=8" width="180" height="100" frameborder="0"></iframe>
        <iframe src="http://localhost:3000/d-solo/PgnNuQSIz/gizmo-minos?orgId=1&from=1706549605348&to=1706553205348&panelId=6" width="180" height="100" frameborder="0"></iframe>
        <iframe src="http://localhost:3000/d-solo/PgnNuQSIz/gizmo-minos?orgId=1&from=1706553251222&to=1706556851223&panelId=4" width="180" height="100" frameborder="0"></iframe>
        <iframe src="http://localhost:3000/d-solo/PgnNuQSIz/gizmo-minos?orgId=1&from=1706553278073&to=1706556878073&panelId=10" width="180" height="100" frameborder="0"></iframe>
        <iframe src="http://localhost:3000/d-solo/PgnNuQSIz/gizmo-minos?orgId=1&from=1706553300710&to=1706556900711&panelId=12" width="180" height="100" frameborder="0"></iframe>
        </p>
      </div>
    );
  };

export default Card;