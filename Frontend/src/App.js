import './App.css';
import Header from './components/header';
import Card from './components/card';
import CardList from './components/cardlist';
import ModuleBox from './components/modulebox';
import React, { useEffect } from 'react';

// SETTING UP MAIN FUNCTION APP
function App() {

  // CONTINUOS JSON AQUISITION OTHER UNITS
  const [othersData2, setOthersData2] = React.useState([]);

  const loadOthers = () => {
    fetch("http://localhost:8000/other_units")
      .then(response => response.json())
      .then(data => {
        // Get response JSON
        const dict = Object.keys(data);
        // Create modulesData based on modules_names,
        const newOthersData2 = [];
        for (let i = 0; i < dict.length; i += 2) {
          newOthersData2.push([
            //console.log(JSON.stringify(othersNames.length))
            <Card id={i}
                  title={data[i]["unit"].toUpperCase()}
                  on_message={data[i]["dictionary"]["on_message"]}
                  off_message={data[i]["dictionary"]["off_message"]}
                  crate_status={data[i]["crate_status"]}/>,
            //<Card id={i+1}
            //      title={data[i+1]["unit"].toUpperCase()}
            //      on_message={data[i+1]["dictionary"]["on_message"]}
            //      off_message={data[i+1]["dictionary"]["off_message"]}
            //      crate_status={data[i+1]["crate_status"]}/>,
          ]);
        }
        setOthersData2(newOthersData2);
      });
  }

  // CONTINUOS JSON AQUISITION ATTACHED UNITS
  const [modulesData2, setModulesData2] = React.useState([]);

  const loadAttached = () => {
    fetch("http://localhost:8000/attached_units2")
      .then(response => response.json())
      .then(data => {
        // Get response JSON
        const dict = Object.keys(data);
        // Create modulesData based on modules_names,
        const newModulesData2 = [];
        for (let i = 0; i < dict.length; i += 2) {
          const numericPart = dict[i].match(/\d+/)[0]
          const numericValue = parseInt(numericPart, 10)
          //const formattedString = `Module ${numericValue}`;
          newModulesData2.push([
            <ModuleBox id={i}
                  title={`Module ${numericValue}`}
                  units={[data[dict[i]][i]["unit"]]}
                  crate_status={data[dict[i]][i]["crate_status"]}
                  measuring={data[dict[i]][i]["measuring_status"]}/>,
            <ModuleBox id={i+1}
            title={`Module ${numericValue+1}`}
            units={[data[dict[i+1]][i+1]["unit"]]}
            crate_status={data[dict[i+1]][i+1]["crate_status"]}
            measuring={data[dict[i+1]][i+1]["measuring_status"]}/>,
          ])
        }
        setModulesData2(newModulesData2);
      });
  }

  // Loading both JSON files from API
  const loadData = () => {
    loadOthers();
    loadAttached();
  };

  // RELOAD JSON FILES EVERY 10 SECONDS
  useEffect(() => {
    // Fetch initial data
    loadData(); 
    // Set up polling every 10 seconds
    const intervalId = setInterval(loadData, 10000);
    // Clean up the interval when the component unmounts
    return () => clearInterval(intervalId);
  }, []);

  //#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
  //# RETURN DISPLAY
  //#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
    return (
      <div className="mother_container">
        <Header />
        <div className='title-container'>
          <div className='modules_group'>
            <div className='circle'>
              <CardList cardData={modulesData2}/>
            </div>
          </div>
          <div className='other_units_group'>
            <CardList cardData={othersData2}/>
          </div>
        </div>
      </div>
    )
}

export default App;
