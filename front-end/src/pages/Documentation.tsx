import logo from "../images/logo-cropped.svg"
import TopLinks, { TopLinksProps } from "../components/TopLinks"
import resTopLinks from "../resources/topLinks.json"

const Documentation = () => {
    const topLinks: TopLinksProps = {
        links: resTopLinks.links
    }

    return (
        <>
            <img src={logo} style={{ position: 'absolute', top: '0px', height: '20vh', left: '40vh' }} />
            <div className="my-Header-Gradient App-header">
                <TopLinks links={topLinks.links} />
            </div>
            <div className="App-body">
                <div className="my-Form-Gradient my-Form-Blob">
                    
                </div>
            </div>
        </>
    )
}

export default Documentation;