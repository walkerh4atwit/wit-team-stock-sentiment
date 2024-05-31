import React from 'react'
import { Row, Col, Form, } from 'react-bootstrap'
import SearchBar from './SearchBar'
import "../styles/bg-gradient.css"

const MyForm = () => {
    const dropDownHandler = (option: any, onClick: () => void): JSX.Element => {
        return <div key={option} onClick={onClick}>{option}</div>
    }

    return (
        <Form className='my-Form-Gradient my-Form-Container'>
            <Row>
                <Form.Label column>
                    Step 1
                </Form.Label>
                <Form.Label column>
                    Step 2
                </Form.Label>
                <Form.Label column>
                    Step 3
                </Form.Label>
            </Row>
            <Row>
                <Form.Group as={Col} style={{'padding': '1rem'}}>
                    <Form.Check type="radio" label="Radio1" 
                    name="formHorizontalRadios" style={{'paddingBottom': '1rem'}}/>
                    <Form.Check type="radio" label="Radio2" 
                    name="formHorizontalRadios"/>
                </Form.Group>
                <Form.Group as={Col} style={{'padding': '1rem'}}>
                    <SearchBar optionMapper={dropDownHandler}/>
                </Form.Group>
                <Form.Group as={Col}>

                </Form.Group>
            </Row>
        </Form>
    )
}

export default MyForm