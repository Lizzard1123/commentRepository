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

export type DPAParams = {
  name?: string;
  type?: 'salesPrice' | 'loanAmount' | 'fixed';
  value?: number;
  payment?: DPAPayment;
};

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
