import Form from 'react-bootstrap/Form'
import { useState, useEffect, useRef } from 'react'
import '../styles/bg-gradient.css'
import '../styles/Dropdown.css'


const SearchBar = (props: { optionRender: (option: any, onClick: () => void) => JSX.Element, type: string}) => {
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

    useEffect(() => {
        fetch('http://localhost:3131/tickers', {
            method: 'GET', headers: {
                "Access-Control-Allow-Origin": "*",
                "Content-Type": "text/plain"
            }
        }).then((tks) => { return tks.json() }).then((tks) =>
            setTickers(tks.map((tk: any) => tk[1] == null ? tk[0] : tk[1])))
    }, [])



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