import { Select } from 'antd'
const { Option } = Select;

// Defining top tags
const tags = ['action', 'adventure', 'casual', 'atmospheric','2d', 
'anime', 'building', 'arcade', 'action_rpg', 'character_customization']

// Constructing children for tags component
const children = []
for (let i = 0; i < tags.length; i++) {
    children.push(<Option key={i}>{tags[i]}</Option>);
  }

const handleChange = (value) => {
    // TODO
    console.log(`selected ${value}`);
}

const selectStyle = {
    maxWidth: 200, 
    
    minWidth: 130, 
    fontFamily: 'Arial',
    filter: 'invert(82%)',
}

const Tags = () => {
    return (
        <Select
            size='small'
            mode="multiple"
            listHeight={120}
            allowClear
            style={selectStyle}
            dropdownStyle={selectStyle}
            placeholder="Filter by tag..."
            onChange={handleChange}
        >
        {children}
        </Select>
    );
}

export default Tags;