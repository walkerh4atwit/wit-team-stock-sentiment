import TopLinks from '../components/TopLinks'
import { TopLinksProps } from '../components/TopLinks'
import MyForm from '../components/MyForm'
import resTopLinks from "../resources/topLinks.json"
import "../styles/App.css"
import "../styles/bg-gradient.css"

const App = () => {
	const topLinks: TopLinksProps = {
		links: resTopLinks.links
	}

	return (
		<>
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
