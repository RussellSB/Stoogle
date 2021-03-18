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

const removeWord = (array, word) => {
    let arr = []
    for(let i=0; i < array.length; i++){
	if(array[i] != word){
	   arr.push(array[i])
	}
    }

    return arr
}

const Tags = (props) => {

    const selectStyle = {
        maxWidth: props.maxWidth, 
        minWidth: props.minWidth,
        filter: 'invert(82%)',
    }
    

    return (
        <Select
            size='large'
            mode="multiple"
            listHeight={props.listHeight}
            allowClear
            style={selectStyle}
            dropdownStyle={selectStyle}
            placeholder="Filter by tag..."
	    onDeselect={i => props.setTags(removeWord(props.tags, tags[i]))}
	    onSelect={i => props.setTags([...props.tags, tags[i]])}
        >
        {children}
        </Select>
    );
}

export default Tags;
