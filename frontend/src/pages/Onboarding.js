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
                <div className='OnContainer'>
                    <div className='sortBy'>
                        <p>test</p>
                    </div>

                    <div className='tags'>
                        <p>test</p>
                    </div>
                </div>

          </body>
      </div>
    );
  }
  
export default Onboarding;