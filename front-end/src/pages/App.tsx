import React from 'react'
import TopLinks from '../components/TopLinks'
import MyForm from '../components/MyForm'
import "../styles/App.css"
import "../styles/bg-gradient.css"

const App = () => {
	return (
		<>
			<div className="my-Header-Gradient App-header">
				<TopLinks />
			</div>
			<MyForm />
		</>
	);
}

export default App;
