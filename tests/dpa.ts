import { DownPaymentAssistance } from './downPaymentAssistance';

/**
 * Determines the total down payment assistance (DPA) based on the type of DPA and either sales price or loan amount.
 *
 * @param dpa {DownPaymentAssistance} The DownPaymentAssistance object containing the type and value of DPA.
 * @param salesPrice {number} The sales price of the property or item being purchased.
 * @param loanAmount {number} The loan amount for the purchase transaction.
 *
 * @returns { number } The calculated total down payment assistance as a number value.
 *
 * @generated xNDZZd Generated on: 2025-02-23 21:57:54 by Ollama
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
 * Returns the calculated down payment assistance (DPA) payment based on the given DPA object, sales price, and loan amount.
 *
 * @param dpa {DownPaymentAssistance} The Down Payment Assistance details including type of payment and other relevant information.
 * @param salesPrice {number} The total sales price of the property.
 * @param loanAmount {number} The loan amount being considered for the down payment assistance calculation.
 *
 * @returns { number } The calculated DPA payment amount.
 *
 * @generated JYMnJZ Generated on: 2025-02-23 21:58:03 by Ollama
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
 * Returns the monthly payment for an I/O (Interest-Only) Down Payment Assistance plan based on the given parameters.
 *
 * @param dpa {DownPaymentAssistance} The Down Payment Assistance object containing payment details.
 * @param salesPrice {number} The total sales price of the property.
 * @param loanAmount {number} The loan amount for the property purchase.
 *
 * @returns { number } The calculated monthly payment or 0 if not an I/O plan.
 *
 * @generated kSvZ6p Generated on: 2025-02-23 21:58:11 by Ollama
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
