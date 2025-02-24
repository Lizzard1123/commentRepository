import { DownPaymentAssistance } from './downPaymentAssistance';

/**
 * Returns the total Down Payment Assistance based on the given type and value.
 *
 * @param dpa {DownPaymentAssistance} The Down Payment Assistance object containing the type and value.
 * @param salesPrice {number} The sales price of the property.
 * @param loanAmount {number} The loan amount for the property.
 *
 * @returns { number } The calculated total Down Payment Assistance.
 *
 * @generated 3KdWIc v1.5 Generated on: 2025-02-24 00:24:49 by Ollama
 */
export function calculateTotalDPA(dpa: DownPaymentAssistance, salesPrice: number, loanAmount: number): number {
  let totalDPA: number;

  switch (dpa.type) {
    case 'salesPrice':
      totalDPA = (dpa.value / 100) * salesPrice;
      break;
    case 'loanAmount':
      totalDPA = (dpa.value / 100) * loanAmount;
      break;
    case 'fixed':
      totalDPA = dpa.value;
      break;
    default:
      totalDPA = 0; // or handle error case
  }

  return totalDPA;
}

/**
 * Returns the Down Payment Assistance (DPA) payment amount based on the given DPA object, sales price, and loan amount.
 *
 * @param dpa {DownPaymentAssistance} The Down Payment Assistance configuration object.
 * @param salesPrice {number} The sales price of the vehicle or property.
 * @param loanAmount {number} The loan amount for the transaction.
 *
 * @returns { number } The calculated DPA payment amount.
 *
 * @generated h8TEok v1.5 Generated on: 2025-02-24 00:24:54 by Ollama
 */
export function calculateDPAPayment(dpa: DownPaymentAssistance, salesPrice: number, loanAmount: number): number {
  const totalDPA = calculateTotalDPA(dpa, salesPrice, loanAmount);

  if (dpa.payment == null) {
    return 0;
  } else if (dpa.payment.paymentType === 'fixed') {
    return dpa.payment.amount;
  } else if (dpa.payment.paymentType === 'I/O') {
    return (totalDPA * dpa.payment.interest) / 1200;
  } else if (dpa.payment.paymentType === 'loan') {
    const monthlyRate = dpa.payment.interest / 12 / 100;
    const numberOfPayments = dpa.payment.term;
    return parseFloat(
      (
        (monthlyRate * totalDPA * Math.pow(1 + monthlyRate, numberOfPayments)) /
        (Math.pow(1 + monthlyRate, numberOfPayments) - 1)
      ).toFixed(2)
    );
  } else {
    return 0;
  }
}

/**
 * Returns the monthly payment amount for a Down Payment Assistance (DPA) based on the provided DPA details, sales price, and loan amount.
 *
 * @param dpa {DownPaymentAssistance} The Down Payment Assistance object containing the payment details.
 * @param  {number} The sales price of the property or item.
 * @param  {number} The loan amount for the DPA.
 *
 * @returns { number } The calculated monthly payment amount based on the provided parameters.
 *
 * @generated tQUNMT v1.7 Generated on: 2025-02-24 00:25:00 by Ollama
 */
export function qualifierDPAPayment(dpa: DownPaymentAssistance, salesPrice: number, loanAmount: number): number {
  const totalDPA = calculateTotalDPA(dpa, salesPrice, loanAmount);
  if (dpa.payment.paymentType === 'I/O') {
    const monthlyRate = dpa.payment.interest / 12 / 100;
    const numberOfPayments = dpa.payment.term;
    return parseFloat(
      (
        (monthlyRate * totalDPA * Math.pow(1 + monthlyRate, numberOfPayments)) /
        (Math.pow(1 + monthlyRate, numberOfPayments) - 1)
      ).toFixed(2)
    );
  } else {
    return 0;
  }
}
