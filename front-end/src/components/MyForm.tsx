import React from 'react'
import { Row, Col, Form, Button as BootButton } from 'react-bootstrap'
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
                    
                </Form.Label>
                <Form.Label column>
                    Choose a stock
                </Form.Label>
                <Form.Label column>
                    
                </Form.Label>
            </Row>
            <Row>
                <Form.Group as={Col} style={{'padding': '1rem'}}>
                    {/* <Form.Check type="radio" label="Radio1" 
                    name="formHorizontalRadios" style={{'paddingBottom': '1rem'}}/>
                    <Form.Check type="radio" label="Radio2" 
                    name="formHorizontalRadios"/> */}
                </Form.Group>
                <Form.Group as={Col} style={{'padding': '1rem'}}>
                    <SearchBar optionMapper={dropDownHandler}/>
                    <BootButton variant='success'>
                        Submit!
                    </BootButton>
                </Form.Group>
                <Form.Group as={Col}>

                </Form.Group>
            </Row>
        </Form>
    )
}

export default MyForm