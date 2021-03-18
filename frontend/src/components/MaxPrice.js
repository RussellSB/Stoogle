import { Input } from 'antd';

import { Slider, Switch } from 'antd';


const MaxPrice = (props) => {

    const slideStyle = {
        width: props.width, 
        filter: 'invert(82%)'
    }

    return (
        <Slider tooltipPlacement='bottom' defaultValue={500} min={0} max={500} size='large' onChange={props.setMaxPrice} style={slideStyle}/>
    );
}


export default MaxPrice;
