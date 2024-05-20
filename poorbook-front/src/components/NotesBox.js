import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';

const NotesBox = () => {
  const [notes, setNotes] = useState([]);
  const [currentNote, setCurrentNote] = useState('');
  const inputRef = useRef(null);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (inputRef.current && !inputRef.current.contains(event.target)) {
        saveCurrentNote();
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [currentNote]);

  const saveCurrentNote = () => {
    if (currentNote.trim() === '') return;

    const newNote = {
      date: new Date().toLocaleString(),
      note: currentNote,
    };

    // axios.post('/api/create-note', newNote)
    //   .then(response => {
    //     setNotes([...notes, newNote]);
    //     setCurrentNote('');
    //   })
    //   .catch(error => {
    //     console.error('There was an error creating the note!', error);
    //   });
  };

  const handleKeyPress = (event) => {
    if (event.key === 'Enter') {
      event.preventDefault();
      saveCurrentNote();
    }
  };

  return (
    <div className="box">
        <div className="title-container">
        <h1>Pastebin</h1>
        </div>
        
      {notes.map((note, index) => (
        <div key={index} className="note">
            
          {note.note}
        </div>
      ))}
      <textarea
        ref={inputRef}
        value={currentNote}
        onChange={(e) => setCurrentNote(e.target.value)}
        onKeyPress={handleKeyPress}
        placeholder="Type a note..."
        className="note-input"
      />
    </div>
  );
};

export default NotesBox;
