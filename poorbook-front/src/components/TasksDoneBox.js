import React from 'react';

const TasksDoneBox = ({ tasksDone }) => {
  return  <div className='tasks-done-container'>
            <div className="tasks-done-box">
              Tasks Done: {tasksDone}
            </div>
          </div>
};

export default TasksDoneBox;
