import TopLinks, { TopLinksProps } from '../components/TopLinks'
import MyForm from '../components/MyForm'
import resTopLinks from "../resources/topLinks.json"
import logo from '../images/logo-cropped.svg'
import "../styles/App.css"
import "../styles/bg-gradient.css"

const App = () => {
	const topLinks: TopLinksProps = {
		links: resTopLinks.links
	}

	return (
		<>
			<img src={logo} style={{ position: 'absolute', top: '0px', height: '20vh', left: '40vh' }} />
			<div className="my-Header-Gradient App-header">
				<TopLinks links={topLinks.links} />
			</div>
			<div className="App-body">
				<MyForm />
			</div>
		</>
	);
}

export default App;
