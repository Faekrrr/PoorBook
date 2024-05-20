import React from 'react';

const ProgressBar = ({ percentage }) => {
  // ${percentage}
  return (
    <div className="progress-bar">
      PROGRESS {percentage}%
      <div className="progress" style={{ width: `50%` }}> &nbsp; </div>

    </div>
  );
};

export default ProgressBar;
