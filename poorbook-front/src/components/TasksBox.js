import React, { useState, useEffect } from 'react';
import Modal from 'react-modal';
import axiosInstance from '../axiosInstance';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';

Modal.setAppElement('#root');

const TasksBox = () => {
  const [modalIsOpen, setModalIsOpen] = useState(false);
  const [title, setTitle] = useState('');
  const [desc, setDesc] = useState('');
  const [doneDate, setDoneDate] = useState(new Date());
  const [tasks, setTasks] = useState([]);

  useEffect(() => {
    const fetchTasks = async () => {
      try {
        const response = await axiosInstance.get('/tasks');
        if (response.data.statusCode === 200) {
          setTasks(response.data.content.result);
        }
      } catch (error) {
        console.error('Error fetching tasks:', error);
      }
    };

    fetchTasks();
  }, []);

  const openModal = () => setModalIsOpen(true);
  const closeModal = () => setModalIsOpen(false);

  const handleSubmit = async (e) => {
    e.preventDefault();

    const taskData = {
      taskTitle: title,
      taskDesc: desc,
      taskStatus: 'TODO',
      taskCreated: new Date().toISOString(),
      taskDonedate: doneDate.toISOString(),
    };

    try {
      await axiosInstance.post('/tasks', taskData);
      closeModal();
      const response = await axiosInstance.get('/tasks');
      if (response.data.statusCode === 200) {
        setTasks(response.data.content.result);
      }
    } catch (error) {
      console.error('There was an error creating the task!', error);
    }
  };

  return (
    <div className="box">
      <div className='title-container'>
        <h2>Active Tasks</h2>
        <button onClick={openModal} className="add-icon">+</button>
      </div>
      <ul className="tasks-list">
        {tasks.map((task) => (
          <li key={task.id} className="task-item">
            <div className='title-highlight'>
              <h3>{task.taskTitle}</h3>
            </div>
            <hr className='solid'/>
            <b>Description</b>
            <div className='description-highlight'>
            {task.taskDesc}
            </div> 
              <b>Status</b> 
              <div className='status-highlight'>
              {task.taskStatus}
              </div>
            <b>Done by </b>
            <div className='done-highlight'>
              {new Date(task.taskDonedate).toLocaleString()}
            </div>
            <p className='taskCreated'>Created: {new Date(task.taskCreated).toLocaleString()}</p>
          </li>
        ))}
      </ul>
      <Modal
        isOpen={modalIsOpen}
        onRequestClose={closeModal}
        contentLabel="Create Task"
        className="modal"
        overlayClassName="overlay"
      >
        <h2>Create Task</h2>
        <form onSubmit={handleSubmit}>
          <label>
            Task Title:
            <input 
              type="text" 
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              required 
            />
          </label>
          <label>
            Description (optional):
            <textarea 
              value={desc}
              onChange={(e) => setDesc(e.target.value)}
            />
          </label>
          <label>
            Foreseen Done Date:
            <DatePicker 
              selected={doneDate} 
              onChange={(date) => setDoneDate(date)} 
              showTimeSelect
              timeFormat="HH:mm"
              timeIntervals={15}
              dateFormat="yyyy/MM/dd HH:mm"
              required 
            />
          </label>
          <button type="submit">Create Task</button>
        </form>
        <button onClick={closeModal}>Close</button>
      </Modal>
    </div>
  );
};

export default TasksBox;
