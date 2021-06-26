import TotalValueMobileCard from '../widgets/TotalValueMobileCard.js';
import TotalValueLineMobileCard from '../widgets/TotalValueLineMobileCard.js';
import GainLossLineMobileCard from '../widgets/GainLossLineMobileCard.js';

function Simon(props) {
  const account = 'simon';
  return (
    <div className="mt-1">
      <TotalValueMobileCard account={account}></TotalValueMobileCard>
      <TotalValueLineMobileCard account={account}></TotalValueLineMobileCard>
      <GainLossLineMobileCard account={account}></GainLossLineMobileCard>
    </div>
  );
}

export default Simon;
