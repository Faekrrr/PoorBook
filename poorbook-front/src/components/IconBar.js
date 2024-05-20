import React from 'react';

const IconBar = ({ icons }) => {
  return (
    <div className="icon-bar">
      {icons.map((icon, index) => (
        <a key={index} href={icon.linkTo}>
          {/* <img src={icon.iconUrl} alt={icon.name} />
           */}
          UU
        </a>
      ))}
    </div>
  );
};

export default IconBar;
