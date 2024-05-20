import React, { useEffect, useState } from 'react';
import NotesBox from './NotesBox';
import EventsBox from './EventsBox';
import TasksBox from './TasksBox'
import IconBar from './IconBar';
import TasksDoneBox from './TasksDoneBox';
import ProgressBar from './ProgressBar';
import axios from 'axios';

const HorizontalContainer = () => {
  const [icons, setIcons] = useState([]);
  const [tasksDone, setTasksDone] = useState(0);
  const [tasksDonePerc, setTasksDonePerc] = useState(0);

  useEffect(() => {
    // Fetch icons
    // axios.get('/api/icons').then((response) => {
    //   setIcons(response.data);
    // });

    // // Fetch tasks done
    // axios.get('/api/tasks-done').then((response) => {
    //   setTasksDone(response.data.tasksDone);
    // });

    // // Fetch tasks done percentage
    // axios.get('/api/tasks-done-perc').then((response) => {
    //   setTasksDonePerc(response.data.tasksDonePerc);
    // });
  }, []);

  return (
    <div className="horizontal-container">
      <div className="top-row">
        <TasksBox />
        <EventsBox />
        <NotesBox />
      </div>
      <div className="middle-row">
        <IconBar icons={icons} />
        <TasksDoneBox tasksDone={tasksDone} />
      </div>
      <div className="bottom-row">
        <ProgressBar percentage={tasksDonePerc} />
      </div>
    </div>
  );
};

export default HorizontalContainer;
