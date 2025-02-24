/**
 * Type representing different down payment assistance payment types.
 *
 * @generated fLP2sm v1.4 Generated on: 2025-02-24 00:25:02 by Ollama
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
 * Type for defining down payment assistance parameters.
 *
 * @param name {string} Optional parameter to set the name.
 * @param type {'salesPrice' | 'loanAmount' | 'fixed'} Optional parameter to define the type of value.
 * @param value {number} Optional parameter to set the value.
 * @param payment {DPAPayment} Optional parameter for payment details.
 *
 * @generated so53L8 v1.4 Generated on: 2025-02-24 00:25:08 by Ollama
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
 * @param data {DPAParams | undefined} An optional object containing DPA parameters to initialize the class instance.
 *
 * @generated g41k90 v1.4 Generated on: 2025-02-24 00:25:11 by Ollama
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

