import logo from "../images/logo-cropped.svg";
import "../styles/App.css";
import "../styles/bg-gradient.css";
import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { ProgressBar } from "react-bootstrap";
import '../styles/DataPage.css'

export interface IDataQuery {
    id: number, type: string
}

interface IDataPage {
    sector: string,
    score: number,
    name: string,
    ticker: string
}

const Data = () => {
    const [data, setData] = useState<IDataPage>({
        sector: "",
        score: 0,
        name: "",
        ticker: ""
    })

    const { type, id } = useParams()
    console.log(`Type: ${type}, ID: ${id}`);

    // this differentiates the server between dev and prod
    const backEndHost =
        process.env.REACT_APP_API_URL

    const pullData = async (qry: IDataQuery) => {
        try {
            const response = await fetch("https://" + backEndHost + "/sentiment/" + qry.type + "/" + qry.id)
            const responseData = await response.json()

            setData({
                sector: responseData['sector'],
                score: responseData['score'],
                name: responseData['name'],
                ticker: responseData['ticker']
            })

        } catch (error) {
            console.log(error)
        }
    }

    useEffect(
        () => {
            if (id && type) {
                pullData({ id: parseInt(id), type: type })
            }
        }, []
    )

    return (
        <>
            <img src={logo} style={{
                position: 'absolute',
                top: '0px',
                height: '20vh',
                left: '40vh'
            }} />
            <div className="my-Header-Gradient App-header"></div>
            <div className="App-body">
                <div className="my-Form-Gradient my-Form-Blob">
                    <div style={{display: 'flex', justifyContent: 'space-between'}}>
                        <div className="title">{data.name} {type == 'stock' && '(' + data.ticker + ')'}</div>
                        <div className="secondary-title">{type == "stock" ? data.sector : ""}</div>
                    </div>
                    <div>
                        <ProgressBar
                            now={data.score > 0.1 ? data.score / 2.0 * 100 : 10}
                            label={data.score.toFixed(2)}
                            variant={data.score > 1.2 ? 'success' : data.score > 0.8 ? "warning" : 'danger'}>
                        </ProgressBar>
                    </div>
                </div>
            </div>
        </>
    )
}

export default Data;