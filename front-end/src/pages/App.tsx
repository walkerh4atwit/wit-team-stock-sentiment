import TopLinks from '../components/TopLinks'
import { TopLinksProps } from '../components/TopLinks'
import MyForm from '../components/MyForm'
import "../styles/App.css"
import "../styles/bg-gradient.css"

const App = () => {
	const linkObj: TopLinksProps = {
		links:
		[
			{
				text: "Callback",
				link: "localhost:3000"
			},
			{
				text: "New page",
				link: "localhost:3000"
			}
		]
	}

	return (
		<>
			<div className="my-Header-Gradient App-header">
				<TopLinks links={linkObj.links}/>
			</div>
			<MyForm />
		</>
	);
}

export default App;
