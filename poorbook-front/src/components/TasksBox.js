import React, { useState, useEffect } from 'react';
import Modal from 'react-modal';
import axios from 'axios';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';

Modal.setAppElement('#root');

const TasksBox = () => {
  const [modalIsOpen, setModalIsOpen] = useState(false);
  const [taskTitle, setTitle] = useState('');
  const [taskDesc, setDesc] = useState('');
  const [taskDonedate, setDoneDate] = useState(new Date());
  const [tasks, setTasks] = useState([]);

  // Axios instance with default headers
  const axiosInstance = axios.create({
    baseURL: "http://localhost:8000/api/v1/",
    headers: {
      'X-API-KEY': 'ioxnsaunxa'
    }
  });

  useEffect(() => {
    // Fetch tasks from the backend when the component mounts
    const fetchTasks = async () => {
      let data = JSON.stringify({});
      try {
        const response = await axiosInstance.get('/tasks', { data: {} });
        if (response.data.status === 200) {
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

  const handleSubmit = (e) => {
    e.preventDefault();

    const taskData = {
      taskTitle,
      taskDesc,
      taskDonedate,
      taskStatus: 'IN_PROGRESS'
    };

    axiosInstance.post('/tasks', taskData)
      .then(response => {
        console.log('Task created:', response.data);
        closeModal();
      })
      .catch(error => {
        console.error('There was an error creating the task!', error);
      });
  };

  return (
    <div className="box">
      <h2>Tasks</h2>
      <button onClick={openModal} className="add-icon">+</button>
      <ul className="tasks-list">
        {tasks.map(task => (
          <li key={task.id} className="task-item">
            <h3>{task.taskTitle}</h3>
            <p>{task.taskDesc}</p>
            <p><b>Status</b>: {task.taskStatus}</p>
            <p><b>Created</b>: {new Date(task.taskCreated).toLocaleString()}</p>
            <p><b>Done by</b>: {new Date(task.taskDonedate).toLocaleString()}</p>
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
              value={taskTitle}
              onChange={(e) => setTitle(e.target.value)}
              required 
            />
          </label>
          <label>
            Description (optional):
            <textarea 
              value={taskDesc}
              onChange={(e) => setDesc(e.target.value)}
            />
          </label>
          <label>
            Foreseen Done Date:
            <DatePicker 
              selected={taskDonedate} 
              onChange={(date) => setDoneDate(date)} 
              dateFormat="yyyy/MM/dd"
              required 
            />
          </label>
          <label>
            Status:
            <input 
              type="checkbox" 
              checked 
              readOnly 
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