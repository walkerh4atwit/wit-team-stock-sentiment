import { Link } from "react-router-dom"
import "../styles/App.css"
import "../styles/TopLinks.css"
import "../styles/bg-gradient.css"

export interface TopLinksProps {
	links:
	{
		text: string;
		link: string;
	}[]
}

const TopLinks = (props: TopLinksProps) => {
	return (
		<div className='Top-links my-Form-Gradient'>
			{
				props.links.map(
					(link) => <Link style={{color: 'black'}} key={link.text} to={link.link}>{link.text}</Link>
				)
			}
		</div>
	)
}

export default TopLinks;