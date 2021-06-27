export function removeNegativeZero(amount, decimalPlaces) {
  if (!amount) {
    return amount;
  }
  let amt = amount.toFixed(decimalPlaces);
  return amt;
}

export function redGreen(amount, otherStyles, decimalPlaces) {
  let amt = removeNegativeZero(amount, decimalPlaces);
  if (Number(amt) < 0) {
    return otherStyles + ' red-text';
  }
  if (Number(amt) >= 0) {
    return otherStyles + ' green-text';
  }
  return otherStyles;
}
