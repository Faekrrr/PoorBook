import React from 'react';
import logo from '../assets/poortaskslogo.png';
import Sidebar from './Sidebar';

const TopBar = () => {
  return (
    <div className="top-bar">
      <img src={logo} alt="Poor Tasks Logo" className="logo" />
      <Sidebar />
    </div>
  );
};

export default TopBar;