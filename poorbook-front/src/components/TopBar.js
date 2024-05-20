import React from 'react';
import logo from '../assets/poortaskslogo.png';

const TopBar = () => {
  return (
    <div className="top-bar">
      <img src={logo} alt="Poor Tasks Logo" className="logo" />
      <h1>Poor Tasks</h1>
      {/* You can add more content here, such as navigation links or icons */}
    </div>
  );
};

export default TopBar;