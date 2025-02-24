import { DownPaymentAssistance } from './downPaymentAssistance';

/**
 * Calculates the total down payment assistance (DPA) based on the given DPA type and either sales price or loan amount.
 *
 * @returns The calculated total DPA as a number
 *
 * @generated ZSDJe8 Generated on: 2025-02-23 21:19:46 by Ollama
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
 * Calculates the down payment assistance (DPA) payment based on the type of payment specified in the DownPaymentAssistance object.
 *
 * @returns number representing the calculated DPA payment amount
 *
 * @generated D0f78a Generated on: 2025-02-23 21:19:50 by Ollama
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
 * Calculates the payment amount for a down payment assistance program based on the type of payment (Interest-Only or otherwise).
 *
 * @returns number representing the calculated payment amount or 0 if not interest-only
 *
 * @generated ma3zPJ Generated on: 2025-02-23 21:19:54 by Ollama
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
