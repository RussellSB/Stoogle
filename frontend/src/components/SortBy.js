import { Select } from 'antd'
const { Option } = Select;

const selectStyle = {
    width: 130, 
    filter: 'invert(82%)'
}

const SortBy = (props) => {
    return (
        <Select 
            size='large'
            defaultValue="relevancy" 
            style={selectStyle} 
            onChange={props.setSortBy}
            dropdownStyle={selectStyle}
        >
            
            <Option value="relevancy">Relevancy</Option>
            <Option value="reviews">Reviews</Option>
            <Option value="popularity">Popularity</Option>
        </Select>
    );
}

export default SortBy;
