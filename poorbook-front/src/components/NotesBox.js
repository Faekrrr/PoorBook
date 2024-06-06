import React, { useState } from 'react';
import axiosInstance from '../axiosInstance';

const NotesBox = () => {
  const [notes, setNotes] = useState([]);

  const handlePasteNote = async () => {
    try {
      const text = await navigator.clipboard.readText();
      if (text) {
        const noteData = { content: text };
        const response = await axiosInstance.post('/notes', noteData);
        if (response.status === 200) {
          // Optionally, update the notes state with the new note
          setNotes([...notes, response.data]);
        }
      }
    } catch (error) {
      console.error('Error reading clipboard content:', error);
    }
  };

  return (
    <div className="box">
      <div className='title-container'>
        <h2>Your pastebin</h2>
      </div>
      <button onClick={handlePasteNote} className="paste-note-button">Click me 2 times!</button>
      <hr className='solid'/>
      <ul className="notes-list">
        {notes.map((note, index) => (
          <li key={index} className="note">
            {note.content}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default NotesBox;
