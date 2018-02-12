#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import datetime
from math import ceil


# Check a string is of valid date format
def valid_date(date_string):
    try:
        datetime.datetime.strptime(date_string, '%m%d%Y')
        return True
    except ValueError:
        return False


# Check if a string is of float format
def valid_num(num_string):
    try:
        float(num_string)
        return True
    except ValueError:
        return False


# Check if input record is invalid
def is_invalid(cmte_id, name, zip_code, transaction_dt, transaction_amt,
               other_id):
    if not cmte_id or not name or len(zip_code) < 5:
        return True
    if other_id or not valid_date(transaction_dt) or not valid_num(
            transaction_amt):
        return True


# Output a float into the desired integer, for example: 2.3 -> 2, 3.5 -> 3
def round_up_num(num):
    if num - int(num) >= 0.5:
        return int(num) + 1
    else:
        return int(num)


# Given a list and percentile, output a element following the nearest-rank
# method
def get_percentile(num_list, percentile):
    idx = ceil(len(num_list) * percentile / 100) - 1
    return round_up_num(num_list[idx])


# The main function
def main():
    if len(sys.argv) != 4:
        print('Not correct input arguments!')
        return
    donor_record = dict()
    recipient_record = dict()
    output = []
    percentile = 0
    # Read the file containing the percentile number
    with open(sys.argv[2], 'r') as g:
        for line in g:
            percentile = int(line.strip())

    with open(sys.argv[1], 'r') as f:
        for line in f:
            if not line:
                continue
            s = line.split('|')
            if len(s) < 16:
                continue
            cmte_id = s[0]
            name = s[7]
            zip_code = s[10]
            transaction_dt = s[13]
            transaction_amt = s[14]
            other_id = s[15]
            if is_invalid(cmte_id, name, zip_code, transaction_dt,
                          transaction_amt, other_id):
                continue
            zip_code = zip_code[:5]
            year = transaction_dt[4:]
            donor_id = zip_code + ' ' + name
            recipient_id = cmte_id + ' ' + zip_code + ' ' + year
            if recipient_id not in recipient_record:
                recipient_record[recipient_id] = [float(transaction_amt)]
            else:
                recipient_record[recipient_id].append(float(transaction_amt))
            if donor_id not in donor_record:
                donor_record[donor_id] = (donor_id, year)
            else:
                amount = get_percentile(recipient_record[recipient_id],
                                        percentile)
                total_amount = round_up_num(sum(recipient_record[recipient_id]))
                contribution_number = len(recipient_record[recipient_id])
                output_record = '{}|{}|{}|{}|{}|{}'.format(cmte_id, zip_code,
                                                           year, amount,
                                                           total_amount,
                                                           contribution_number)
                # print(output_record)
                output.append(output_record)
    
    with open(sys.argv[3], 'w') as h:
        for line in output:
            h.write(line+'\n')


if __name__ == '__main__':
    main()
