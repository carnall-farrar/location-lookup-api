import React, { useState } from 'react';
import axios from 'axios';

import './App.css';

import { Col, Container, Row } from 'react-bootstrap';

import ResultList from './components/ResultList';
import Search from './components/Search';

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
    <Container className='pt-3'>
      <h1>Location Lookup</h1>
      <p className='lead'>
        Use the controls below to peruse the NHS location catalog and filter the results.
      </p>
      <Row>
        <Col lg={4}>
          <Search search={search} />
        </Col>
        <Col lg={8}>
          <ResultList results={results}/>
        </Col>
      </Row>
    </Container>
  );
}

export default App;
