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
            <Option value="RATING">Reviews</Option>
            <Option value="OWNERS">Popularity</Option>
            <Option value="PRICE">Price</Option>
        </Select>
    );
}

export default SortBy;
