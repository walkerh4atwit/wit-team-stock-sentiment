import { Link } from 'react-router-dom'
import '../styles/App.css'
import '../styles/TopLinks.css'

export interface TopLinksProps {
	links:
	{
		text: string;
		link: string;
	}[]
}

const TopLinks = (props: TopLinksProps) => {
	return (
		<div className='Top-links'>
			{
				props.links.map(
					(link) => <Link key={link.text} to={link.link}>{link.text}</Link>
				)
			}
		</div>
	)
}

export default TopLinks;