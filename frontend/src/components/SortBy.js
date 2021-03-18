import { Select } from 'antd'
const { Option } = Select;

const SortBy = (props) => {

    const selectStyle = {
        width: props.width, 
        filter: 'invert(82%)'
    }

    return (
        <Select 
            size='large'
            defaultValue="relevancy" 
            style={selectStyle} 
            value={props.sortBy}
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
