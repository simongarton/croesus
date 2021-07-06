import ShareSummary from '../widgets/ShareSummary.js';
import TotalValueLine from '../widgets/TotalValueLine.js';
import GainLossLine from '../widgets/GainLossLine.js';
import TotalValue from '../widgets/TotalValue.js';
import TotalValueMobile from '../widgets/TotalValueMobile.js';
import TotalValueHorizontalBar from '../widgets/TotalValueHorizontalBar.js';
import GainLossHorizontalBar from '../widgets/GainLossHorizontalBar.js';
import GainLossPercentageHorizontalBar from '../widgets/GainLossPercentageHorizontalBar.js';
import CAGRHorizontalBar from '../widgets/CAGRHorizontalBar.js';
import HoldingPie from '../widgets/HoldingPie.js';
import HostPie from '../widgets/HostPie.js';
import AccountPie from '../widgets/AccountPie.js';
import ExchangePie from '../widgets/ExchangePie.js';
import RegionPie from '../widgets/RegionPie.js';
import TypePie from '../widgets/TypePie.js';

function SharePage(props) {
  const account = props.account;
  const mqlMobile = window.matchMedia('(max-width: 480px)');
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
  let accountPie = <div />;
  if (account === 'all') {
    accountPie = <AccountPie account={account}></AccountPie>;
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
      <TotalValueHorizontalBar account={account}></TotalValueHorizontalBar>
      <GainLossHorizontalBar account={account}></GainLossHorizontalBar>
      <GainLossPercentageHorizontalBar account={account}></GainLossPercentageHorizontalBar>
      <CAGRHorizontalBar account={account}></CAGRHorizontalBar>
      <HoldingPie account={account}></HoldingPie>
      <RegionPie account={account}></RegionPie>
      <TypePie account={account}></TypePie>
      <ExchangePie account={account}></ExchangePie>
      <HostPie account={account}></HostPie>
      {accountPie}
      <div className="mb-2"></div>
    </div>
  );
}

export default SharePage;
