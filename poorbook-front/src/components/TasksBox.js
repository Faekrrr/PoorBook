import React, { useState, useEffect } from 'react';
import Modal from 'react-modal';
import axiosInstance from '../axiosInstance';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import { MdSettingsInputSvideo } from "react-icons/md";
import { FaEdit, FaTrash } from 'react-icons/fa';

Modal.setAppElement('#root');

const TasksBox = () => {
  const [modalIsOpen, setModalIsOpen] = useState(false);
  const [statusModalIsOpen, setStatusModalIsOpen] = useState(false);
  const [editModalIsOpen, setEditModalIsOpen] = useState(false);
  const [deleteModalIsOpen, setDeleteModalIsOpen] = useState(false);

  const [title, setTitle] = useState('');
  const [desc, setDesc] = useState('');
  const [doneDate, setDoneDate] = useState(new Date());
  const [tasks, setTasks] = useState([]);
  const [currentTaskId, setCurrentTaskId] = useState(null);
  const [currentStatus, setCurrentStatus] = useState('TODO');

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

  const openStatusModal = (taskId) => {
    setCurrentTaskId(taskId);
    setStatusModalIsOpen(true);
  };
  const closeStatusModal = () => setStatusModalIsOpen(false);

  const openEditModal = (task) => {
    setCurrentTaskId(task.id);
    setTitle(task.taskTitle);
    setDesc(task.taskDesc);
    setDoneDate(new Date(task.taskDonedate));
    setEditModalIsOpen(true);
  };
  const closeEditModal = () => setEditModalIsOpen(false);

  const openDeleteModal = (taskId) => {
    setCurrentTaskId(taskId);
    setDeleteModalIsOpen(true);
  };
  const closeDeleteModal = () => setDeleteModalIsOpen(false);

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

  const handleStatusSubmit = async (e) => {
    e.preventDefault();

    try {
      await axiosInstance.put(`/tasks/status/${currentTaskId}`, { taskStatus: currentStatus });
      closeStatusModal();
      const response = await axiosInstance.get('/tasks');
      if (response.data.statusCode === 200) {
        setTasks(response.data.content.result);
      }
    } catch (error) {
      console.error('There was an error updating the task status!', error);
    }
  };

  const handleEditSubmit = async (e) => {
    e.preventDefault();

    const taskData = {
      taskTitle: title,
      taskDesc: desc,
      taskStatus: 'TODO',
      taskCreated: new Date().toISOString(),
      taskDonedate: doneDate.toISOString(),
    };

    try {
      await axiosInstance.put(`/tasks/${currentTaskId}`, taskData);
      closeEditModal();
      const response = await axiosInstance.get('/tasks');
      if (response.data.statusCode === 200) {
        setTasks(response.data.content.result);
      }
    } catch (error) {
      console.error('There was an error updating the task!', error);
    }
  };

  const handleDelete = async () => {
    try {
      await axiosInstance.delete(`/tasks/${currentTaskId}`);
      closeDeleteModal();
      const response = await axiosInstance.get('/tasks');
      if (response.data.statusCode === 200) {
        setTasks(response.data.content.result);
      }
    } catch (error) {
      console.error('There was an error deleting the task!', error);
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
              <div className="tasks-icons">
                <MdSettingsInputSvideo className="icon" onClick={() => openStatusModal(task.id)} />
              <FaEdit className="icon" onClick={() => openEditModal(task)} />
              <FaTrash className="icon" onClick={() => openDeleteModal(task.id)} />
            </div>
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
            Task Title
            <input 
              type="text" 
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              required 
            />
          </label>
          <label>
            Short description
            <textarea
              type='text'
              value={desc}
              onChange={(e) => setDesc(e.target.value)}
              className='description'
            />
          </label>
          <label>
            Foreseen Done Date
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
        <button onClick={closeModal} className='close-button'>Close</button>
      </Modal>

      <Modal
        isOpen={statusModalIsOpen}
        onRequestClose={closeStatusModal}
        contentLabel="Set Task Status"
        className="modal"
        overlayClassName="overlay"
      >
        <h2>Set Task Status</h2>
        <form onSubmit={handleStatusSubmit}>
          <label>
            Status:
            <select value={currentStatus} onChange={(e) => setCurrentStatus(e.target.value)}>
              <option value="TODO">TODO</option>
              <option value="IN_PROGRESS">IN_PROGRESS</option>
              <option value="DONE">DONE</option>
              <option value="BLOCKED">BLOCKED</option>
            </select>
          </label>
          <button type="submit">Set</button>
        </form>
        <button onClick={closeStatusModal} className='close-button'>Close</button>
      </Modal>

      <Modal
        isOpen={editModalIsOpen}
        onRequestClose={closeEditModal}
        contentLabel="Edit Task"
        className="modal"
        overlayClassName="overlay"
      >
        <h2>Edit Task</h2>
        <form onSubmit={handleEditSubmit}>
          <label>
            Task Title
            <input 
              type="text" 
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              required 
            />
          </label>
          <label className='description-area'>
            Short description
            <textarea
              type='text'
              value={desc}
              onChange={(e) => setDesc(e.target.value)}
              className='description'
            />
          </label>
          <label>
            Foreseen Done Date
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
          <button type="submit">Edit Task</button>
        </form>
        <button onClick={closeEditModal} className='close-button'>Close</button>
      </Modal>

      <Modal
        isOpen={deleteModalIsOpen}
        onRequestClose={closeDeleteModal}
        contentLabel="Delete Task"
        className="modal"
        overlayClassName="overlay"
      >
        <h2>Are you sure you want to delete this task?</h2>
        <button onClick={handleDelete} className='deletion-confirmation-button'>Delete</button>
        <button onClick={closeDeleteModal} className='close-button'>Cancel</button>
      </Modal>
    </div>
  );
};

export default TasksBox;