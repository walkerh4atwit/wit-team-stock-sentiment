import React from 'react';
import TopLinks from '../components/TopLinks'
import Container from 'react-bootstrap/Container'
import { Row, Col, Form } from 'react-bootstrap'
import CSS from 'csstype'
import "../styles/App.css"
import "../styles/bg-gradient.css"

const App = () => {
	return (
		<>
			<div className="my-Header-Gradient App-header">
				<TopLinks />
			</div>
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
		</>
	);
}

export default App;
