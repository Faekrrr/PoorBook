import React from 'react';
import HorizontalContainer from './HorizontalContainer';
import CustomCalendar from './Calendar';

const MainContainer = () => {
  return (
    <div className="main-container">
      <HorizontalContainer />
      <div className="calendar-holder">
        <CustomCalendar />
      </div>
    </div>
  );
};

export default MainContainer;
