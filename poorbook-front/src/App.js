// import React from 'react';
// import MainContainer from './components/MainContainer';
// import TopBar from './components/TopBar';
// import './App.css';

// function App() {
//   return (
//     <div className="App">
//       <TopBar />
//       <MainContainer />
//     </div>
//   );
// }

// export default App;


import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import MainContainer from './components/MainContainer';
import TopBar from './components/TopBar';

import TasksPage from './pages/TasksPage';
import EventsPage from './pages/EventsPage';
import LocalizatorPage from './pages/LocalizatorPage';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <TopBar />
        <div className="main-container">
          <MainContainer/>
          <div className="content">
            <Routes>
              <Route path='/tasks' element={TasksPage} />
              <Route path='/events' element={EventsPage} />
              <Route path='/localizator' element={LocalizatorPage} />
            </Routes>
          </div>
        </div>
      </div>
    </Router>
  );
}

export default App;