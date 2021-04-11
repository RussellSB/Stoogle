import '../styles/Results.css'
import SearchBar from '../components/SearchBar'
import SortBy from '../components/SortBy'
import Tags from '../components/Tags'
import MaxPrice from '../components/MaxPrice'
import Save from '../components/Save'
import ItemList from '../components/ItemList'

import { useState, useEffect, useRef } from 'react'

const Results = (props) => {

    // ================= Concerned with pagination
    const value = useRef(1);
    const [pageIndex, setPageIndex] = useState(value.current)
    const [checklist, setCheckList] = useState([])

    const [block, setBlock] = useState(true)

    // Resets page index and checklist on new results
    useEffect(() => {

        // Reset page to first
        value.current = 1;
        setPageIndex(value.current)  

        // Reset checkboxes to all relevant
        const defaultCheckList = []
        for (let i=0; i < props.results.length; i++){
            defaultCheckList.push(i)
        }
        setCheckList(defaultCheckList)

        // Toggle visibility
        if(props.sortBy == 'relevancy'){setBlock(false)}
        else{setBlock(true)}

        return () => {};
      }, [props.results, props.sortBy]);

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
                <ItemList 
                    onCheck={props.onCheck} 
                    data={props.results}
                    value = {value}

                    pageIndex={pageIndex}
                    setPageIndex={setPageIndex}

                    checklist={checklist}
                    setCheckList={setCheckList}
                    />
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
                    <p>Send</p>
                    <div className='saveR'>
                        <Save onSave={() => props.sendFeedback(checklist)} width={280} block={block}/>
                    </div>
                </div>
                
            </div>

        </div>

    </div>
    )
  }
  
export default Results
