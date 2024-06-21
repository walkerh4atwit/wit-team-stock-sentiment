import React from "react";
import ReactDOM from "react-dom/client";
import { createBrowserRouter, RouterProvider } from "react-router-dom"
import "bootstrap/dist/css/bootstrap.min.css";

import App from "./pages/App";
import FAQ from "./pages/FAQ";
import Documentation from "./pages/Documentation";

import reportWebVitals from "./reportWebVitals";

const root = ReactDOM.createRoot(
	document.getElementById('root') as HTMLElement
);

const router = createBrowserRouter([
	{
		path: '/',
		element: <App />
	},
	{
		path: '/faq',
		element: <FAQ />
	},
	{
		path: '/docs',
		element: <Documentation />
	}
])

root.render(
	<React.StrictMode>
		<RouterProvider router={router} />
	</React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
