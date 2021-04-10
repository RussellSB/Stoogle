import '../styles/Results.css'
import SearchBar from '../components/SearchBar'
import SortBy from '../components/SortBy'
import Tags from '../components/Tags'
import MaxPrice from '../components/MaxPrice'
import Save from '../components/Save'
import ItemList from '../components/ItemList'

import {useState} from 'react'

const Results = (props) => {

    const [checked, setChecked] = useState(props.results.length)  // sets to amount of checked to amount returned

    const onSave = () => {
        console.log(checked)
        console.log(checked)
    }
    
    const onCheck = (e) => {
        if(e.target.checked){
            setChecked(checked + 1)
        }
        else{
            setChecked(checked - 1)
        }
    }

    return (
    <div className='bodyResults'>

	    <div className='header'>
	    	<div className='titleSmall'>St<span className='oo'>oo</span>gle</div>
	    	<SearchBar 
                setSearch={props.setSearch} 
                onSearch={props.onSearch} 
                search={props.search} 
                width={800}
            />
	    </div>
	    
        <div className='bot'>

            <div className='results'>
                <ItemList onCheck={onCheck} data={props.results}/>
            </div>

            <div className='subBot'>

                <div className='subBotContainerR'>
                        <p>Max Price</p>
                        <div className='maxPriceR'>
                            <MaxPrice 
                                setMaxPrice={props.setMaxPrice}     
                            />
                        </div>
                </div>

                <div className='subBotContainerR'>
                    <p>Tags</p>
                    <div className='tagsR'>
                        <Tags 
                            setTags={props.setTags} 
                            tags={props.tags} 
                            maxWidth={280} 
                            minWidth={280} 
                            listHeight={120}
                        />
                    </div>
                </div>

                <div className='subBotContainerR'>
                    <p>Sort by</p>
                    <div className='sortByR'>
                        <SortBy 
                            setSortBy={props.setSortBy} 
                            sortBy={props.sortBy} 
                            width={280}
                        />
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
