import { Input } from 'antd';
const { Search } = Input;

const onSearch = () => {    
    // TODO
}

const searchStyle = {
    width: 400, 
    filter: 'invert(82%)'
}


const SearchBar = () => {
    return (
        <Search 
            placeholder="Search video game..." 
            onSearch={onSearch} 
            enterButton 
            size='large'
            style={searchStyle}
        />
      
    );
}


export default SearchBar;