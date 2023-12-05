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
      }
    }
  })

// COMPONENT CONSTANT
const Measuring= ({ id, title, status, button_status }) => {

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
    setClicked((prevClicked) => !prevClicked);
    const endpoint = clicked ? `http://localhost:8000/attached_units/${id}/${title}/turn-on` : `http://localhost:8000/attached_units/${id}/${title}/turn-off`;
    fetch(endpoint, {method: "PUT"})
    .then(response => response.json())
    }

  // Setting up readout name
  const firstWord = title;
  const capitalizedFirstLetter = firstWord.charAt(0).toUpperCase();
  const restOfWord = firstWord.slice(1);
  const newTitle = `${capitalizedFirstLetter}${restOfWord} readout`;

  
  //#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
  //# RETURN MEASURING ROW
  //#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
  return (
      <div className={clicked ? 'measuring-row-off' : 'measuring-row-on'}>
        <div className='measuring'>
          {newTitle}
        </div>
        <ThemeProvider theme={theme}>
          <div style={{paddingLeft : '10px'}}> 
            <Button color={clicked ? 'secondary' : 'primary'}
                    variant="contained"
                    style={{width: 82, height: 30, borderRadius: 0}}
                    onClick={handleClick}
                    disabled={!button_status}>
                    {clicked ? 'OFF' : 'ON'}
            </Button>
          </div>
        </ThemeProvider>
      </div>
  )
}

export default Measuring;