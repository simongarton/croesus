import './SingleStat.css';

import { redGreen } from '../utils';

function SingleStat(props) {
  const label = props['label'] ? props['label'] : '';
  let value = props['value']
    ? parseFloat(props['value']).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })
    : '';
  const originalValue = props['value'] ? parseFloat(props['value']) : undefined;
  if (props['currency']) {
    value = '$' + value;
  }
  if (props['percentage']) {
    value = (value * 100).toLocaleString(undefined, { minimumFractionDigits: 2 }) + '%';
  }
  let valueSpan;
  if (props['redGreen']) {
    valueSpan = <span className={redGreen(originalValue, 'single-span-value right-align code', 0)}>{value}</span>;
  } else {
    valueSpan = <span className="single-span-value right-align code">{value}</span>;
  }
  if (props['cell'] && props['cell'] === true) {
    return valueSpan;
  }
  return (
    <div>
      <span className="single-span-label left-align code">{label}</span>
      {valueSpan}
    </div>
  );
}

export default SingleStat;
