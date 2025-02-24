import { DownPaymentAssistance } from './downPaymentAssistance';

/**
 * This function calculates the total Down Payment Assistance (DPA) based on the given parameters.
 *
 * @param dpa {DownPaymentAssistance} The object containing the type and value of the down payment assistance.
 * @param salesPrice {number} The sales price of the property being purchased.
 * @param loanAmount {number} The loan amount for the mortgage.
 *
 * @returns { number } The calculated total down payment assistance as a number.
 *
 * @generated X4PFeu v1.3 Generated on: 2025-02-23 22:52:21 by Ollama
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
 * Returns the down payment amount based on the given DownPaymentAssistance object and sales price, loan amount.
 *
 * @param dpa {DownPaymentAssistance} An object containing details of the down payment assistance including its type and terms.
 * @param salesPrice {number} The total sales price of the property.
 * @param loanAmount {number} The loan amount being considered for financing.
 *
 * @returns { number } The calculated down payment amount based on the input parameters and conditions specified in the DownPaymentAssistance object.
 *
 * @generated fnVHaq v1.3 Generated on: 2025-02-23 22:52:31 by Ollama
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
 * Returns the monthly payment amount for a Down Payment Assistance (DPA) loan based on the given parameters.
 *
 * @param dpa {DownPaymentAssistance} The Down Payment Assistance object containing details about the assistance. (default: N/A)
 * @param salesPrice {number} The sales price of the property being purchased. (default: N/A)
 * @param loanAmount {number} The loan amount for the DPA assistance. (default: N/A)
 *
 * @returns { number } The calculated monthly payment amount or 0 if the payment type is not 'I/O'.
 *
 * @generated 8zK5sI v1.5 Generated on: 2025-02-23 22:53:15 by Ollama
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
