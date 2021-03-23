import { Select } from 'antd'
const { Option } = Select;

// Defining top tags plausible for selection
// Note not to be confused with props.tags - which refers to the selected tags
const tags = [ 'action', 'indie', 'adventure', 'multiplayer', 'singleplayer', 'casual', 'rpg', 'strategy', 'open_world', 'simulation']

// Constructing children for tags component
const children = []
for (let i = 0; i < tags.length; i++) {
    children.push(<Option key={i}>{tags[i]}</Option>);
  }


const Tags = (props) => {

    const selectStyle = {
        maxWidth: props.maxWidth, 
        minWidth: props.minWidth,
        filter: 'invert(82%)',
    }

    // Removes the option for tags that were already selected
    const filteredTags = tags.filter(o => !props.tags.includes(o));

    return (
        <Select
            size='large'
            mode="multiple"
            listHeight={props.listHeight}
            allowClear
            style={selectStyle}
            dropdownStyle={selectStyle}
            placeholder="Filter by tag..."
            value={props.tags}
            onChange={props.setTags}
        >
            {filteredTags.map(item => (
            <Select.Option key={item} value={item}>
                {item}
            </Select.Option>
            ))}
        </Select>
    );
}

export default Tags;
