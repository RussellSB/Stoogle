
import 'antd/dist/antd.css';
import Onboarding from './pages/Onboarding'
import {useState} from 'react'
import Results from './pages/Results'

const App = () => {

   const [search, setSearch] = useState('')
   const [sortBy, setSortBy] = useState('relevancy')
   const [tags, setTags] = useState([])
   const [maxPrice, setMaxPrice] = useState(500)
   const [page, setPage] = useState('onboarding') // onboarding

   const [results, setResults] = useState([])  // stores the retrieved data parsed correctly
  	
   const onSearch = async () => {    
      //let payload = {search, sortBy, maxPrice: 1000, tags}

      const payload = {
         "searchTerm": search,
         "boolOp": 0,  
         "filterOp": 0,  
         "categoryFilter": 0, 
         "categoryThreshold": 50,
         "totalDocs": 10,
         "needSort": 1,  
         "sortBy": ["NAME"], 
         "isAscending": 1, 
         "needFilter": 1, 
         "categories": ["NAME", "PRICE", "RATING", "SHORT_DESCRIPTION"],
      }
      
      //console.log(payload)

      const requestOptions = {
         method: 'POST',
         headers: { 
            'Content-Type': 'application/json', 
            'Access-Control-Allow-Origin': '*',
       },
         body: JSON.stringify(payload)
     }

     fetch('http://localhost:5000/search', requestOptions)
         .then(response => response.json())
         .then(data => {

            console.log(data)
            const d = []  // list to store objects of information
            const length = Object.keys(data.data['NAME']).length  // sets to length of results returned
        
            let i = 0
            for (const [key, value] of Object.entries(data.data['NAME']))
            {
                  d.push({
                     id: i,
                     title: data.data['NAME'][key],
                     description: data.data['SHORT_DESCRIPTION'][key],
                     price: data.data['PRICE'][key],
                     checked: data.data['RELEVANT'][key]
                  })
                  i += 1
            }

            setResults(d)
            setPage('results')
         })
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
                                    results={results}
                                 />
         }
     </div>
  );
}

export default App;
