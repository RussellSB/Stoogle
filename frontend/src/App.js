
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
  	
   const onSearch = () => {    
      let d = {search, sortBy, maxPrice: 1000, tags}
      console.log(d)
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
