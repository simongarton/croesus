import ShareSummary from '../widgets/ShareSummary.js';
import TotalValueLineMobileCard from '../widgets/TotalValueLineMobileCard.js';
import GainLossLineMobileCard from '../widgets/GainLossLineMobileCard.js';

function SharePage(props) {
  const account = props.account;
  return (
    <div className="mt-1">
      <ShareSummary account={account}></ShareSummary>
      <TotalValueLineMobileCard account={account}></TotalValueLineMobileCard>
      <GainLossLineMobileCard account={account}></GainLossLineMobileCard>
    </div>
  );
}

export default SharePage;
