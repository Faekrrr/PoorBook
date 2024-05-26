import React from 'react';
import { NavLink } from 'react-router-dom';
import { FaHome, FaTasks, FaCalendarAlt, FaMapMarkerAlt } from 'react-icons/fa'; // Import icons from react-icons

const Sidebar = () => {
  return (
    <div className="sidebar-outer">

        <div className="sidebar-inner">
        
        <div className='navigation-item'>
            <NavLink to="/" exact activeClassName="active">
                <FaHome size={30}/>
            </NavLink>
        </div>

        <div className='navigation-item'>
            <NavLink to="/tasks" activeClassName="active">
                <FaTasks size={30}/>
            </NavLink>
        </div>

        <div className='navigation-item'>
            <NavLink to="/events" activeClassName="active">
                <FaCalendarAlt size={30}/>
            </NavLink>
        </div>

        <div className='navigation-item'>
            <NavLink to="/localizator" activeClassName="active">
                <FaMapMarkerAlt size={30}/>
            </NavLink>
        </div>

        </div>
        
    </div>
  );
};

export default Sidebar;
