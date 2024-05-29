import Form from 'react-bootstrap/Form'
import tickers from '../resources/mockSearch.json'
import { useState, useEffect, useRef } from 'react'

const SearchBar = () => {
    const mockValues = tickers.tickers
    console.log(mockValues)

    const inputRef = useRef(null)
    const clickToggle = (e: any) => {
        setIsOpen(e && e.target === inputRef.current)
    }

    const [isOpen, setIsOpen] = useState(false)
    const [query, setQuery] = useState('')

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
        <Form.Control ref={inputRef} placeholder='Enter Stock' onChange={(e) => {isOpen && setQuery(e.target.value)}}>
            {}
        </Form.Control>
    )
}

export default SearchBar;