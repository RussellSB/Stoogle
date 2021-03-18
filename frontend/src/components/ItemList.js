import { List } from 'antd';
import { useState, useEffect, useRef } from 'react'
import { Checkbox } from 'antd'

const PAGE_SIZE = 6

const ItemList = (props) => {

    // ================= Concerned with pagination
    const value = useRef(1);
    const [pageIndex, setPageIndex] = useState(value.current)

    const listStyle = {
        filter: 'invert(82%)'
    }

    const itemStyle = {
        padding: 40,
        fontSize: '1.5em'
    }

    // If pressed key is our target key then perform action to navigate left or right
    const upHandler = ({ key }) => {
      if (key === 'ArrowLeft' && value.current - 1 >= 1) {  //doesnt trigger when outside limit
        value.current -= 1
        setPageIndex(value.current)
      }
      if (key === 'ArrowRight' && value.current + 1 <= Math.ceil(props.data.length / PAGE_SIZE)) {  //doesnt trigger when outside limit
        value.current += 1
        setPageIndex(value.current)
      }
    }
  
    // Add event listeners for page navigation
    useEffect(() => {
      window.addEventListener('keyup', upHandler)
      // Remove event listeners on cleanup
      return () => {
        window.removeEventListener('keyup', upHandler)
      };
    }, []); // Empty array ensures that effect is only run on mount and unmount

    // A hacky solution, to enable all by default
    const defaultChecked = [];
    for(let i=0; i<props.data.length; i++){
        defaultChecked.push(i)
    }

    return (
        <List style={listStyle}
        itemLayout="horizontal"
        dataSource={props.data}
        size='large'
        pagination={{
            onChange: page => {
                value.current = page;
                setPageIndex(page)
            },
            pageSize: PAGE_SIZE,
            current: pageIndex
        }}
        renderItem={item => (
            <Checkbox.Group style={{ width: '100%' }} defaultValue={defaultChecked}>
                <List.Item style={itemStyle} size='large'>
                    <List.Item.Meta
                    title={item.title}
                    description={item.description}
                    />
                    <div style={{paddingRight: 20}}>£{item.price}</div>
                    <Checkbox value={item.id} onChange={props.onCheck}/>
                </List.Item>
            </Checkbox.Group>
        )}
        />
    );
}

export default ItemList;
