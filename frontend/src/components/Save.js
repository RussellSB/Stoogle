import { Button } from 'antd';

const MaxPrice = (props) => {

    const saveStyle = {
        width: props.width, 
        filter: 'invert(82%)'
    }

    return (
        <Button type="primary" size='large' onClick={props.onSave} style={saveStyle} disabled={props.block}>Send Relevancy</Button>
    );
}


export default MaxPrice;
