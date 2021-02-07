#!/usr/bin/env python

import struct

def fp_to_decimal(binary_input, exponent_bits, mantissa_bits, num_fractional_digits, show_trailing_zeroes = False, truncate = False):
	sign     = (binary_input & (1 << (exponent_bits + mantissa_bits))) >> (exponent_bits + mantissa_bits)
	exponent = (binary_input & (((1 << exponent_bits) - 1) << mantissa_bits)) >> mantissa_bits
	mantissa =  binary_input & ((1 << mantissa_bits) - 1)
	if exponent != 0:
		mantissa = mantissa + (1 << mantissa_bits)
	if sign == 1: mantissa = -mantissa
	return fraction_to_decimal(mantissa * (1 << exponent) , 1 << ((1 << (exponent_bits - 1)) + mantissa_bits - 1), num_fractional_digits, show_trailing_zeroes, truncate)

def double_to_decimal(input, num_fractional_digits, show_trailing_zeroes = False, truncate = False):
	binary_input = struct.unpack('Q', struct.pack('d', input))[0]
	return fp_to_decimal(binary_input, 11, 52, num_fractional_digits, show_trailing_zeroes, truncate)

def float_to_decimal(input, num_fractional_digits, show_trailing_zeroes = False, truncate = False):
	binary_input = struct.unpack('I', struct.pack('f', input))[0]
	return fp_to_decimal(binary_input, 8, 23, num_fractional_digits, show_trailing_zeroes, truncate)

def fraction_to_decimal(numerator, denumerator, num_fractional_digits, show_trailing_zeroes = False, truncate = False):
	sign = ''
	if numerator < 0:
		sign = '-'
		numerator = -numerator
	if not(truncate):
		numerator, denumerator = numerator * 2 + denumerator, denumerator * 2
	floor = numerator // denumerator
	if num_fractional_digits == 0: return floor
	numerator = numerator - floor * denumerator
	if (numerator == 0 and not(show_trailing_zeroes)): return floor
	fractional_digits = fractional_digits_from_proper_fraction(numerator, denumerator, num_fractional_digits, show_trailing_zeroes, truncate)
	return sign + str(floor) + '.' + fractional_digits

def fractional_digits_from_proper_fraction(numerator, denumerator, digits, show_trailing_zeroes, truncate):
	if digits == 0 or (not(show_trailing_zeroes) and numerator == 0): return ''
	if digits == 1 and not(truncate): numerator, denumerator = add_fraction
	numerator *= 10
	digit = numerator // denumerator
	rest_numerator = numerator - digit * denumerator
	return str(digit) + fractional_digits_from_proper_fraction(rest_numerator, denumerator, digits - 1, show_trailing_zeroes, truncate)
