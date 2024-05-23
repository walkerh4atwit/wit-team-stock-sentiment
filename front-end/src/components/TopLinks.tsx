import { ListFormat } from 'typescript'
import '../styles/App.css'
import '../styles/TopLinks.css'

interface TopLinksProps {
	links?: {
		name: string;
		link: string;
	}[]
}

const TopLinks = (props: TopLinksProps) => {
	return (
		<div className='Top-links'>
			<div>Henry</div>
			<div>Walker</div>
			<div>Is</div>
			<div>Cool</div>
		</div>
	)
}

export default TopLinks;