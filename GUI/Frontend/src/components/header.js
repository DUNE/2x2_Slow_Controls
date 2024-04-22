import '../App.css';

function Header() {
  
  //#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
  //# RETURN PAGE HEADER
  //#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
    return (
        <div className="title-container">
          <div className="twobytwo-image"></div>
          <div>
            <p className="title">2x2 Slow Controls</p>
            <p className="subtitle">Remote control tool</p>
          </div>
        </div>
      );
}

export default Header;