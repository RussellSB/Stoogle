import { List } from 'antd';
import { useState, useEffect, useRef } from 'react'
import { Checkbox } from 'antd'

const PAGE_SIZE = 5

const ItemList = (props) => {

    const listStyle = {
        filter: 'invert(82%)'
    }

    const itemStyle = {
        padding: 40,
        fontSize: '1.5em'
    }

    // If pressed key is our target key then perform action to navigate left or right
    const upHandler = ({ key }) => {
      if (key === 'ArrowLeft' && props.value.current - 1 >= 1) {  // doesn't trigger when outside limit
        props.value.current -= 1
        props.setPageIndex(props.value.current)
      }
      if (key === 'ArrowRight' && props.value.current + 1 <= Math.ceil(props.data.length / PAGE_SIZE)) {  //doesn't trigger when outside limit
        props.value.current += 1
        props.setPageIndex(props.value.current)
      }
    }
  
    // Add event listeners for page navigation
    useEffect(() => {
      window.addEventListener('keyup', upHandler)
      // Remove event listeners on cleanup
      return () => {
        window.removeEventListener('keyup', upHandler)
      };
    }, []);

    // Updates check list, either by an item being unchecked or checked
    const updateCheckList = (e) => {
      if (e.target.checked == true){
        props.setCheckList([... props.checklist, e.target.value])
      }

      if (e.target.checked == false){
        const unchecked = props.checklist.filter(function(value, index, arr){return value != e.target.value})
        props.setCheckList(unchecked)
      }
    }

    return (
      <Checkbox.Group style={{ width: '100%' }} value={props.checklist}>
          <List style={listStyle}
          itemLayout="horizontal"
          dataSource={props.data}
          size='large'
          pagination={{
              onChange: page => {
                  props.value.current = page;
                  props.setPageIndex(page)
              },
              pageSize: PAGE_SIZE,
              current: props.pageIndex
          }}
          renderItem={item => (
                  <List.Item style={itemStyle} size='large'>
                      <List.Item.Meta
                      title={(item.id+1) + '. ' + item.title}
                      description={item.description}
                      />
                      <div style={{paddingRight: 40, paddingLeft: 20}}>£{item.price}</div>
                      <Checkbox value={item.id} onChange={updateCheckList}/>
                  </List.Item>
          )}
          />
      </Checkbox.Group>
    );
}

export default ItemList;
