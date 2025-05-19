import React from 'react';
import ChartsGrid from './components/ChartsGrid';

const App: React.FC = () => {
  return (
    <div className="App">
      <h1>CS:GO Match Statistics</h1>
      <ChartsGrid />
    </div>
  );
};

export default App;