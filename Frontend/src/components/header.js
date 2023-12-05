import '../App.css';

function Header() {
  
  //#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
  //# RETURN PAGE HEADER
  //#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
    return (
        <div className="title-container">
        <div>
        <p className="title">2x2 Slow Controls Configuration Room</p>
        <p className="subtitle">Turn ON/OFF each unit by pressing the toggle switches. To monitor the output data in real-time go to&nbsp;
         <a href="localhost:3000" class="custom-link">Grafana</a>
        .</p>
        </div>
        <div className="title-image"></div>
        </div>
      );
}

export default Header;