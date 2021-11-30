import React, { useState } from 'react';

import axios from 'axios';
import { Formik } from 'formik';
import { Form } from 'react-bootstrap';
import Button from '@mui/material/Button';
import { AsyncTypeahead } from 'react-bootstrap-typeahead';
import DownloadIcon from '@mui/icons-material/Download';
import SearchIcon from '@mui/icons-material/Search';

function Search ({ search, handleDownloadClick }) {

    const [isLoading, setLoading] = useState(false);
    const [options, setOptions] = useState([]);

    const locationSearchWord = async query => {
        if (query.length < 3) {
            setLoading(false);
            setOptions([]);
        } else {
            setLoading(true);
            try {
                const response = await axios({
                    method: 'get',
                    url: `${process.env.REACT_APP_LOCATION_SERVICE_URL}/location/words`,
                    params: {
                        query: query
                    }
                });
                setOptions(response.data);
            } catch(error) {
                console.error(error);
                setOptions([]);
            } finally { 
                setLoading(false);
            }
        }
    };

    const onSubmit = async (values, actions) => {
        await search(
            values.query
        );
    };

    return (
        <Formik
        initialValues={{
            query: ''
        }}
        onSubmit={onSubmit}
        >
        {({
            handleChange,
            handleSubmit,
            setFieldValue,
            values
        }) => (
            <Form noValidate onSubmit={handleSubmit} style={{display:'flex', flexDirection:'row'}}>
            <Form.Group controlId='query' style={{width:'100%'}}>
                        <AsyncTypeahead
                            filterBy={() => true}
                            id="query"
                            isLoading={isLoading}
                            labelKey="word"
                            name="query"
                            onChange={selected => {
                                const value = selected.length > 0 ? selected[0].word : '';
                                setFieldValue('query', value);
                            }}
                            onInputChange={value => setFieldValue('query', value)}
                            onSearch={locationSearchWord}
                            options={options}
                            placeholder="Enter a search term (e.g. Manchester)"
                            type="text"
                            value={values.query}
                        />
            </Form.Group>
            <Form.Group>
                <Button 
                type='submit' 
                style={{backgroundColor:'#26B0B2', color: '#FFFF', border:'thin solid #26B0B2'}}
                endIcon={<SearchIcon />}
                >
                Search
                </Button>
            </Form.Group>
            <Form.Group>
                <Button 
                type='submit' 
                style={{backgroundColor:'#E30B9E', color: '#FFFF', border:'thin solid #E30B9E'}}
                endIcon={<DownloadIcon />}
                onClick={handleDownloadClick}
                >
                 Download
                </Button>
            </Form.Group>
            </Form>
        )}
        </Formik>
    );
}

export default Search;