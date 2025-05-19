import React from 'react';
import ChartsGrid from './components/ChartsGrid';

const App: React.FC = () => {
  return (
    <div className="App">
      <h1>Game Statistics Dashboard</h1>
      <ChartsGrid />
    </div>
  );
};

export default App;