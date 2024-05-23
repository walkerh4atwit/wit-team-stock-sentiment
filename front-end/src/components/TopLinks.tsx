import { ListFormat } from 'typescript'
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
					(link) => <a href={link.link}>
						{link.text}
					</a>
				)
			}
		</div>
	)
}

export default TopLinks;