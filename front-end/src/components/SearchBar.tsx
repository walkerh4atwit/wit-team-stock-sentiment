import Form from 'react-bootstrap/Form'
import { useState, useEffect, useRef } from 'react'
import ipInfo from '../resources/ipInfo.json'
import '../styles/bg-gradient.css'
import '../styles/Dropdown.css'


const SearchBar = (props: {
    optionRender: (option: any, onClick: () => void) => JSX.Element,
    type: string,
    setBackEndStatus: any
}) => {

    const backEndHost = process.env.NODE_ENV == 'development' ? ipInfo.devHost : ipInfo.prodHost

    const [isOpen, setIsOpen] = useState(false)
    const [query, setQuery] = useState("")
    const [tickers, setTickers] = useState([])

    const inputRef = useRef(null)

    const clickToggle = (e: any) => {
        setIsOpen(e && e.target === inputRef.current)
    }

    const getValue = () => {
        if (query) return query
        return ""
    }

    const selectOption = (option: string) => {
        setQuery(() => option)
        setIsOpen((isOpen) => !isOpen)
    }

    const pullTickers = async () => {
        try {
            const response = await fetch('http://' + ipInfo.devHost + ':3131/tickers', {
                method: 'GET', headers: {
                    "Access-Control-Allow-Origin": "*",
                    "Content-Type": "text/plain"
                }
            });
            const data = await response.json();
            props.setBackEndStatus("Online")
            setTickers(data.map((tk: any) => tk[1] == null ? tk[0] : tk[1]));
        }
        catch (error) {
            props.setBackEndStatus("Offline")
        }
    }

    useEffect(() => {
        document.addEventListener('click', clickToggle);
        return () =>
            document.removeEventListener('click', clickToggle);
    }, [])

    const myFilter = (options: string[]): string[] => (
        options.filter((option) => (
            option.toLowerCase().indexOf(query.toLowerCase()) > -1
        ))
    )

    // This effect is to pull the data from the back for ticker info
    useEffect(() => { pullTickers() }, [])

    return (
        <div className='dropdown'>
            <Form.Control value={getValue()} ref={inputRef} placeholder={"Enter name"} onChange={(e) => { isOpen && setQuery(e.target.value) }}
                style={{ 'borderTopRightRadius': 0, 'borderBottomRightRadius': 0 }} />
            {isOpen && props.type && <div className="options my-Header-Gradient">
                {myFilter(tickers).map((value: string) => {
                    return (
                        props.optionRender(value, () => selectOption(value))
                    )
                })}
            </div>}
        </div>
    )
}

export default SearchBar;