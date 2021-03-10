import '../styles/Onboarding.css'
import SearchBar from '../components/SearchBar'

const Onboarding = () => {
    return (
      <div className="Onboarding">
          <body>
                <div className='title'>Stoogle</div>
                <br></br><br></br>
                <SearchBar/>

                {/** Container 
                 * 
                 * Sort by
                 * Tags (use state)
                 * 
                */}
                <div className='botContainer'>
                    <div className='subBotContainer'>
                        <p>Sort by</p>
                        <div className='sortBy'>
                            <p>test</p>
                        </div>
                    </div>

                    <div className='subBotContainer'>
                        <p>Tags</p>
                        <div className='tags'>
                            <p>test</p>
                        </div>
                    </div>
                </div>

          </body>
      </div>
    );
  }
  
export default Onboarding;