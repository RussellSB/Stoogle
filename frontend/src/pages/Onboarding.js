import '../styles/Onboarding.css'
import SearchBar from '../components/SearchBar'
import SortBy from '../components/SortBy'
import Tags from '../components/Tags'

const Onboarding = () => {
    return (
      <div className="Onboarding">
          <body>
                <div className='title'>St<span className='oo'>oo</span>gle</div>
                <SearchBar/>

                <div className='botContainer'>
                    <div className='subBotContainer'>
                        <p>Sort by</p>
                        <div className='sortBy'>
                            <SortBy/>
                        </div>
                    </div>

                    <div className='subBotContainer'>
                        <p>Tags</p>
                        <div className='tags'>
                            <Tags/>
                        </div>
                    </div>
                </div>

          </body>
      </div>
    );
  }
  
export default Onboarding;