import React from 'react';

const CardList = ({ cardData }) => {
  return (
    <div id="card-container" style={{width: '100%'}}>
      {cardData.map((rowData, rowIndex) => (
        <div key={rowIndex} className="card-row">
          {rowData.map((cardContent, columnIndex) => (
            <div key={columnIndex}>
              {cardContent} 
            </div>
          ))}
        </div>
      ))}
    </div>
  );
};

export default CardList;
