import React, { useState, useEffect } from 'react';
import { FaCopy, FaTrash } from 'react-icons/fa';
import axiosInstance from '../axiosInstance';

const NotesBox = () => {
  const [notes, setNotes] = useState([]);
  const [copiedNoteId, setCopiedNoteId] = useState(null);

  const fetchNotes = async () => {
    try {
      const response = await axiosInstance.get('/notes');
      if (response.data.statusCode === 200) {
        setNotes(response.data.content.result);
      }
    } catch (error) {
      console.error('Error fetching notes:', error);
    }
  };

  useEffect(() => {
    fetchNotes();
  }, []);

  const handlePasteNote = async () => {
    try {
      const text = await navigator.clipboard.readText();
      if (text) {
        const noteData = { content: text };
        const response = await axiosInstance.post('/notes', noteData);
        if (response.status === 201) {
          fetchNotes(); // Refresh notes after pasting a new note
        }
      }
    } catch (error) {
      console.error('Error reading clipboard content:', error);
    }
  };

  const handleCopy = async (content, id) => {
    try {
      await navigator.clipboard.writeText(content);
      setCopiedNoteId(id);
      setTimeout(() => {
        setCopiedNoteId(null);
      }, 2000);
    } catch (error) {
      console.error('Error copying to clipboard:', error);
    }
  };

  const handleDelete = async (id) => {
    try {
      await axiosInstance.delete(`/notes/${id}`);
      fetchNotes(); // Refresh notes after deleting a note
    } catch (error) {
      console.error('Error deleting note:', error);
    }
  };

  return (
    <div className="box">
      <div className="title-container">
        <h2>Pastebin</h2>
        <button onClick={handlePasteNote} className="paste-note-button">Paste</button>
      </div>
      <ul className="notes-list">
        {notes.map((note) => (
          <li key={note.id} className="note">
            <div className="note-header">
              <p className="note-id">{note.id}</p>
              <div className="note-icons">
                <FaCopy className="icon" onClick={() => handleCopy(note.content, note.id)} />
                {copiedNoteId === note.id && <span className="copied-text">Copied</span>}
                <FaTrash className="icon" onClick={() => handleDelete(note.id)} />
              </div>
            </div>
            <p className="note-content">{note.content}</p>
            <p className="note-created">{new Date(note.created).toLocaleString()}</p>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default NotesBox;
