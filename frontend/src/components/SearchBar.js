import { Input } from 'antd';
const { Search } = Input;

const searchStyle = {
    width: 400, 
    filter: 'invert(82%)'
}


const SearchBar = (props) => {
    return (
        <Search 
            placeholder="Search video game..." 
            onSearch={props.onSearch}
	    onChange={e => props.setSearch(e.target.value)}
            enterButton 
            size='large'
            style={searchStyle}
        />
      
    );
}


export default SearchBar;
