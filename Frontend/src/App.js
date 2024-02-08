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
        const Others_left = [];
        const Others_right = [];

        for (let i = 0; i < dict.length; i += 1) {
          const cardLeft = (
            <Card
              id={i}
              title={data[i]["unit"].toUpperCase()}
              on_message={data[i]["dictionary"]["on_message"]}
              off_message={data[i]["dictionary"]["off_message"]}
              error_message={data[i]["dictionary"]["error_message"]}
              crate_status={data[i]["crate_status"]}
              grafana_links={data[i]["dictionary"]["powering"]}
              error_status={data[i]["error_status"]}
            />
          );
        
          // const cardRight = (
          //   <Card
          //     id={i + 1}
          //     title={data[i + 1]["unit"].toUpperCase()}
          //     on_message={data[i + 1]["dictionary"]["on_message"]}
          //     off_message={data[i + 1]["dictionary"]["off_message"]}
          //     crate_status={data[i + 1]["crate_status"]}
          //   />
          // );
        
          // Check the title and push into the appropriate array
          if (data[i]["unit"].toUpperCase() === 'GIZMO' || data[i]["unit"].toUpperCase() === 'MPOD') {
            Others_left.push(cardLeft);
          } 
          // Don't forget to change this to newOthersData2.push([cardLeft, cardRight]);  
          newOthersData2.push([cardLeft]);
          //newOthersData2.push([cardLeft, cardRight]);
        }

        setOthersData2(newOthersData2);
      });
  };


        //for (let i = 0; i < dict.length; i += 2) {
        //  newOthersData2.push([
            //console.log(JSON.stringify(othersNames.length))
         //   <Card id={i}
         //         title={data[i]["unit"].toUpperCase()}
         //         on_message={data[i]["dictionary"]["on_message"]}
         //         off_message={data[i]["dictionary"]["off_message"]}
         //         crate_status={data[i]["crate_status"]}/>,
            //<Card id={i+1}
            //      title={data[i+1]["unit"].toUpperCase()}
            //      on_message={data[i+1]["dictionary"]["on_message"]}
            //      off_message={data[i+1]["dictionary"]["off_message"]}
            //      crate_status={data[i+1]["crate_status"]}/>,
         // ]);
        //}
        //setOthersData2(newOthersData2);
      //});
  //}

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
        for (let i = 0; i < dict.length; i += 1) {
          const numericPart = dict[i].match(/\d+/)[0]
          const numericValue = parseInt(numericPart, 10)
          //const formattedString = `Module ${numericValue}`;
          newModulesData2.push([
            <ModuleBox id={i}
                  title={`Module ${numericValue}`}
                  units={[data[dict[i]][i]["unit"]]}
                  crate_status={data[dict[i]][i]["crate_status"]}
                  measuring={data[dict[i]][i]["measuring_status"]}
                  grafana_links={data[dict[i]][i]["dictionary"]["powering"]}/>,
            //<ModuleBox id={i+1}
            //title={`Module ${numericValue+1}`}
            //units={[data[dict[i+1]][i+1]["unit"]]}
            //crate_status={data[dict[i+1]][i+1]["crate_status"]}
            //measuring={data[dict[i+1]][i+1]["measuring_status"]}/>,
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
        <div className="main_column">
          <Header />
          <CardList cardData={othersData2}/>
        </div>

        <div className="main_column">
          <div className="modules-row">
            {modulesData2.map((item, index) => (
            <div key={index} className="module-item">
              {item}
            </div>
            ))}
          </div>
        </div>

      </div>
    )
}

export default App;
