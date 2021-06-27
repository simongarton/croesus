import ShareSummary from '../widgets/ShareSummary.js';
import TotalValueLineMobileCard from '../widgets/TotalValueLineMobileCard.js';
import GainLossLineMobileCard from '../widgets/GainLossLineMobileCard.js';
import TotalValue from '../widgets/TotalValue.js';

function SharePage(props) {
  const account = props.account;
  return (
    <div className="mt-1">
      <ShareSummary account={account}></ShareSummary>
      <div className="bottom-margin"></div>
      <TotalValueLineMobileCard account={account}></TotalValueLineMobileCard>
      <GainLossLineMobileCard account={account}></GainLossLineMobileCard>
      <div className="bottom-margin"></div>
      <TotalValue account={account}></TotalValue>
    </div>
  );
}

export default SharePage;
