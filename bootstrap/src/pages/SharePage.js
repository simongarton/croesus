import ShareSummary from '../widgets/ShareSummary.js';
import TotalValueLine from '../widgets/TotalValueLine.js';
import GainLossLine from '../widgets/GainLossLine.js';
import TotalValue from '../widgets/TotalValue.js';
import TotalValueMobile from '../widgets/TotalValueMobile.js';

function SharePage(props) {
  const account = props.account;
  return (
    <div className="mt-1">
      <ShareSummary account={account}></ShareSummary>
      <div className="mb-2"></div>
      <TotalValueLine account={account}></TotalValueLine>
      <div className="mb-2"></div>
      <GainLossLine account={account}></GainLossLine>
      <div className="mb-2"></div>
      <div className="hide-on-mobile">
        <TotalValue account={account}></TotalValue>
      </div>
      <div className="hide-on-desktop">
        <TotalValueMobile account={account}></TotalValueMobile>
      </div>
      <div className="mb-2"></div>
    </div>
  );
}

export default SharePage;
