
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
  	
   // Searches for results from API - linked to backend
   const onSearch = () => {    

      // Handles sort by
      let needSort = 0
      if (sortBy != 'relevancy'){needSort = 1}

      const payload = {
         "searchTerm": search,
         "boolOp": 1,  // index of the list-item ['must', 'should', 'match']
         "filterOp": 0,  // 0 for less than, return items less than categoryThreshold
         "categoryFilter": 0, // index of the list-item ['price', 'rating', 'owners']
         "categoryThreshold": maxPrice,  // effectively MaxPrice
         "totalDocs": 20,
         "needSort": needSort,  // Set to 0 for Relevancy, 1 for rest
         "sortBy": [sortBy], // either Rating or Owners
         "isAscending": 1, 
         "needFilter": 0,  // set to false
         "tags": tags
      }

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
         
            let i = 0
            for (const [key, value] of Object.entries(data.data['NAME']))
            {
                  d.push({
                     id: i,
                     title: data.data['NAME'][key],
                     description: data.data['SHORT_DESCRIPTION'][key],
                     price: data.data['PRICE'][key]
                  })

                  i += 1
            }

            setResults(d)
            setPage('results')
            
         })
   }

   // Parses checked marks annotations and sends relevancy feedback to server for evaluation
   const sendFeedback = (checklist) => {

      const sortedCheckList = checklist.sort()
      const feedback = [] // feedback is a list of 'yes' and 'no' wrt to relevant item index

      for (let i=0; i<results.length; i++){
         if (sortedCheckList.includes(i))
         {
            feedback.push('Yes')
         }
         else
         {
            feedback.push('No')
         }
      }

      // Send to API
      const payload = {"Results":feedback}

      const requestOptions = {
         method: 'POST',
         headers: { 
            'Content-Type': 'application/json', 
            'Access-Control-Allow-Origin': '*',
         },
         body: JSON.stringify(payload)
      }

      fetch('http://localhost:5000/feedback', requestOptions)
         .then(response => alert(response.status))  // alerts whether sent or not
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

                                    sendFeedback={sendFeedback}
                                 />
         }
     </div>
  );
}

export default App;
