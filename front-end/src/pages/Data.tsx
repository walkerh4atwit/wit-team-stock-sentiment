import { Button as BootButton } from "react-bootstrap"
import logo from "../images/logo-cropped.svg";
import "../styles/App.css";
import "../styles/bg-gradient.css";
import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

export interface IDataPage {
    id: number, type: string
}

const Data = () => {
    const { id, type } = useParams()

    const pullData = (qry: IDataPage) => {
        // expose backend point
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
                <div className="my-Form-Gradient my-Form-Container">
                </div>
            </div>
        </>
    )
}

export default Data;