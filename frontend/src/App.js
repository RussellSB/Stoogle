
import 'antd/dist/antd.css';
import Onboarding from './pages/Onboarding'
import {useState} from 'react'
import Results from './pages/Results'

const App = () => {
  const [page, setPage] = useState('results') // onboarding
  return (
     <div>
        {page == 'onboarding' && <Onboarding setPage={setPage}/>}
        {page == 'results' && <Results setPage={setPage}/>}
     </div>
  );
}

export default App;
