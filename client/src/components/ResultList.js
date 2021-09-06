import React from 'react';

import { Card, Table } from 'react-bootstrap';

function ResultList ({ results }) {
  const resultItems = results.map(result =>
    <Card className='mb-3' key={result.id}>
      <Card.Body>
        <Card.Title>{result.ccg_name}</Card.Title>
        <Card.Text>
          <Table striped bordered hover size="sm">
            <thead>
              <tr>
                <th></th>
                <th>Code</th>
                <th>Name</th>
                <th>CDH</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>CCG</strong></td>
                <td>{result.ccg_code}</td>
                <td>{result.ccg_name}</td>
                <td></td>
              </tr>
              <tr>
                <td><strong>STP</strong></td>
                <td>{result.stp_code}</td>
                <td>{result.stp_name}</td>
                <td>{result.stp_cdh}</td>
              </tr>
              <tr>
                <td><strong>Region</strong></td>
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