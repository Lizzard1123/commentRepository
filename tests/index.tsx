// PreAppSlider.tsx
import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Sheet, SheetTrigger, SheetContent, SheetTitle, SheetDescription } from '@/components/ui/sheet';
import * as FormattedNumbers from '@/utils/formattedNumber';
import { CellInput } from '../../../ui/CellInput';
import { WritableDraft } from 'immer';
import { Borrower } from '@/models/clientProfile';
import { PlusIcon, TrashIcon } from '@/components/ui/Icons';
import { VisuallyHidden } from '@chakra-ui/react';
import ApprovalButton from './approvalButton';
import QualificationMessage from './qualificationMessage';
import { Popover, PopoverContent, PopoverTrigger } from '@/components/ui/popover';
import { useOfficerContext } from '@/context/officer';
import { Separator } from '@/components/ui/separator';
import { AddNewRealtorDialogue } from '@/components/alerts/addNewRealtorDialogue';
import { CRUD } from '@/context/officer/editCacher';
import { cn } from '@/utils/utils';
import CommandSelectTop from '@/components/ui/commandSelectButtonTop';
import { CalculatorButton } from '@/components/ui/Calculator';
import { CalculatorState } from '@/components/ui/Calculator';
import { TextInput } from '@/components/ui/TextInput';

/**
 * A function to format a phone number by removing non-digit characters and adding appropriate formatting.
 *
 * @param value {string} The input string containing the phone number to be formatted.
 *
 * @returns { any } A formatted string representing the phone number, or an empty string if the input is invalid.
 *
 * @generated V52Pwd v1.0 Generated on: 2025-02-24 12:11:17 by Ollama
 */
const formatPhoneNumber = (value: string) => {
  // Remove all non-digit characters
  const phoneNumber = value.replace(/\D/g, '');

  // Format the number as (XXX) XXX-XXXX
  if (phoneNumber.length >= 10) {
    return `(${phoneNumber.slice(0, 3)}) ${phoneNumber.slice(3, 6)}-${phoneNumber.slice(6, 10)}`;
  } else if (phoneNumber.length > 6) {
    return `(${phoneNumber.slice(0, 3)}) ${phoneNumber.slice(3, 6)}-${phoneNumber.slice(6)}`;
  } else if (phoneNumber.length > 3) {
    return `(${phoneNumber.slice(0, 3)}) ${phoneNumber.slice(3)}`;
  } else if (phoneNumber.length > 0) {
    return `(${phoneNumber}`;
  }
  return '';
};

/**
 * A function that creates a slider for pre-application borrower information, including various inputs and logic to manage borrowers' details.
 *
 * @param Start Line {41} The start line of the function in the source code.
 * @param End Line {587} The end line of the function in the source code.
 *
 * @returns { any } The function returns JSX elements representing the UI for borrower information management.
 *
 * @generated yCVJvk v1.0 Generated on: 2025-02-24 12:11:49 by Ollama
 */
const PreAppSlider = () => {
  const { updateOfficerState, activeProfile, activeOption, activeLoan, updateActiveProfile, pushUpdates, realtors } =
    useOfficerContext();
  const [isNewRealtorDialogOpen, setIsNewRealtorDialogOpen] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);
  const [calculatorStates, setCalculatorStates] = useState<{ [key: string]: CalculatorState }>({});
  const [emailErrors, setEmailErrors] = useState<{ [key: string]: boolean }>({});
  const [phoneErrors, setPhoneErrors] = useState<{ [key: string]: boolean }>({});
  const totalPages = activeProfile.additionalBorrowers.length + 1;

  if (currentPage > activeProfile.additionalBorrowers.length + 1) {
    setCurrentPage(1);
    return;
  }

  const currentBorrower =
    currentPage === 1 ? activeProfile.primaryBorrower : activeProfile.additionalBorrowers[currentPage - 2];
  /**
   * A function to update the current borrower based on the currentPage.
   *
   * @param updater {(draft: WritableDraft<Borrower>) => void} A function that updates the draft of the borrower.
   *
   * @returns { any (omit if not a function) } Omit as this is a function and does not return a value.
   *
   * @generated SveIcT v1.0 Generated on: 2025-02-24 12:11:56 by Ollama
   */
  const updateCurrentBorrower = (updater: (draft: WritableDraft<Borrower>) => void) => {
    updateActiveProfile((draft) => {
      updater(currentPage === 1 ? draft.primaryBorrower : draft.additionalBorrowers[currentPage - 2]);
    });
  };

  /**
   * A function to add a new borrower when the total pages are less than 4.
   *
   * @returns { any } The function does not explicitly return anything, but updates state or performs side effects.
   *
   * @generated bM4L0J v1.0 Generated on: 2025-02-24 12:12:00 by Ollama
   */
  const handleAddBorrower = () => {
    if (totalPages < 4) {
      updateActiveProfile((draft) => {
        draft.additionalBorrowers.push(new Borrower());
      });
      setCurrentPage(totalPages + 1);
    }
  };

  /**
   * A function to handle the previous page action by decrementing the current page number if it is greater than 1.
   *
   * @param Not explicitly defined (arrow function) {-} -
   *
   * @returns { any } The function returns nothing, but updates the state.
   *
   * @generated 4fFNOI v1.1 Generated on: 2025-02-24 12:15:06 by Ollama
   */
  const handlePrevious = () => {
    if (currentPage > 1) {
      setCurrentPage(currentPage - 1);
    }
  };

  /**
   * A function to increment the current page by one if it is less than the total number of pages.
   *
   * @param none {none} This function does not take any parameters.
   *
   * @returns { any } The return type is not explicitly defined in the function, hence it is of type any.
   *
   * @generated QzUg5h v1.3 Generated on: 2025-02-24 12:18:18 by Ollama
   */
  const handleNext = () => {
    if (currentPage < totalPages) {
      setCurrentPage(currentPage + 1);
    }
  };
  const salesPrice = activeOption.salesPrice || 0; // Ensure it has a default value if not provided

  const loanAmount = activeLoan.getLoanAmount();
  const incomeDeficit = activeLoan.getShortfallOrExcessIncome(loanAmount);
  const housingRatioIncomeDeficit = activeLoan.getIncomeHousingRatioSurplusDeficit(loanAmount);
  const dtiIncomeDeficit = activeLoan.getIncomeDTISurplusDeficit(loanAmount);
  const housingRatioLiabilitiesDeficit = activeLoan.getLiabilitiesHousingRatioSurplusDeficit(loanAmount);
  const dtiLiabilitiesDeficit = activeLoan.getLiabilitiesDTISurplusDeficit(loanAmount);
  const newLAMaxDU = activeLoan.getNewLAMaxDU(loanAmount);
  const newLAMaxDTI = activeLoan.getNewLAMaxDTI(loanAmount);
  const liabilitiesDeficit = activeLoan.getShortfallOrExcessLiabilities(loanAmount);

  //conditional rendering checks and variables:
  // Reduce LA to variables:
  // const isDUMoreRestrictive = (Math.abs(newLAMaxDU) <= Math.abs(newLAMaxDTI) && housingRatioLiabilitiesDeficit > 0);
  // const isDTIMoreRestrictive = (Math.abs(newLAMaxDTI) <= Math.abs(newLAMaxDU) && dtiLiabilitiesDeficit > 0);

  //reduce liabilities checks:
  const isHousingLower = Math.abs(housingRatioLiabilitiesDeficit) <= Math.abs(dtiLiabilitiesDeficit);

  /**
   * A function to update the state of a calculator for a specific borrower.
   *
   * @param borrowerId {string} The unique identifier for the borrower whose state is being updated.
   * @param state {CalculatorState} The new state to be set for the specified borrower.
   *
   * @returns { any } This function does not return a value.
   *
   * @generated tBOacV v1.0 Generated on: 2025-02-24 12:12:18 by Ollama
   */
  const handleCalculatorStateChange = (borrowerId: string, state: CalculatorState) => {
    setCalculatorStates((prev) => ({
      ...prev,
      [borrowerId]: state
    }));
  };

  /**
   * A function to update the income of the current borrower based on the provided monthly income.
   *
   * @param monthlyIncome {number} The monthly income to update the current borrower's income with.
   *
   * @returns { any (omitted due to not being a function) } Omit as it is not a function.
   *
   * @generated chMngo v1.0 Generated on: 2025-02-24 12:12:23 by Ollama
   */
  const handleCalculatorResult = (monthlyIncome: number) => {
    updateCurrentBorrower((x) => (x.income = monthlyIncome));
  };

  /**
   * A function to validate if a given email string is valid.
   *
   * @param email {string} The email address to be validated.
   *
   * @returns { any } A boolean value indicating whether the provided email is valid or not.
   *
   * @generated OjixOd v1.0 Generated on: 2025-02-24 12:12:29 by Ollama
   */
  const isValidEmail = (email: string) => {
    return !email || /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  };

  /**
   * A function to validate if a given phone number is valid based on length.
   *
   * @param phone {string} The phone number to be validated.
   *
   * @returns { any } A boolean indicating whether the phone number is valid or not.
   *
   * @generated ktUxIs v1.0 Generated on: 2025-02-24 12:12:34 by Ollama
   */
  const isValidPhone = (phone: string) => {
    return !phone || phone.replace(/\D/g, '').length === 10;
  };

  /**
   * A function to handle email change events, updating the state with validation errors and current borrower's email.
   *
   * @param e {React.ChangeEvent<HTMLInputElement>} The event generated by the input element change.
   * @param borrowerId {string} The ID of the borrower whose email is being updated.
   *
   * @returns { any (omitted as not a function returning type) } Omitted as this function does not return any value.
   *
   * @generated gORV9K v1.0 Generated on: 2025-02-24 12:12:42 by Ollama
   */
  const handleEmailChange = (e: React.ChangeEvent<HTMLInputElement>, borrowerId: string) => {
    const value = e.target.value;
    const hasError = !isValidEmail(value);
    setEmailErrors((prev) => ({ ...prev, [borrowerId]: hasError }));
    updateCurrentBorrower((x) => (x.email = value));
  };

  /**
   * A function to handle phone number change events and update state accordingly.
   *
   * @param e {React.ChangeEvent<HTMLInputElement>} The event object containing the target element and its value.
   * @param borrowerId {string} The ID of the borrower associated with the phone number being updated.
   *
   * @returns { any (omit if not a function) } No explicit return value, updates state internally.
   *
   * @generated CSeMdr v1.0 Generated on: 2025-02-24 12:12:50 by Ollama
   */
  const handlePhoneChange = (e: React.ChangeEvent<HTMLInputElement>, borrowerId: string) => {
    const value = e.target.value;
    const formattedPhone = formatPhoneNumber(value);
    const hasError = !isValidPhone(value);
    setPhoneErrors((prev) => ({ ...prev, [borrowerId]: hasError }));
    updateCurrentBorrower((x) => (x.phone = formattedPhone.replace(/\D/g, '').slice(0, 10)));
  };

  return (
    <Sheet onOpenChange={(open) => !open && pushUpdates()}>
      <VisuallyHidden>
        <SheetTitle>Pre-App</SheetTitle>
      </VisuallyHidden>
      <VisuallyHidden>
        <SheetDescription>Pre-App</SheetDescription>
      </VisuallyHidden>
      <SheetTrigger asChild>
        <Button
          variant='ghost'
          size='sm'
          className={cn(
            'px-4 py-2 rounded-lg',
            'bg-gradient-to-br from-slate-200/90 via-slate-100/90 to-slate-200/90',
            'hover:from-slate-100 hover:via-slate-50 hover:to-slate-100',
            'text-slate-700 hover:text-slate-800',
            'border border-slate-300/50 hover:border-slate-300',
            'shadow-[0_2px_10px_-2px] shadow-slate-300/30',
            'hover:shadow-[0_4px_20px_-4px] hover:shadow-slate-400/40',
            'transition-all duration-300',
            'hover:scale-[1.02] active:scale-[0.98]',
            'relative',
            'font-medium',
            'flex items-center gap-2',
            'backdrop-blur-[2px]',
            'ring-1 ring-slate-200/30'
          )}>
          <svg className='w-4 h-4' fill='none' viewBox='0 0 24 24' stroke='currentColor' strokeWidth={2}>
            <path
              strokeLinecap='round'
              strokeLinejoin='round'
              d='M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z'
            />
          </svg>
          Borrower Info
        </Button>
      </SheetTrigger>
      <Popover>
        <PopoverTrigger asChild>
          <ApprovalButton isApproved={activeLoan.isApproved} />
        </PopoverTrigger>
        <PopoverContent className='w-[500px]'>
          <div className=''>
            <QualificationMessage
              isRealtor={false}
              isApproved={activeLoan.isApproved}
              incomeDeficit={incomeDeficit}
              liabilitiesDeficit={liabilitiesDeficit}
              housingRatioIncomeDeficit={housingRatioIncomeDeficit}
              housingRatioLiabilitiesDeficit={housingRatioLiabilitiesDeficit}
              dtiIncomeDeficit={dtiIncomeDeficit}
              dtiLiabilitiesDeficit={dtiLiabilitiesDeficit}
              newLAMaxDU={newLAMaxDU}
              newLAMaxDTI={newLAMaxDTI}
              salesPrice={salesPrice}
            />
          </div>
        </PopoverContent>
      </Popover>
      <SheetContent
        side='left'
        className={cn(
          'w-[40%] !max-w-full sm:!max-w-full border-r-8 overflow-auto',
          activeLoan.isApproved ? 'border-green-700' : 'border-red-700',
          'border-8'
        )}>
        <div className='p-4 flex flex-col space-y-6'>
          <div className='flex justify-between items-center'>
            <h2 className='text-lg font-bold'>Borrower Financial Information</h2>
            <Button
              variant='ghost'
              size='sm'
              className='ml-2 px-2 py-2 rounded-lg border border-black bg-[#00064A] text-white hover:bg-gray-100 hover:border-black hover:text-black'
              onClick={handleAddBorrower}
              disabled={totalPages >= 4}>
              Add Borrower
            </Button>
          </div>
          <div className='flex justify-between items-center mt-4'>
            <Button
              variant='ghost'
              size='sm'
              className='ml-2 px-2 py-2 rounded-lg border border-black bg-[#00064A] text-white hover:bg-gray-100 hover:border-black hover:text-black disabled:opacity-50'
              onClick={handlePrevious}
              disabled={currentPage === 1}>
              Previous
            </Button>
            <div>
              Borrower {currentPage} of {totalPages}
            </div>
            <Button
              variant='ghost'
              size='sm'
              className='ml-2 px-2 py-2 rounded-lg border border-black bg-[#00064A] text-white hover:bg-gray-100 hover:border-black hover:text-black disabled:opacity-50'
              onClick={handleNext}
              disabled={currentPage === totalPages}>
              Next
            </Button>
          </div>
          <div className='mt-4'>
            <div className='flex flex-1 flex-row justify-between py-1'>
              <div className='font-medium text-black'>Borrower Name</div>
              <div className='flex flex-row w-1/2 justify-between items-center'>
                {currentPage > 1 && (
                  <Button
                    className='bg-bla h-7 w-7 mr-3 !px-0 !py-0'
                    onClick={() => {
                      updateOfficerState((x) => {
                        x.getEditCache().borrowerEditCache.set(currentBorrower.slug, CRUD.DELETE); // manually add delete to update collector
                        x.getLoanPicker().deleteAdditionalBorrower(currentBorrower.slug);
                      });
                      pushUpdates();
                      handlePrevious();
                    }}>
                    <TrashIcon className='w-3 h-3' />
                  </Button>
                )}

                {/* <Input
                  id='borrower_name'
                  className='!w-auto flex-1'
                  value={currentBorrower.name}
                  onChange={(e) => updateCurrentBorrower((x) => (x.name = e.target.value))}
                /> */}
                <TextInput
                  id='borrower_name'
                  className='!w-auto flex-1'
                  defaultValue={currentBorrower.name}
                  setData={(inputValue) =>
                    updateCurrentBorrower((x) => {
                      x.name = inputValue;
                    })
                  }
                />
              </div>
            </div>

            <div className='flex flex-1 flex-row justify-between py-1'>
              <div className='font-medium text-black'>Borrower Email</div>
              <div className='flex flex-row w-1/2 justify-between items-center'>
                <TextInput
                  type='email'
                  value={currentBorrower.email}
                  onChange={(e) => handleEmailChange(e, currentBorrower.slug)}
                  className={cn('w-full', emailErrors[currentBorrower.slug] && 'border-red-500')}
                  id='borrower_email'
                  placeholder='Enter email'
                  defaultValue={currentBorrower.email}
                  onSubmit={(e) => {
                    e.preventDefault();
                    const value = (e.target as HTMLInputElement).value;
                    if (!value || isValidEmail(value)) {
                      updateCurrentBorrower((x) => {
                        x.email = value;
                      });
                    }
                  }}
                />
              </div>
            </div>
            <div className='flex flex-1 flex-row justify-between py-1'>
              <div className='font-medium text-black'>Borrower Phone</div>
              <div className='flex flex-row w-1/2 justify-between items-center'>
                <TextInput
                  type='tel'
                  value={currentBorrower.phone ? formatPhoneNumber(currentBorrower.phone) : ''}
                  onChange={(e) => handlePhoneChange(e, currentBorrower.slug)}
                  className={cn('w-full', phoneErrors[currentBorrower.slug] && 'border-red-500')}
                  id='borrower_phone'
                  placeholder='(XXX) XXX-XXXX'
                  defaultValue={currentBorrower.phone ? formatPhoneNumber(currentBorrower.phone) : ''}
                  onSubmit={(e) => {
                    e.preventDefault();
                    const value = (e.target as HTMLInputElement).value;
                    if (!value || isValidPhone(value)) {
                      updateCurrentBorrower((x) => {
                        x.phone = value.replace(/\D/g, '').slice(0, 10);
                      });
                    }
                  }}
                />
              </div>
            </div>
            {currentPage === 1 && (
              <>
                <div className='flex flex-1 flex-row justify-between py-1'>
                  <div className='font-medium text-black'>Realtor</div>
                  <CommandSelectTop
                    className='!w-1/2'
                    defaultSearchTerm={realtors.find((x) => x.slug === activeProfile.realtorContactSlug)?.name ?? ''}
                    items={realtors}
                    onSelect={(realtor) => {
                      updateActiveProfile((x) => {
                        x.realtorContactSlug = realtor ? realtor.slug : '';
                      });
                    }}
                    placeholder='No Matching Realtor Found.'
                    getItemText={(realtor) => realtor.name}>
                    <Button
                      variant='ghost'
                      className='w-full h-6 justify-start hover:bg-gray-200 dark:hover:bg-gray-700 py-4'
                      onMouseDown={() => {
                        setIsNewRealtorDialogOpen(true);
                      }}>
                      <PlusIcon className='h-4 w-4 mr-2' />
                      Add New Realtor
                    </Button>
                    <Separator />
                    <AddNewRealtorDialogue
                      open={isNewRealtorDialogOpen}
                      onOpenChange={(open) => setIsNewRealtorDialogOpen(open)}
                      onSubmit={(realtor) => updateActiveProfile((x) => (x.realtorContactSlug = realtor.slug))}
                    />
                  </CommandSelectTop>
                </div>
                <div className='flex flex-1 flex-row justify-between py-1'>
                  <div className='font-medium text-black'>Referral Source</div>
                  {/* <Input
                    id='referral_source'
                    className='!w-1/2'
                    value={activeProfile.referralSource}
                    onChange={(e) => {
                      updateActiveProfile((x) => {
                        x.referralSource = e.target.value;
                      });
                    }}
                  /> */}
                  <TextInput
                    id='referral_source'
                    className='!w-1/2'
                    defaultValue={activeProfile.referralSource}
                    setData={(inputValue) =>
                      updateActiveProfile((x) => {
                        x.referralSource = inputValue;
                      })
                    }
                  />
                </div>
              </>
            )}
            <div className='flex flex-col flex-1 py-1 space-y-2'>
              <div className='flex flex-1 flex-row justify-between items-center'>
                <div className='flex items-center'>
                  <div className='font-medium text-black'>Income (monthly)</div>
                  <CalculatorButton
                    onResult={(value) => handleCalculatorResult(value)}
                    initialState={calculatorStates[currentBorrower.slug]}
                    onStateChange={(state) => handleCalculatorStateChange(currentBorrower.slug, state)}
                  />
                </div>
                <CellInput
                  id='income'
                  className='!w-1/2'
                  defaultValue={currentBorrower.income}
                  dataType={FormattedNumbers.money}
                  setData={(update) => {
                    if (update !== currentBorrower.income) {
                      updateCurrentBorrower((x) => (x.income = update));
                    }
                  }}
                />
              </div>
              {totalPages === 1 && (
                <div className='flex flex-1 justify-between items-center'>
                  {incomeDeficit >= 0 && activeLoan.isApproved ? (
                    <div className='text-green-700 font-semibold'>
                      Income available: {FormattedNumbers.money.toString(Math.abs(incomeDeficit))}
                    </div>
                  ) : (
                    <div className='text-red-700 font-semibold'>
                      Income Short by {FormattedNumbers.money.toString(Math.abs(incomeDeficit))}
                    </div>
                  )}
                </div>
              )}
              {totalPages > 1 && (
                <>
                  <div className='flex flex-1 flex-row justify-between items-center'>
                    <div className='font-medium text-black'>Combined Incomes</div>
                    <div className='w-1/2 border-b border-black text-end py-2 px-3 h-10'>
                      {FormattedNumbers.money.toString(activeLoan.getTotalIncome())}
                    </div>
                  </div>
                  <div className='flex flex-1 justify-between items-center'>
                    {incomeDeficit >= 0 && activeLoan.isApproved ? (
                      <div className='text-green-700 font-semibold'>
                        Income Available: {FormattedNumbers.money.toString(Math.abs(incomeDeficit))}
                      </div>
                    ) : (
                      <div className='text-red-700 font-semibold'>
                        Income Short by {FormattedNumbers.money.toString(Math.abs(incomeDeficit))}
                      </div>
                    )}
                  </div>
                </>
              )}
            </div>
            <div className='flex flex-1 flex-row justify-between py-4'>
              <div className='font-medium text-black'>Car Payments</div>
              <CellInput
                id='car_payments'
                className='!w-1/2'
                defaultValue={currentBorrower.carPayments}
                dataType={FormattedNumbers.money}
                setData={(update) => updateCurrentBorrower((x) => (x.carPayments = update))}
              />
            </div>
            <div className='flex flex-1 flex-row justify-between py-4'>
              <div className='font-medium text-black'>Credit Card Loan Payments</div>
              <CellInput
                id='credit_card_payments'
                className='!w-1/2'
                defaultValue={currentBorrower.creditCardPayments}
                dataType={FormattedNumbers.money}
                setData={(update) => updateCurrentBorrower((x) => (x.creditCardPayments = update))}
              />
            </div>
            <div className='flex flex-1 flex-row justify-between py-4'>
              <div className='font-medium text-black'>Student Loan Payments</div>
              <CellInput
                id='student_loan_payments'
                className='!w-1/2'
                defaultValue={currentBorrower.studentLoanPayments}
                dataType={FormattedNumbers.money}
                setData={(update) => updateCurrentBorrower((x) => (x.studentLoanPayments = update))}
              />
            </div>
            <div className='flex flex-1 flex-row justify-between py-4'>
              <div className='font-medium text-black'>Rent Loss</div>
              <CellInput
                id='rent_loss'
                className='!w-1/2'
                defaultValue={currentBorrower.rentLoss}
                dataType={FormattedNumbers.money}
                setData={(update) => updateCurrentBorrower((x) => (x.rentLoss = update))}
              />
            </div>
            <div
              className={`flex flex-1 flex-row justify-between py-4 ${
                currentPage > 1 ? 'opacity-50 pointer-events-none' : ''
              }`}>
              <div className='font-medium text-black'>Total Credit Payments</div>
              <div className='w-1/2 border-b border-black text-end py-2 px-3 h-10'>
                {FormattedNumbers.money.toString(currentBorrower.totalPayments)}
              </div>
            </div>
            {totalPages > 1 && (
              <div className='flex flex-1 flex-row justify-between py-4'>
                <div className='font-medium text-black'>Combined Total Credit Payments</div>
                <div className='w-1/2 border-b border-black text-end py-2 px-3 h-10'>
                  {FormattedNumbers.money.toString(activeProfile.getTotalMonthlyPayments())}
                </div>
              </div>
            )}
            <div className={`flex flex-1 flex-row justify-between py-4`}>
              <div className='font-medium text-black'>
                Mortgage Payment
                {housingRatioLiabilitiesDeficit <= 0 && activeLoan.isApproved ? (
                  <div className='text-green-700 font-semibold'>
                    {' '}
                    Mortg. Pmt Available: {FormattedNumbers.money.toString(Math.abs(housingRatioLiabilitiesDeficit))}
                  </div>
                ) : housingRatioLiabilitiesDeficit > 0 && dtiLiabilitiesDeficit < housingRatioLiabilitiesDeficit ? (
                  <div className='text-red-700 font-semibold '>
                    Mortg. Pmt over by: {FormattedNumbers.money.toString(Math.abs(liabilitiesDeficit))}
                  </div>
                ) : null}
              </div>
              <div className='w-1/2 border-b border-black text-end py-2 px-3 h-10'>
                {FormattedNumbers.money.toString(activeLoan.getTotalMonthly(loanAmount))}
              </div>
            </div>
            <div
              className={`flex flex-1 flex-row justify-between py-4 ${
                currentPage > 1 ? 'opacity-50 pointer-events-none' : ''
              }`}>
              <div className='font-medium text-black'>
                Total Liabilities
                {dtiLiabilitiesDeficit <= 0 && activeLoan.isApproved ? (
                  <div className='text-green-700 font-semibold'>
                    {' '}
                    Total Liabilities Available: {FormattedNumbers.money.toString(Math.abs(dtiLiabilitiesDeficit))}
                  </div>
                ) : dtiLiabilitiesDeficit > 0 && !isHousingLower && liabilitiesDeficit <= dtiLiabilitiesDeficit ? (
                  <div className='text-red-700 font-semibold '>
                    Total Liabilities over by: {FormattedNumbers.money.toString(Math.abs(liabilitiesDeficit))}
                  </div>
                ) : null}
              </div>
              <div className='w-1/2 border-b border-black text-end py-2 px-3 h-10'>
                {FormattedNumbers.money.toString(activeLoan.getTotalPaymentsWithMortgage(loanAmount))}
              </div>
            </div>
            {totalPages > 1 && (
              <div className='flex flex-1 flex-row justify-between py-4'>
                <div className='font-medium text-black'>
                  Combined Total Liabilities
                  {dtiLiabilitiesDeficit <= 0 && activeLoan.isApproved ? (
                    <div className='text-green-700 font-semibold'>
                      {' '}
                      Total Liabilities Available: {FormattedNumbers.money.toString(Math.abs(dtiLiabilitiesDeficit))}
                    </div>
                  ) : dtiLiabilitiesDeficit > 0 && !isHousingLower && liabilitiesDeficit <= dtiLiabilitiesDeficit ? (
                    <div className='text-red-700 font-semibold '>
                      Total Liabilities over by: {FormattedNumbers.money.toString(Math.abs(liabilitiesDeficit))}
                    </div>
                  ) : null}
                </div>
                <div className='w-1/2 border-b border-black text-end py-2 px-3 h-10'>
                  {FormattedNumbers.money.toString(activeLoan.getTotalPaymentsWithMortgage(loanAmount))}
                </div>
              </div>
            )}
            <div className={`flex flex-col flex-1 py-4 ${currentPage > 1 ? 'opacity-50 pointer-events-none' : ''}`}>
              <div className='flex flex-1 flex-row justify-between items-center'>
                <div className='font-medium text-black'>Housing Ratio</div>
                <div className='w-1/2 border-b border-black text-end py-2 px-3 h-10'>
                  {FormattedNumbers.percentage.toString(activeLoan.getHousingRatio(loanAmount))}
                </div>
              </div>
            </div>
            <div className={`flex flex-col flex-1 py-4 ${currentPage > 1 ? 'opacity-50 pointer-events-none' : ''}`}>
              <div className='flex flex-1 flex-row justify-between items-center'>
                <div className='font-medium text-black'>Debt to Income Ratio</div>
                <div className='w-1/2 border-b border-black text-end py-2 px-3 h-10'>
                  {FormattedNumbers.percentage.toString(activeLoan.getDTI(loanAmount))}
                </div>
              </div>
            </div>
          </div>

          <QualificationMessage
            isRealtor={false}
            isApproved={activeLoan.isApproved}
            incomeDeficit={incomeDeficit}
            liabilitiesDeficit={liabilitiesDeficit}
            housingRatioIncomeDeficit={housingRatioIncomeDeficit}
            housingRatioLiabilitiesDeficit={housingRatioLiabilitiesDeficit}
            dtiIncomeDeficit={dtiIncomeDeficit}
            dtiLiabilitiesDeficit={dtiLiabilitiesDeficit}
            newLAMaxDU={newLAMaxDU}
            newLAMaxDTI={newLAMaxDTI}
            salesPrice={salesPrice}
          />
        </div>
      </SheetContent>
    </Sheet>
  );
};

export default PreAppSlider;
