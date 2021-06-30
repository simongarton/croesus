import ShareSummary from '../widgets/ShareSummary.js';
import TotalValueLine from '../widgets/TotalValueLine.js';
import GainLossLine from '../widgets/GainLossLine.js';
import TotalValue from '../widgets/TotalValue.js';
import TotalValueMobile from '../widgets/TotalValueMobile.js';

function SharePage(props) {
  const account = props.account;
  const mqlMobile = window.matchMedia('(max-width: 480px)');
  const mqlDesktop = window.matchMedia('not all and (max-width: 480px)');
  console.log(mqlMobile);
  console.log(mqlDesktop);
  let value;
  if (mqlMobile.matches) {
    value = <TotalValueMobile account={account} small="true"></TotalValueMobile>;
  } else {
    value = (
      <div>
        <TotalValue account={account}></TotalValue>
        <TotalValueMobile account={account} small="false"></TotalValueMobile>
      </div>
    );
  }
  return (
    <div className="mt-1">
      <ShareSummary account={account}></ShareSummary>
      <div className="mb-2"></div>
      <TotalValueLine account={account}></TotalValueLine>
      <div className="mb-2"></div>
      <GainLossLine account={account}></GainLossLine>
      <div className="mb-2"></div>
      <div>{value}</div>
      <div className="mb-2"></div>
    </div>
  );
}

export default SharePage;
