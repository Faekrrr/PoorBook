import React, { useState, useEffect } from 'react';
import Modal from 'react-modal';
import DatePicker from 'react-datepicker';
import { FaEdit, FaTrash } from 'react-icons/fa';
import 'react-datepicker/dist/react-datepicker.css';
import axiosInstance from '../axiosInstance';

Modal.setAppElement('#root');

const EventsBox = () => {
  const [events, setEvents] = useState([]);
  const [modalIsOpen, setModalIsOpen] = useState(false);
  const [editModalIsOpen, setEditModalIsOpen] = useState(false);
  const [deleteModalIsOpen, setDeleteModalIsOpen] = useState(false);
  const [eventName, setEventName] = useState('');
  const [eventDate, setEventDate] = useState(new Date());
  const [eventPlace, setEventPlace] = useState('');
  const [currentEventId, setCurrentEventId] = useState(null);

  const fetchEvents = async () => {
    try {
      const response = await axiosInstance.get('/events');
      if (response.data.statusCode === 200) {
        setEvents(response.data.content.result);
      }
    } catch (error) {
      console.error('Error fetching events:', error);
    }
  };

  useEffect(() => {
    fetchEvents();
  }, []);

  const openModal = () => setModalIsOpen(true);
  const closeModal = () => setModalIsOpen(false);

  const openEditModal = (event) => {
    setCurrentEventId(event.id);
    setEventName(event.eventName);
    setEventDate(new Date(event.eventDate));
    setEventPlace(event.eventPlace);
    setEditModalIsOpen(true);
  };
  const closeEditModal = () => setEditModalIsOpen(false);

  const openDeleteModal = (eventId) => {
    setCurrentEventId(eventId);
    setDeleteModalIsOpen(true);
  };
  const closeDeleteModal = () => setDeleteModalIsOpen(false);

  const formatDate = (date) => {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    return `${year}-${month}-${day} ${hours}:${minutes}`;
  };

  const handleCreateSubmit = async (e) => {
    e.preventDefault();

    const eventData = {
      eventName,
      eventDate: formatDate(eventDate),
      eventPlace,
    };

    try {
      await axiosInstance.post('/events', eventData);
      fetchEvents(); // Refresh events after adding a new event
      closeModal();
    } catch (error) {
      console.error('There was an error creating the event!', error);
    }
  };

  const handleEditSubmit = async (e) => {
    e.preventDefault();

    const eventData = {
      eventName,
      eventDate: formatDate(eventDate),
      eventPlace,
    };

    try {
      await axiosInstance.put(`/events/${currentEventId}`, eventData);
      fetchEvents(); // Refresh events after editing an event
      closeEditModal();
    } catch (error) {
      console.error('There was an error updating the event!', error);
    }
  };

  const handleDelete = async () => {
    try {
      await axiosInstance.delete(`/events/${currentEventId}`);
      fetchEvents(); // Refresh events after deleting an event
      closeDeleteModal();
    } catch (error) {
      console.error('There was an error deleting the event!', error);
    }
  };

  return (
    <div className="box">
      <div className="title-container">
        <h2>Events</h2>
        <button onClick={openModal} className="add-icon">+</button>
      </div>
      <ul className="events-list">
        {events.map((event) => (
          <li key={event.id} className="event">
            <p className="event-name">
              {event.eventName}
              <div className="event-icons">
                <FaEdit className="icon" onClick={() => openEditModal(event)} />
                <FaTrash className="icon" onClick={() => openDeleteModal(event.id)} />
              </div>
            </p>
            <p className="event-place">{event.eventPlace}</p>
            <p className="event-date">{new Date(event.eventDate).toLocaleString()}</p>
            <p className="event-created">{new Date(event.eventCreated).toLocaleString()}</p>
          </li>
        ))}
      </ul>
      <Modal
        isOpen={modalIsOpen}
        onRequestClose={closeModal}
        contentLabel="Create Event"
        className="modal"
        overlayClassName="overlay"
      >
        <h2>Create Event</h2>
        <form onSubmit={handleCreateSubmit}>
          <label>
            Event Name:
            <input 
              type="text" 
              value={eventName}
              onChange={(e) => setEventName(e.target.value)}
              required 
            />
          </label>
          <label>
            Event Date:
            <DatePicker 
              selected={eventDate} 
              onChange={(date) => setEventDate(date)} 
              showTimeSelect
              timeFormat="HH:mm"
              timeIntervals={15}
              dateFormat="yyyy-MM-dd HH:mm"
              required 
            />
          </label>
          <label>
            Event Place:
            <input 
              type="text" 
              value={eventPlace}
              onChange={(e) => setEventPlace(e.target.value)}
              required 
            />
          </label>
          <button type="submit">Create Event</button>
        </form>
        <button onClick={closeModal}>Close</button>
      </Modal>
      <Modal
        isOpen={editModalIsOpen}
        onRequestClose={closeEditModal}
        contentLabel="Edit Event"
        className="modal"
        overlayClassName="overlay"
      >
        <h2>Edit Event</h2>
        <form onSubmit={handleEditSubmit}>
          <label>
            Event Name:
            <input 
              type="text" 
              value={eventName}
              onChange={(e) => setEventName(e.target.value)}
              required 
            />
          </label>
          <label>
            Event Date:
            <DatePicker 
              selected={eventDate} 
              onChange={(date) => setEventDate(date)} 
              showTimeSelect
              timeFormat="HH:mm"
              timeIntervals={15}
              dateFormat="yyyy-MM-dd HH:mm"
              required 
            />
          </label>
          <label>
            Event Place:
            <input 
              type="text" 
              value={eventPlace}
              onChange={(e) => setEventPlace(e.target.value)}
              required 
            />
          </label>
          <button type="submit">Save Changes</button>
        </form>
        <button onClick={closeEditModal}>Close</button>
      </Modal>
      <Modal
        isOpen={deleteModalIsOpen}
        onRequestClose={closeDeleteModal}
        contentLabel="Delete Event"
        className="modal"
        overlayClassName="overlay"
      >
        <h2>Are you sure you want to delete this event?</h2>
        <button onClick={handleDelete}>Delete</button>
        <button onClick={closeDeleteModal}>Close</button>
      </Modal>
    </div>
  );
};

export default EventsBox;
