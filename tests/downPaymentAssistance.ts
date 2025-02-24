/**
 * Type representing different types of down payment assistance payments.
 *
 * @generated so8Y8J v1.2 Generated on: 2025-02-23 23:49:49 by Ollama
 */
export type DPAPayment =
  | {
      paymentType: 'fixed';
      amount: number;
    }
  | {
      paymentType: 'loan';
      interest: number;
      term: number;
    }
  | {
      paymentType: 'I/O';
      interest: number;
      term: number;
    }
  | {
      paymentType: 'none';
    };

/**
 * Type definition for parameters related to down payment assistance.
 *
 * @param name {string} An optional string representing the name of the parameter.
 * @param type {'salesPrice' | 'loanAmount' | 'fixed'} An optional string indicating the type of the parameter, which can be one of 'salesPrice', 'loanAmount', or 'fixed'.
 * @param value {number} An optional number representing the value of the parameter.
 * @param payment {DPAPayment} An optional object of type DPAPayment.
 *
 * @generated RpLAD3 v1.2 Generated on: 2025-02-23 23:49:55 by Ollama
 */
export type DPAParams = {
  name?: string;
  type?: 'salesPrice' | 'loanAmount' | 'fixed';
  value?: number;
  payment?: DPAPayment;
};

/**
 * A class for managing down payment assistance details.
 *
 * @generated egLe48 v1.2 Generated on: 2025-02-23 23:49:57 by Ollama
 */
export class DownPaymentAssistance {
  public name: string = '';
  public type: 'salesPrice' | 'loanAmount' | 'fixed' = 'salesPrice';
  public value: number = 0;
  public fee: number = 0;
  public payment: DPAPayment = {
    paymentType: 'fixed',
    amount: 0
  };

  constructor(data?: DPAParams) {
    if (data != null) {
      Object.assign(this, data);
    }
  }
}

