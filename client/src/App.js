import React, { useState } from 'react';
import axios from 'axios';

import './App.css';

import ResultList from './components/ResultList';
import Search from './components/Search';
import { NavBar } from './components/NavBar';
import Card from '@mui/material/Card';

function App () {

  const [results, setResults] = useState([]);

  const search = async (query) => {
    try {
      const response = await axios({
        method: 'get',
        url: `${process.env.REACT_APP_LOCATION_SERVICE_URL}/location/search`,
        params: {
          query: query
        }
      });
      setResults(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
      }}
    >
      <NavBar/>
      <div style={{width:'85%', margin:'auto', marginTop: '2%', display:'flex'}}>
        <Card sx={{width: '20%', marginRight: '10px', height: "90vh"}}>
          <div style={{marginLeft:'15px', marginTop:'20px'}}>
            <span style={{color:'#26B0B2', fontWeight:'bold'}}>Select dataset</span>
            <ul style={{marginTop: '15px', listStyleType:'none'}}>
              <li style={{cursor:'pointer', color:'#5C7080'}} id='ccg-lookup'>CCG lookup</li>
            </ul>
            <span style={{color:'lightgray'}}>More data will be added here in due course</span>
          </div>
        </Card>
        <Card sx={{width: '80%'}}>
          <Search search={search} />
          <ResultList results={results}/>
        </Card>
      </div>
    </div>
  );
}

export default App;
