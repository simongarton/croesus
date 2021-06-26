import TotalValueMobileCard from '../widgets/TotalValueMobileCard.js';
import TotalValueLineMobileCard from '../widgets/TotalValueLineMobileCard.js';
import GainLossLineMobileCard from '../widgets/GainLossLineMobileCard.js';

function Helen(props) {
  const account = 'helen';
  return (
    <div className="mt-1">
      <TotalValueMobileCard account={account}></TotalValueMobileCard>
      <TotalValueLineMobileCard account={account}></TotalValueLineMobileCard>
      <GainLossLineMobileCard account={account}></GainLossLineMobileCard>
    </div>
  );
}

export default Helen;
