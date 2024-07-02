import { ReactElement, useEffect, useState } from "react";
import { Col, Row, Container } from "react-bootstrap";
import ipInfo from "../resources/ipInfo.json"
import "../styles/LeaderTables.css"

export interface LeaderTablesProps {

}

interface ILeaderDataPoint {

}

// this represents how the data
// will come in from the backend
interface IDataGroups {
    [key: string]: any[][]
}

const LeaderTables = (props: LeaderTablesProps) => {
    // this state is the data used to populate the tables
    // it is expecting to conform to the IDataGroups interface
    // as does its initial value
    const [data, setData] = useState<IDataGroups>({
        "descTickers": [],
        "ascTickers": [],
        "descSectors": [],
        "ascSectors": []
    })

    // this is the information about
    // the headers and what data they will
    // need underneath
    const dataGroupsSchema: {
        label: string,
        dataKey: string
    }[] = [
            {
                label: "Top 5 stocks",
                dataKey: "descTickers"
            },
            {
                label: "Bottom 5 stocks",
                dataKey: "ascTickers"
            },
            {
                label: "Top 5 sectors",
                dataKey: "descSectors"
            },
            {
                label: "Bottom 5 sectors",
                dataKey: "ascSectors"
            }
        ]

    // this differentiates the server between dev and prod
    const backEndHost =
        process.env.NODE_ENV ==
            'development' ?
            ipInfo.devHost
            : ipInfo.prodHost;

    // pulls data from the backend
    const pullData = async () => {
        try {
            const response = await 
                fetch('http://' + backEndHost + "/leadertables");
            const data = await response.json()
            setData(data)
        }
        catch { }
    }

    // this function is the way that a table will render the header and each row
    const tableRender = (label: string, data: any[]) => {
        // a div for the header
        const tableHeader: ReactElement =
            <div className='my-Table-Header my-Header-Gradient'>{label}</div>
        // a map of divs for the rows in empty tags
        const tableBody: ReactElement = <>
            {data.map((data, index) => {
                return (
                    <Row className="my-Table-Row" key={index}>
                        <Col className="my-Table-Column" style={{ maxWidth: "10%" }}>
                            {data[2]}
                        </Col>
                        <Col className="my-Table-Column" style={{ minWidth: "70%", marginRight: "0.5rem" }}>
                            {data[0]}
                        </Col>
                        <Col className="my-Table-Column">
                            {data[1].toFixed(2)}
                        </Col>
                    </Row>
                )
            })}
        </>
        // returns them as siblings (oldest is header)
        return <>{tableHeader} {tableBody}</>
    }

    // makes sure that pulldata 
    // is used at render-time
    useEffect(() => { pullData(); }, [])

    return (
        <>
            {dataGroupsSchema.map(
                (group) => {
                    return (
                        <Col xs className="my-Table" key={group.dataKey}>
                            {tableRender(group.label, data[group.dataKey])}
                        </Col>
                    )
                }
            )}
        </>
    )
}

export default LeaderTables;