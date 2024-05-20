import React, { useState } from 'react';
import Modal from 'react-modal';
import axios from 'axios';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';

Modal.setAppElement('#root'); // This is important for accessibility

const TasksBox = () => {
  const [modalIsOpen, setModalIsOpen] = useState(false);
  const [title, setTitle] = useState('');
  const [desc, setDesc] = useState('');
  const [doneDate, setDoneDate] = useState(new Date());

  const openModal = () => setModalIsOpen(true);
  const closeModal = () => setModalIsOpen(false);

  const handleSubmit = (e) => {
    e.preventDefault();

    const taskData = {
      title,
      desc,
      doneDate,
      status: 'todo'
    };

    // axios.post('/api/create-task', taskData)
    //   .then(response => {
    //     console.log('Task created:', response.data);
    //     closeModal();
    //   })
    //   .catch(error => {
    //     console.error('There was an error creating the task!', error);
    //   });
  };

  return (
    <div className="box">
      <div className='title-container'>
      <h1>Tasks</h1>
      <button onClick={openModal} className="add-icon">+</button>
      </div>
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
            <h3>Description (optional):</h3>
            <input 
              value={desc}
              onChange={(e) => setDesc(e.target.value)}
            />
          </label>
          <label>
            Foreseen Done Date:
            <DatePicker 
              selected={doneDate} 
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
