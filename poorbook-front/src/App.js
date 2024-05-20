import React from 'react';
import MainContainer from './components/MainContainer';
import TopBar from './components/TopBar';
import './App.css';

function App() {
  return (
    <div className="App">
      <TopBar />
      <MainContainer />
    </div>
  );
}

export default App;