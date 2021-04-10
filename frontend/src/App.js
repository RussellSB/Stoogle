
import 'antd/dist/antd.css';
import Onboarding from './pages/Onboarding'
import {useState} from 'react'
import Results from './pages/Results'

import axios from 'axios'

const App = () => {

   const [search, setSearch] = useState('')
   const [sortBy, setSortBy] = useState('relevancy')
   const [tags, setTags] = useState([])
   const [maxPrice, setMaxPrice] = useState(500)
   const [page, setPage] = useState('onboarding') // onboarding
  	
   const onSearch = async () => {    
      //let payload = {search, sortBy, maxPrice: 1000, tags}
      let payload = {
         "searchTerm": "Counter-Strike",
         "boolOp": 0,  
         "filterOp": 0,  
         "categoryFilter": 0, 
         "totalDocs": 10,
         "needSort": 1,  
         "sortBy": ["NAME"], 
         "isAscending": 1, 
         "needFilter": 1, 
         "categories": ["NAME", "PRICE", "RATING", "SHORT_DESCRIPTION"]
     }
      
      //console.log(payload)

      let res = await axios.post(`localhost:5000/search`, {data: payload})
      console.log(res, res.data)
      //let data = res.data
      //console.log(data)

      setPage('results')
   }

  return (
     <div>
        {page == 'onboarding' && <Onboarding 
                                    setPage={setPage} 
                                    setSearch={setSearch} 
                                    onSearch={onSearch}
                                    setSortBy={setSortBy} 
                                    setMaxPrice={setMaxPrice} 
                                    setTags={setTags}
                                    tags={tags}
                                 />
        }

        {page == 'results' && <Results 
                                    setPage={setPage} 
                                    setSearch={setSearch} 
                                    onSearch={onSearch}
                                    setSortBy={setSortBy} 
                                    setMaxPrice={setMaxPrice} 
                                    setTags={setTags}

                                    tags={tags}
                                    sortBy={sortBy}
                                    search={search}
                                 />
         }
     </div>
  );
}

export default App;
