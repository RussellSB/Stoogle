import '../styles/Onboarding.css'
import SearchBar from '../components/SearchBar'
import SortBy from '../components/SortBy'
import Tags from '../components/Tags'

import {useState} from 'react'

const Onboarding = (props) => {

    return (
      <div className="bodyOnboarding">
	    
                <div className='title'>St<span className='oo'>oo</span>gle</div>
                <SearchBar setSearch={props.setSearch} onSearch={props.onSearch} width={400}/>
	    
                <div className='botContainer'>
                    <div className='subBotContainer'>
                        <p>Sort by</p>
                        <div className='sortBy'>
                            <SortBy setSortBy={props.setSortBy} width={130}/>
                        </div>
                    </div>

                    <div className='subBotContainer'>
                        <p>Tags</p>
                        <div className='tags'>
                            <Tags setTags={props.setTags} tags={props.tags} maxWidth={250} minWidth={130} listHeight={120} />
                        </div>
                    </div>
                </div>
      </div>
    )
  }
  
export default Onboarding
