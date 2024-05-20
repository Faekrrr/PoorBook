import React, { useState, useEffect } from 'react';
import Calendar from 'react-calendar';
import Modal from 'react-modal';
import axios from 'axios';
import DatePicker from 'react-datepicker';
import 'react-calendar/dist/Calendar.css';
import 'react-datepicker/dist/react-datepicker.css';

Modal.setAppElement('#root');

const CustomCalendar = () => {
  const [events, setEvents] = useState([]);
  const [selectedEvent, setSelectedEvent] = useState(null);
  const [editModalIsOpen, setEditModalIsOpen] = useState(false);
  const [eventModalIsOpen, setEventModalIsOpen] = useState(false);

  useEffect(() => {
    // axios.get('/api/events').then((response) => {
    //   setEvents(response.data);
    // });
  }, []);

  const openEventModal = (event) => {
    setSelectedEvent(event);
    setEventModalIsOpen(true);
  };

  const closeEventModal = () => {
    setEventModalIsOpen(false);
  };

  const openEditModal = () => {
    setEditModalIsOpen(true);
  };

  const closeEditModal = () => {
    setEditModalIsOpen(false);
  };

  const handleEditSubmit = (event) => {
    event.preventDefault();
    // Handle event edit submission logic
    closeEditModal();
    closeEventModal();
  };

  const renderEvents = (date) => {
    const dayEvents = events.filter(
      (event) =>
        new Date(event.dateFrom).toDateString() === date.toDateString() ||
        new Date(event.dateTo).toDateString() === date.toDateString()
    );

    return (
      <div className="events">
        {dayEvents.map((event, index) => (
          <div
            key={index}
            className={`event ${
              new Date(event.dateFrom).toDateString() === date.toDateString() &&
              new Date(event.dateTo).toDateString() !== date.toDateString()
                ? 'start-event'
                : new Date(event.dateTo).toDateString() === date.toDateString() &&
                  new Date(event.dateFrom).toDateString() !== date.toDateString()
                ? 'end-event'
                : 'single-day-event'
            }`}
            onClick={() => openEventModal(event)}
          >
            {event.title}
          </div>
        ))}
      </div>
    );
  };

  return (
    <div className="calendar-container">
      <Calendar tileContent={({ date }) => renderEvents(date)} />

      {selectedEvent && (
        <Modal
          isOpen={eventModalIsOpen}
          onRequestClose={closeEventModal}
          contentLabel="Event Details"
          className="modal"
          overlayClassName="overlay"
        >
          <h2>
            {selectedEvent.title}
            <button onClick={openEditModal} className="edit-icon">✏️</button>
          </h2>
          <p><strong>Place:</strong> {selectedEvent.place}</p>
          <p><strong>Date From:</strong> {new Date(selectedEvent.dateFrom).toLocaleString()}</p>
          <p><strong>Date To:</strong> {new Date(selectedEvent.dateTo).toLocaleString()}</p>
          <p><strong>Description:</strong> {selectedEvent.desc}</p>
          <button onClick={closeEventModal}>Close</button>
        </Modal>
      )}

      {selectedEvent && (
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
              Event Title:
              <input type="text" defaultValue={selectedEvent.title} required />
            </label>
            <label>
              Place:
              <input type="text" defaultValue={selectedEvent.place} required />
            </label>
            <label>
              Date From:
              <DatePicker
                selected={new Date(selectedEvent.dateFrom)}
                onChange={(date) => setSelectedEvent({ ...selectedEvent, dateFrom: date })}
                showTimeSelect
                timeFormat="HH:mm"
                timeIntervals={15}
                dateFormat="yyyy/MM/dd HH:mm"
                timeCaption="Time"
                required
              />
            </label>
            <label>
              Date To:
              <DatePicker
                selected={new Date(selectedEvent.dateTo)}
                onChange={(date) => setSelectedEvent({ ...selectedEvent, dateTo: date })}
                showTimeSelect
                timeFormat="HH:mm"
                timeIntervals={15}
                dateFormat="yyyy/MM/dd HH:mm"
                timeCaption="Time"
                required
              />
            </label>
            <label>
              Description:
              <textarea defaultValue={selectedEvent.desc} />
            </label>
            <button type="submit">Save Changes</button>
          </form>
          <button onClick={closeEditModal}>Close</button>
        </Modal>
      )}
    </div>
  );
};

export default CustomCalendar;
