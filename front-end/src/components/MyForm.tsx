import React, { ChangeEvent, EventHandler, useState } from 'react'
import { Row, Col, Form, InputGroup, Button as BootButton } from 'react-bootstrap'
import SearchBar from './SearchBar'
import '../styles/Form.css'
import "../styles/bg-gradient.css"

const MyForm = () => {
    const dropDownHandler = (option: any, onClick: () => void): JSX.Element => {
        return <div className='option' key={option} onClick={onClick}>{option}</div>
    }

    const handleRadio = (e: React.ChangeEvent<HTMLInputElement>) => {
        setRadioChoice(e.target.value)
    }

    const [backEndStatus, setBackEndStatus] = useState('Online')
    const [radioChoice, setRadioChoice] = useState("")

    return (
        <Form className='my-Form-Gradient my-Form-Container'>
            <Row>
                <Form.Label column style={{paddingTop: '0px'}}>
                    Step 1: Choose...
                </Form.Label>
                <Form.Label column md={6} style={{paddingTop: '0px'}}>
                    {`Step 2: Find${radioChoice ? " a " + radioChoice : "..."}`}
                </Form.Label>
                <Form.Label column style={{paddingTop: '0px'}}>
                    <div style={{ display: 'flex', justifyContent: 'right' }}>
                        Status:
                        <div style={{paddingRight: '1rem', paddingLeft: '1rem'}}>({backEndStatus})</div>
                        <div style={{borderRadius: '50%', backgroundColor: `${backEndStatus == 'Online' ? 'green' : 'red'}`, width: '25px'}}></div>    
                    </div>
                </Form.Label>
            </Row>
            <Row>
                <Form.Group as={Col}>
                    <Form.Check type="radio" label="Single stock" value="stock"
                        name="formHorizontalRadios"
                        onChange={handleRadio} />
                    <Form.Check type="radio" label="Market sector" value="sector"
                        name="formHorizontalRadios"
                        onChange={handleRadio} />
                    <Form.Check type="radio" label="Whole market" value="market"
                        name="formHorizontalRadios"
                        onChange={handleRadio} />
                </Form.Group>
                <Form.Group md={6} as={Col}>
                    <InputGroup>
                        <SearchBar optionRender={dropDownHandler} type={radioChoice} setBackEndStatus={setBackEndStatus} />
                        <BootButton variant='success' style={{ width: '20%' }}>
                            Submit!
                        </BootButton>
                    </InputGroup>
                </Form.Group>
                <Form.Group as={Col}>

                </Form.Group>
            </Row>
            <Row>

            </Row>
        </Form>
    )
}

export default MyForm