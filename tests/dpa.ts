import { DownPaymentAssistance } from './downPaymentAssistance';

/**
 * Returns the total down payment assistance (DPA) based on the provided DPA type and relevant sales price or loan amount.
 *
 * @param dpa {DownPaymentAssistance} The object containing the DPA type and value.
 * @param salesPrice {number} The sales price of the property or item being purchased.
 * @param loanAmount {number} The loan amount for financing the purchase.
 *
 * @returns { number } The calculated total down payment assistance as a number.
 *
 * @generated 7vtq1g v1.1 Generated on: 2025-02-23 22:41:21 by Ollama
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
 * Returns the down payment assistance (DPA) payment amount based on different payment types.
 *
 * @param dpa {DownPaymentAssistance} The DownPaymentAssistance object containing the details of the DPA payment type and other relevant information.
 * @param salesPrice {number} The total sales price of the property being purchased.
 * @param loanAmount {number} The loan amount for the mortgage on the property.
 *
 * @returns { number } The calculated DPA payment amount based on the specified payment type and other parameters.
 *
 * @generated HWfLL7 v1.1 Generated on: 2025-02-23 22:41:31 by Ollama
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
 * Returns the monthly payment amount for a Down Payment Assistance (DPA) program based on the type of payment and other parameters.
 *
 * @param dpa {DownPaymentAssistance} The Down Payment Assistance object containing details such as payment type, interest rate, and term.
 * @param salesPrice {number} The sales price of the property associated with the DPA program.
 * @param loanAmount {number} The loan amount for which the Down Payment Assistance is being calculated.
 *
 * @returns { number } The monthly payment amount for the DPA program, formatted to two decimal places. Returns 0 if the payment type is not 'I/O'.
 *
 * @generated G5YgvA v1.1 Generated on: 2025-02-23 22:41:41 by Ollama
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
