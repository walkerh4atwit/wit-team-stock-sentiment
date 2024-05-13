import React from 'react';
import TopLinks from '../components/TopLinks'
import "../index.css"
import "../styles/App.css"

let App = () => {
  return (
    <>
      <div className="bg-gradient-to-t from-cyan-200 to-blue-500 App-header">
        <TopLinks/>
      </div>
      <div> 
        Yo
      </div>
    </>
  );
}

export default App;
