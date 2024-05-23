import React from 'react'
import { Row, Col, Form, Container } from 'react-bootstrap'
import "../styles/bg-gradient.css"

const MyForm = () => {
    return (
        <Container bg-light fluid className='my-Form-Gradient my-Form-Container'>
            <Form>
                <Row>
                    <Form.Group as={Col}>
                        Hello
                    </Form.Group>
                    <Form.Group as={Col}>
                        It's
                    </Form.Group>
                    <Form.Group as={Col}>
                        Henry
                    </Form.Group>
                </Row>
            </Form>
        </Container>
    )
}

export default MyForm