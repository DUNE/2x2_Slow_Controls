import '../App.css';

function Header() {
  
  //#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
  //# RETURN PAGE HEADER
  //#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
    return (
        <div className="title-container">
          <div className="twobytwo-image"></div>
          <div>
            <p className="title">Slow Controls Room</p>
            <p className="subtitle">Monitoring and control tool</p>
          </div>
        </div>
      );
}

export default Header;