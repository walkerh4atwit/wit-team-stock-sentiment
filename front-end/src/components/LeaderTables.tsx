import { useEffect, useState } from "react";
import { Col, Row } from "react-bootstrap";

export interface LeaderTablesProps {

}

const LeaderTables = (props: LeaderTablesProps) => {
    const [data, setData] = useState({})

    const getData = async () => {
        try {
            const response = await fetch('');
            const data = await response.json()
            setData(data)
        }
        catch {}
    }

    useEffect(() => {
        getData();
    }, [])

    return (
        <Col>
        </Col>
    )
}

export default LeaderTables;