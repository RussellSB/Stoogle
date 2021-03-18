import { Input } from 'antd';
const { Search } = Input;


const SearchBar = (props) => {

    const searchStyle = {
        width: props.width, 
        filter: 'invert(82%)'
    }

    return (
        <Search 
            placeholder="Search video game..." 
            onSearch={props.onSearch}
	        onChange={e => props.setSearch(e.target.value)}
            enterButton 
            size='large'
            style={searchStyle}
            value={props.search}
        />
      
    );
}


export default SearchBar;
