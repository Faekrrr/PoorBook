import React, { useState } from 'react';
import Modal from 'react-modal';
import axios from 'axios';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';

Modal.setAppElement('#root'); // This is important for accessibility

const EventsBox = () => {
  const [modalIsOpen, setModalIsOpen] = useState(false);
  const [title, setTitle] = useState('');
  const [place, setPlace] = useState('');
  const [dateFrom, setDateFrom] = useState(new Date());
  const [dateTo, setDateTo] = useState(new Date());
  const [desc, setDesc] = useState('');

  const openModal = () => setModalIsOpen(true);
  const closeModal = () => setModalIsOpen(false);

  const handleSubmit = (e) => {
    e.preventDefault();

    const eventData = {
      title,
      place,
      dateFrom,
      dateTo,
      desc
    };

    // axios.post('/api/create-event', eventData)
    //   .then(response => {
    //     console.log('Event created:', response.data);
    //     closeModal();
    //   })
    //   .catch(error => {
    //     console.error('There was an error creating the event!', error);
    //   });
  };

  return (
    <div className="box">
      <div className="title-container">
        <h1>Events</h1>
        <button onClick={openModal} className="add-icon">+</button>
      </div>

      <Modal
        isOpen={modalIsOpen}
        onRequestClose={closeModal}
        contentLabel="Create Event"
        className="modal"
        overlayClassName="overlay"
      >
        <h2>Create Event</h2>
        <form onSubmit={handleSubmit}>
          <label>
            <h3>Event Title:</h3>
            <input 
              type="text" 
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              required 
            />
          </label>
          <label>
            <h3>Place / Link:</h3>
            <input 
              type="text" 
              value={place}
              onChange={(e) => setPlace(e.target.value)}
              required 
            />
          </label>
          <label>
            <h3>Date From:</h3>
            <DatePicker 
              selected={dateFrom} 
              onChange={(date) => setDateFrom(date)} 
              dateFormat="yyyy/MM/dd"
              required 
            />
          </label>
          <label>
            <h3>Date To:</h3>
            <DatePicker 
              selected={dateTo} 
              onChange={(date) => setDateTo(date)} 
              dateFormat="yyyy/MM/dd"
              required 
            />
          </label>
          <label>
            <h3>Description:</h3>
            <input
              value={desc}
              onChange={(e) => setDesc(e.target.value)}
            />
          </label>
          <button type="submit">Create Event</button>
        </form>
        <button onClick={closeModal}>Close</button>
      </Modal>
    </div>
  );
};

export default EventsBox;
