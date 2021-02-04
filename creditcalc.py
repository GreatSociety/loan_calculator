"""

Loan Calculator

Settlements are made according to the principle of annuity or differentiated payment.
Argparse module is used to get calculation arguments.

Calculates loan principal or payment or periods and overpayment for annuity.
And calculates every payment with overpayment for differentiated.

Argument:
--type is only can be "diff" or "annuity"
--interest is yours year interest rate
--principal is yours loan principal
--payment is your monthly payment
--periods is number of months of payments

Thus, for any calculation, four out of five arguments must be entered. And everytime --type and --interest.

Example of Calling:
--type=diff --interest=5.2 --principal=1407800 --periods=28
--type=annuity --interest=14.78 --periods=60 --principal=28567510

"""

import math
import argparse
import sys


def interest_rate_nominal(interest):
    """Converts an year rate to a monthly rate"""
    interest_rate = round(interest/(12*100), 10)
    return interest_rate


def periods_calc(payment, principal, interest_rate):
    periods = math.ceil(math.log(payment / (payment - interest_rate * principal), 1 + interest_rate))
    overpayment = (payment * periods) - principal
    return periods, overpayment


def annuity_payment_calc(principal_or_payment, periods, interest_rate, mode):
    constant_calc = ((interest_rate * pow(1 + interest_rate, periods)) / (pow(1 + interest_rate, periods) - 1))
    if mode == 'p':
        principal = math.ceil(principal_or_payment / constant_calc) - 1
        overpayment = math.ceil((principal_or_payment*periods) - principal)
        return principal, overpayment
    elif mode == 'a':
        payment = math.ceil(principal_or_payment * constant_calc)
        overpayment = (payment * periods) - principal_or_payment
        return payment, overpayment
    else:
        return 0


def differentiated_payment(principal, periods, interest_rate):
    m = 1
    overpayment = 0
    while m <= periods:
        diff_pay = math.ceil((principal / periods) + interest_rate * (principal - ((principal * (m - 1))/periods)))
        print(f"Month {m}: payment is {diff_pay}")
        m += 1
        overpayment += diff_pay
    overpayment -= principal
    print(f"\nOverpayment = {overpayment}")
    return 0


def checker_namespace(args_s):
    if len(sys.argv) != 5 or args_s.interest is None:
        return 0
    elif args_s.type != 'diff' and args_s.type != 'annuity':
        return 0
    elif '=-' in ''.join(sys.argv):
        return 0
    elif args_s.type == 'diff' and args_s.payment is not None:
        return 0
    else:
        return 1


parser = argparse.ArgumentParser()
parser.add_argument('-t', '--type', help="You can choice 'diff' or 'annuity' only")
parser.add_argument('-pri', '--principal', type=int)
parser.add_argument('-per', '--periods', type=int)
parser.add_argument('-in', '--interest', type=float)
parser.add_argument('-pay', '--payment', type=int)
args = parser.parse_args()


checker = checker_namespace(args)


if checker == 0:
    print("Incorrect parameters")

elif args.type == 'diff':
    differentiated_payment(args.principal, args.periods, interest_rate_nominal(args.interest))

else:

    if args.periods is None:
        periods_out = periods_calc(args.payment, args.principal, interest_rate_nominal(args.interest))

        if periods_out[0] < 12:
            print(f"It will take {periods_out[0]}"
                  f" months to repay this loan!")
        elif periods_out[0] % 12 == 0:
            print(f"It will take {int(periods_out[0] / 12)} years to repay this loan!")
        else:
            year = int(periods_out[0] / 12)
            month = periods_out[0] - (year * 12)
            print(f"It will take {year} years and {month} months to repay this loan!")
        print(f'Overpayment = {periods_out[1]}')

    elif args.principal is None:
        principal_out = annuity_payment_calc(args.payment, args.periods, interest_rate_nominal(args.interest), 'p')
        print(f'Your loan principal = {principal_out[0]}!\nOverpayment = {principal_out[1]}')
    else:
        payment_out = annuity_payment_calc(args.principal, args.periods, interest_rate_nominal(args.interest), 'a')
        print(f'Your monthly payment = {payment_out[0]}!\nOverpayment = {payment_out[1]}')

