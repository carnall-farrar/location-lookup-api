import React from 'react';

import { sanitize } from 'dompurify';
import { Card, Table } from 'react-bootstrap';

function ResultList ({ results }) {
  const resultItems = results.map(result =>
    <Card className='mb-3' key={result.id}>
      <Card.Body>
        <Card.Title>{result.ccg_name}</Card.Title>
        <Card.Subtitle className='mb-2 text-muted'>
          CCG Code: {result.ccg_code} | STP Code: {result.stp_code} | Region Code: {result.region_code}
        </Card.Subtitle>
        <Card.Text>
          <Table striped bordered hover size="sm">
            <thead>
              <tr>
                <th>Code</th>
                <th>Name</th>
                <th>CDH</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>{result.ccg_code}</td>
                <td>{result.ccg_name}</td>
                <td></td>
              </tr>
              <tr>
                <td>{result.stp_code}</td>
                <td>{result.stp_name}</td>
                <td>{result.stp_cdh}</td>
              </tr>
              <tr>
                <td>{result.region_code}</td>
                <td>{result.region_name}</td>
                <td>{result.region_cdh}</td>
              </tr>
            </tbody>
          </Table>
        </Card.Text>
      </Card.Body>
    </Card>
  );

  return (
    <div>
      {!results && <p>Search using the left panel.</p>}
      {results && results.length === 0 && <p>No results found.</p>}
      {resultItems}
    </div>
  );
}

export default ResultList;