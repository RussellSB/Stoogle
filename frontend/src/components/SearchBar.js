import { Input } from 'antd';
const { Search } = Input;

const onSearch = () => {    
    // TODO
}

const searchStyle = {
    width: 390, 
    fontFamily: 'Arial',
    filter: 'invert(82%)'
}


const SearchBar = () => {
    return (
        <Search 
            placeholder="Search video game..." 
            onSearch={onSearch} 
            enterButton 
            size='small'
            style={searchStyle}
        />
      
    );
}


export default SearchBar;