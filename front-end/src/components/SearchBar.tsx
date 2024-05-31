import Form from 'react-bootstrap/Form'
import tickers from '../resources/mockSearch.json'
import { useState, useEffect, useRef } from 'react'
import '../styles/bg-gradient.css'
import '../styles/Dropdown.css'


const SearchBar = (props: {optionMapper: (option: any, onClick: () => void) => JSX.Element}) => {
    const mockValues = tickers.tickers
    const [isOpen, setIsOpen] = useState(false)
    const [query, setQuery] = useState("")

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

    return (
        <>
            <Form.Control value={getValue()} ref={inputRef} placeholder='Enter Stock' onChange={(e) => { isOpen && setQuery(e.target.value) }} />
            {isOpen && <div className='dropdown my-Header-Gradient'>
                {myFilter(mockValues).map((value: string) => {
                    return (
                        props.optionMapper(value, () => selectOption(value))
                    )
                })}
            </div>}
        </>
    )
}

export default SearchBar;