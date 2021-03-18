import '../styles/Onboarding.css'
import SearchBar from '../components/SearchBar'
import SortBy from '../components/SortBy'
import Tags from '../components/Tags'

import {useState} from 'react'

const Onboarding = (props) => {

    const [search, setSearch] = useState('')
    const [sortBy, setSortBy] = useState('relevancy')
    const [tags, setTags] = useState([])
	
    const onSearch = () => {    
    	let d = {search, sortBy, maxPrice: 1000, tags}
	    console.log(d)
        props.setPage('results')
    }

    return (
      <div className="bodyOnboarding">
	    
                <div className='title'>St<span className='oo'>oo</span>gle</div>
                <SearchBar setSearch={setSearch} onSearch={onSearch} width={400}/>
	    
                <div className='botContainer'>
                    <div className='subBotContainer'>
                        <p>Sort by</p>
                        <div className='sortBy'>
                            <SortBy setSortBy={setSortBy} width={130}/>
                        </div>
                    </div>

                    <div className='subBotContainer'>
                        <p>Tags</p>
                        <div className='tags'>
                            <Tags setTags={setTags} tags={tags} maxWidth={250} minWidth={130} listHeight={120} />
                        </div>
                    </div>
                </div>
      </div>
    )
  }
  
export default Onboarding
