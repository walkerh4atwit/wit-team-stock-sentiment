import React, { ChangeEvent, EventHandler, useState } from 'react'
import { Row, Col, Form, InputGroup, Button as BootButton } from 'react-bootstrap'
import SearchBar from './SearchBar'
import LeaderTables from './LeaderTables'
import { IDataPage } from '../pages/Data'
import '../styles/Form.css'
import "../styles/bg-gradient.css"

const MyForm = (props: { handleSubmit: ({ id, type }: IDataPage) => void }) => {
    // this function handles rendering the dropdown of the searchbar in a certain way
    const dropDownHandler = (option: any[], index: number, onClick: () => void): JSX.Element => {
        const [id, alternate_name, name, count] = option
        const useName: string = name == null ? alternate_name : name
        // renders div after selecting the name to use
        return <div className='option' key={index} onClick={onClick}>{useName}</div>
    }

    // changes the radiochoice based on the radio being pressed
    const handleRadio = (e: React.ChangeEvent<HTMLInputElement>) => {
        setRadioChoice(e.target.value)
    }

    //states
    const [backEndStatus, setBackEndStatus] = useState('Online')
    const [radioChoice, setRadioChoice] = useState("")
    const [idSelection, setIdSelection] = useState(-1)

    return (
        <Form className='my-Form-Gradient my-Form-Container'>
            <Row>
                <Col>
                    Step 1: Choose...
                </Col>
                <Col md={6} style={{ paddingTop: '0px' }}>
                    {`Step 2: Find${radioChoice ? " a " + radioChoice : "..."}`}
                </Col>
                <Col style={{ paddingTop: '0px' }}>
                    <div style={{ display: 'flex', justifyContent: 'right' }}>
                        Status:
                        <div style={{ paddingRight: '1rem', paddingLeft: '1rem' }}>({backEndStatus})</div>
                        <div style={{ borderRadius: '50%', backgroundColor: `${backEndStatus == 'Online' ? 'green' : 'red'}`, width: '25px' }}></div>
                    </div>
                </Col>
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
                        <BootButton variant='success' style={{ width: '20%' }} onClick={() => props.handleSubmit({ id: idSelection, type: radioChoice })}>
                            Submit!
                        </BootButton>
                    </InputGroup>
                </Form.Group>
                <Form.Group as={Col}>

                </Form.Group>
            </Row>
            <Row style={{ paddingTop: '20vh' }}>
                <LeaderTables />
            </Row>
        </Form>
    )
}

export default MyForm