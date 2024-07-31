import logo from "../images/logo-cropped.svg"
import TopLinks, { TopLinksProps } from "../components/TopLinks"
import resTopLinks from "../resources/topLinks.json"
import "../styles/Docs.css"
import evanHeadShot from "../images/evanheadshot.jpeg"
import { Link } from "react-router-dom"

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
                    <div className="docs-row">
                        <div className="docs-quote" style={{ width: '60%' }}>
                            "We provide traders with an easy-to-use
                            web application that will allow them to view
                            the sentiment scores for individual stocks,
                            and overall sectors to use in potential trading
                            strategies.​"
                        </div>
                        <div className="docs-quote-image" style={{ width: '40%' }}>
                            <img src={evanHeadShot} width={'60%'} />
                            <div className="docs-quoted-name">
                                - Evan Dyer, Wentworth Institute of Technology Senior, in charge of Database and ML
                            </div>
                        </div>
                    </div>
                    <div className="docs-row" style={{ justifyContent: 'center', marginTop: '5rem' }}>
                        <a href="documents/example.pdf" target="_blank" className="docs-quote" style={{ textDecoration: 'underline' }}>
                            Documentation for this Project (click here)
                        </a>
                    </div>
                </div>
            </div>
        </>
    )
}

export default Documentation;