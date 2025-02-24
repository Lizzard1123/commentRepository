import { DownPaymentAssistance } from './downPaymentAssistance';

/**
 * Calculates the total Down Payment Assistance (DPA) based on the given type and values.
 *
 * @param dpa {DownPaymentAssistance} The Down Payment Assistance object containing the type and value of DPA.
 * @param salesPrice {number} The sales price of the property.
 * @param loanAmount {number} The loan amount for the property.
 *
 * @returns { number } The calculated total DPA as a number.
 *
 * @generated 5b9EyU Generated on: 2025-02-23 22:31:17 by Ollama
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
 * Returns the down payment assistance (DPA) payment amount based on the type of DPA and other parameters.
 *
 * @param dpa {DownPaymentAssistance} The Down Payment Assistance details including its type, amount, interest rate, term, and payment type (fixed, I/O, loan). (default: N/A)
 * @param salesPrice {number} The total sales price of the property. (default: N/A)
 * @param loanAmount {number} The loan amount for the property purchase. (default: N/A)
 *
 * @returns { number } The calculated down payment assistance payment amount based on the specified type and other parameters.
 *
 * @generated MP4CfM Generated on: 2025-02-23 22:31:28 by Ollama
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
 * Returns the monthly payment amount for Down Payment Assistance (DPA) with interest-only terms based on the given parameters.
 *
 * @param dpa {DownPaymentAssistance} The object containing details of the Down Payment Assistance including its type, payment amount, and term.
 * @param salesPrice {number} The sales price of the property or asset related to the DPA.
 * @param loanAmount {number} The loan amount associated with the Down Payment Assistance.
 *
 * @returns { number } The calculated monthly payment amount for the DPA with interest-only terms, rounded to 2 decimal places. If not an I/O term, returns 0.
 *
 * @generated p2K4z3 Generated on: 2025-02-23 22:31:39 by Ollama
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
