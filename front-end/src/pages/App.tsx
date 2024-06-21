import TopLinks, { TopLinksProps } from '../components/TopLinks';
import MyForm from '../components/MyForm';
import resTopLinks from "../resources/topLinks.json";
import Data from './Data';
import logo from '../images/logo-cropped.svg';
import ReactDOMServer from "react-dom/server"
import { IDataPage } from './Data';
import "../styles/App.css";
import "../styles/bg-gradient.css";

const App = () => {
	const topLinks: TopLinksProps = {
		links: resTopLinks.links
	}

	const handleSubmit = ({id, type}: IDataPage) => {
		const dataHtml = ReactDOMServer.renderToStaticMarkup(<Data id={id} type={type} />)
		const newTab = window.open()

		newTab?.document.write(
			`<!DOCTYPE html>
			<html lang="en">
			<head>
				<meta charset="UTF-8">
				<meta name="viewport" content="width=device-width, initial-scale=1.0">
				<title>About Page</title>
			</head>
			<body>
				<div id="root">${dataHtml}</div>
			</body>
			</html>`
		)

		newTab?.document.close()
	}

	return (
		<>
			<img src={logo} style={{ position: 'absolute', top: '0px', height: '20vh', left: '40vh' }} />
			<div className="my-Header-Gradient App-header">
				<TopLinks links={topLinks.links} />
			</div>
			<div className="App-body">
				<MyForm handleSubmit={handleSubmit}/>
			</div>
		</>
	);
}

export default App;
