import { Select } from 'antd'
const { Option } = Select;

const handleChange = (value) => {
    // TODO
    console.log(`selected ${value}`);
}

const selectStyle = {
    width: 130, 
    filter: 'invert(82%)'
}

const SortBy = () => {
    return (
        <Select 
            size='large'
            defaultValue="relevancy" 
            style={selectStyle} 
            onChange={handleChange}
            dropdownStyle={selectStyle}
        >
            
            <Option value="relevancy">Relevancy</Option>
            <Option value="reviews">Reviews</Option>
            <Option value="popularity">Popularity</Option>
        </Select>
    );
}

export default SortBy;