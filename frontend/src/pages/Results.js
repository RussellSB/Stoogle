import '../styles/Results.css'
import SearchBar from '../components/SearchBar'
import SortBy from '../components/SortBy'
import Tags from '../components/Tags'
import MaxPrice from '../components/MaxPrice'
import Save from '../components/Save'

import {useState} from 'react'

const Results = (props) => {

    const [search, setSearch] = useState('')
    const [sortBy, setSortBy] = useState('relevancy')
    const [tags, setTags] = useState([])
    const [maxPrice, setMaxPrice] = useState(500)
	
    const onSearch = () => {    
    	let d = {search, sortBy, maxPrice, tags}
	    console.log(d)
    }

    const onSave = () => {
        console.log('saved')
    }

    return (
    <div className='bodyResults'>

	    <div className='header'>
	    	<div className='titleSmall'>St<span className='oo'>oo</span>gle</div>
	    	<SearchBar setSearch={setSearch} onSearch={onSearch} width={800}/>
	    </div>
	    
        <div className='bot'>

            <div className='results'>
                <p>test</p>
            </div>
            
            <div className='subBot'>

                <div className='subBotContainerR'>
                        <p>Max Price</p>
                        <div className='maxPriceR'>
                            <MaxPrice setMaxPrice={setMaxPrice} />
                        </div>
                </div>

                <div className='subBotContainerR'>
                    <p>Tags</p>
                    <div className='tagsR'>
                        <Tags setTags={setTags} tags={tags} maxWidth={280} minWidth={280} listHeight={120}/>
                    </div>
                </div>

                <div className='subBotContainerR'>
                    <p>Sort by</p>
                    <div className='sortByR'>
                        <SortBy setSortBy={setSortBy}  width={280}/>
                    </div>
                </div>

                <div className='subBotContainerR'>
                    <p>Save</p>
                    <div className='saveR'>
                        <Save onSave={onSave} width={280}/>
                    </div>
                </div>
                
            </div>

        </div>

    </div>
    )
  }
  
export default Results
