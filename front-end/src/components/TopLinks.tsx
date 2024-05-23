import { ListFormat } from 'typescript'
import '../styles/App.css'
import '../styles/TopLinks.css'

export interface TopLinksProps {
	links?:
	{
		text: string;
		link: string;
	}[]
}

const TopLinks = ({links}: TopLinksProps, props: any) => {
	return (
		<div className='Top-links'>
			{
				links
				&&
				links.map(
					(link) => <a href={link.link}>
						{link.text}
					</a>
				)
			}
		</div>
	)
}

export default TopLinks;