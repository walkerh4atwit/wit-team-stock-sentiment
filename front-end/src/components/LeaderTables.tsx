import { ReactElement, useEffect, useState } from "react";
import { Col, Row } from "react-bootstrap";
import ipInfo from "../resources/ipInfo.json"
import '../styles/LeaderTables.css'

export interface LeaderTablesProps {

}

interface IDataGroups {
    [key: string]: number[]
}

const LeaderTables = (props: LeaderTablesProps) => {
    const [data, setData] = useState<IDataGroups>({
        "descendingStocks": [1, 2, 3, 4, 5],
        "ascendingStocks": [],
        "descendingSectors": [],
        "ascendingSectors": []
    })

    const dataGroups: {
        label: string,
        dataKey: string
    }[] = [
            {
                label: "Top 5 stocks",
                dataKey: "descendingStocks"
            },
            {
                label: "Bottom 5 stocks",
                dataKey: "ascendingStocks"
            },
            {
                label: "Top 5 sectors",
                dataKey: "descendingSectors"
            },
            {
                label: "Bottom 5 sectors",
                dataKey: "ascendingSectors"
            }
        ]

    // this differentiates the server between dev and prod
    const backEndHost = process.env.NODE_ENV == 'development' ? ipInfo.devHost : ipInfo.prodHost

    const getData = async () => {
        try {
            const response = await fetch('');
            const data = await response.json()
            setData(data)
        }
        catch { }
    }

    const tableRender = (label: string, data: any[]) => {
        const tableHeader: ReactElement = <div className='my-Table-Header'>{label}</div>
        const tableBody: ReactElement = <>
            {data.map((row: {}, index) => {
                return (
                    <div>{index + 1}</div>
                )
            })}
        </>
        return <>{tableHeader} {tableBody}</>
    }

    useEffect(() => {
        getData();
    }, [])

    return (
        <>
            {dataGroups.map(
                (group) => {
                    return (<Col>
                        {tableRender(group.label, data[group.dataKey])}
                    </Col>)
                }
            )}
        </>
    )
}

export default LeaderTables;