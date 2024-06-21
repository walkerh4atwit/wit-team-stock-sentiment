import TopLinks, { TopLinksProps } from '../components/TopLinks';
import MyForm from '../components/MyForm';
import resTopLinks from "../resources/topLinks.json";
import Data from './Data';
import ReactDOMServer from "react-dom/server"
import logo from '../images/logo-cropped.svg';
import { IDataPage } from './Data';
import "../styles/App.css";
import "../styles/bg-gradient.css";
import { useRef } from 'react';

const App = () => {
	const topLinks: TopLinksProps = {
		links: resTopLinks.links
	}

	const handleSubmit = ({ id, type }: IDataPage) => {
		const newTab = window.open('')

		const downloadHandler = () => {
			const blob = new Blob([document.documentElement.outerHTML], {type: 'text/html'});
			const url = URL.createObjectURL(blob);

			const a = document.createElement('a');
			a.href = url;
			a.download = 'report.html'
			document.head.appendChild(a)
			a.click()
			document.head.removeChild(a)
			URL.revokeObjectURL(url);
		}

		const newHtml = ReactDOMServer.renderToString(<Data downloadHandler={downloadHandler} id={id} type={type} />)

		// this function puts all the css from this file into text
		const extractCSSRules = () => {
			let css = '';
			// Convert StyleSheetList to an array
			const styleSheets = Array.from(document.styleSheets);
			for (const styleSheet of styleSheets) {
				try {
					// Convert CSSRuleList to an array
					const rules = Array.from(styleSheet.cssRules);
					for (const rule of rules) {
						css += rule.cssText;
					}
				} catch (e) {
					console.log('Access to stylesheet %s is denied. Ignoring.', styleSheet.href);
				}
			}
			return css;
		};

		const css = extractCSSRules();

		const htmlString = `<!DOCTYPE html>
			<html lang="en">
			<head>
				<meta charset="UTF-8">
				<meta name="viewport" content="width=device-width, initial-scale=1.0">
				<title>Your Report</title>
				<style>${css}</style>
			</head>
			<body>
				<div id="root">${newHtml}</div>
			</body>
			</html>`

		newTab?.document.write(htmlString);
		newTab?.document.close();
	}

	return (
		<>
			<img src={logo} style={{ position: 'absolute', top: '0px', height: '20vh', left: '40vh' }} />
			<div className="my-Header-Gradient App-header">
				<TopLinks links={topLinks.links} />
			</div>
			<div className="App-body">
				<MyForm handleSubmit={handleSubmit} />
			</div>
		</>
	);
}

export default App;
