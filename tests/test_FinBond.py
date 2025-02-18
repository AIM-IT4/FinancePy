##############################################################################
# Copyright (C) 2018, 2019, 2020 Dominic O'Kane
##############################################################################

import numpy as np
from financepy.products.bonds.bond import YTMCalcType, Bond
from financepy.products.bonds.bond_zero import BondZero
from financepy.products.bonds.bond_market import *
from financepy.utils.math import ONE_MILLION
from financepy.utils.date import Date
from financepy.utils.day_count import DayCountTypes
from financepy.utils.frequency import FrequencyTypes
import pandas as pd
import sys
sys.path.append("..")


def test_bondtutor_example():
    #  EXAMPLE FROM http://bondtutor.com/btchp4/topic6/topic6.htm

    accrualConvention = DayCountTypes.ACT_ACT_ICMA
    y = 0.062267
    settlement_date = Date(19, 4, 1994)
    issue_date = Date(15, 7, 1990)
    maturity_date = Date(15, 7, 1997)
    coupon = 0.085
    face = ONE_MILLION
    freq_type = FrequencyTypes.SEMI_ANNUAL
    bond = Bond(issue_date, maturity_date,
                coupon, freq_type, accrualConvention, face)

    full_price = bond.full_price_from_ytm(settlement_date, y)
    assert round(full_price, 4) == 108.7696
    clean_price = bond.clean_price_from_ytm(settlement_date, y)
    assert round(clean_price, 4) == 106.5625
    accrued_interest = bond._accrued_interest
    assert round(accrued_interest, 4) == 22071.8232
    ytm = bond.yield_to_maturity(settlement_date, clean_price)
    assert round(ytm, 4) == 0.0622

    bump = 1e-4
    priceBumpedUp = bond.full_price_from_ytm(settlement_date, y + bump)
    assert round(priceBumpedUp, 4) == 108.7395

    priceBumpedDn = bond.full_price_from_ytm(settlement_date, y - bump)
    assert round(priceBumpedDn, 4) == 108.7998

    durationByBump = -(priceBumpedUp - full_price) / bump
    assert round(durationByBump, 4) == 301.1932

    duration = bond.dollar_duration(settlement_date, y)
    assert round(duration, 4) == 301.2458
    assert round(duration - durationByBump, 4) == 0.0526

    modified_duration = bond.modified_duration(settlement_date, y)
    assert round(modified_duration, 4) == 2.7696

    macauley_duration = bond.macauley_duration(settlement_date, y)
    assert round(macauley_duration, 4) == 2.8558

    conv = bond.convexity_from_ytm(settlement_date, y)
    assert round(conv, 4) == 0.0967


def test_bloomberg_us_treasury_example():
    # https://data.bloomberglp.com/bat/sites/3/2017/07/SF-2017_Paul-Fjeldsted.pdf

    settlement_date = Date(21, 7, 2017)
    issue_date = Date(15, 5, 2010)
    maturity_date = Date(15, 5, 2027)
    coupon = 0.02375
    freq_type = FrequencyTypes.SEMI_ANNUAL
    accrual_type = DayCountTypes.ACT_ACT_ICMA
    face = 100.0

    bond = Bond(issue_date,
                maturity_date,
                coupon,
                freq_type,
                accrual_type,
                face)

    clean_price = 99.7808417

    yld = bond.current_yield(clean_price)
    assert round(yld, 4) == 0.0238

    ytm = bond.yield_to_maturity(settlement_date, clean_price,
                                 YTMCalcType.UK_DMO)
    assert round(ytm, 4) == 0.0240

    ytm = bond.yield_to_maturity(settlement_date, clean_price,
                                 YTMCalcType.US_STREET)
    assert round(ytm, 4) == 0.0240

    ytm = bond.yield_to_maturity(settlement_date, clean_price,
                                 YTMCalcType.US_TREASURY)
    assert round(ytm, 4) == 0.0240

    full_price = bond.full_price_from_ytm(settlement_date, ytm)
    assert round(full_price, 4) == 100.2149

    clean_price = bond.clean_price_from_ytm(settlement_date, ytm)
    assert round(clean_price, 4) == 99.7825

    accrued_interest = bond._accrued_interest
    assert round(accrued_interest, 4) == 0.4324

    accddays = bond._accrued_days
    assert round(accddays, 4) == 67.0

    duration = bond.dollar_duration(settlement_date, ytm)
    assert round(duration, 4) == 869.0934

    modified_duration = bond.modified_duration(settlement_date, ytm)
    assert round(modified_duration, 4) == 8.6723

    macauley_duration = bond.macauley_duration(settlement_date, ytm)
    assert round(macauley_duration, 4) == 8.7764

    conv = bond.convexity_from_ytm(settlement_date, ytm)
    assert round(conv, 4) == 0.8517


def test_bloomberg_apple_corp_example():
    settlement_date = Date(21, 7, 2017)
    issue_date = Date(13, 5, 2012)
    maturity_date = Date(13, 5, 2022)
    coupon = 0.027
    freq_type = FrequencyTypes.SEMI_ANNUAL
    accrual_type = DayCountTypes.THIRTY_E_360_ISDA
    face = 100.0

    bond = Bond(issue_date, maturity_date,
                coupon, freq_type, accrual_type, face)

    clean_price = 101.581564

    yld = bond.current_yield(clean_price)
    assert round(yld, 4) == 0.0266

    ytm = bond.yield_to_maturity(settlement_date, clean_price,
                                 YTMCalcType.UK_DMO)
    assert round(ytm, 4) == 0.0235

    ytm = bond.yield_to_maturity(settlement_date, clean_price,
                                 YTMCalcType.US_STREET)
    assert round(ytm, 4) == 0.0235

    ytm = bond.yield_to_maturity(settlement_date, clean_price,
                                 YTMCalcType.US_TREASURY)
    assert round(ytm, 4) == 0.0235

    full_price = bond.full_price_from_ytm(settlement_date, ytm)
    assert round(full_price, 4) == 102.0932

    clean_price = bond.clean_price_from_ytm(settlement_date, ytm)
    assert round(clean_price, 4) == 101.5832

    accddays = bond._accrued_days
    assert accddays == 68

    accrued_interest = bond._accrued_interest
    assert round(accrued_interest, 4) == 0.51

    duration = bond.dollar_duration(settlement_date, ytm)
    assert round(duration, 4) == 456.5778

    modified_duration = bond.modified_duration(settlement_date, ytm)
    assert round(modified_duration, 4) == 4.4722

    macauley_duration = bond.macauley_duration(settlement_date, ytm)
    assert round(macauley_duration, 4) == 4.5247

    conv = bond.convexity_from_ytm(settlement_date, ytm)
    assert round(conv, 4) == 0.2302


def test_zero_bond():
    # A 3 months treasure with 0 coupon per year.
    bill = BondZero(
        issue_date=Date(25, 7, 2022),
        maturity_date=Date(24, 10, 2022),
        face_amount=ONE_MILLION,
        issue_price=99.6410
    )
    settlement_date = Date(8, 8, 2022)

    clean_price = 99.6504
    calc_ytm = bill.yield_to_maturity(
        settlement_date, clean_price, YTMCalcType.ZERO) * 100
    accrued_interest = bill.calc_accrued_interest(settlement_date)
    assert abs(calc_ytm - 1.3997) < 0.0002
    assert abs(accrued_interest - ONE_MILLION * 0.055231 / 100) < 0.01


def test_bond_ror():
    test_case_file = 'test_cases_bond_ror.csv'
    df = pd.read_csv('./tests/data/' + test_case_file,
                     parse_dates=['buy_date', 'sell_date'])
    # A 10-year bond with 1 coupon per year. code: 210215
    bond = Bond(
        issue_date=Date(13, 9, 2021),
        maturity_date=Date(13, 9, 2031),
        coupon=0.0312,
        freq_type=FrequencyTypes.ANNUAL,
        accrual_type=DayCountTypes.ACT_ACT_ICMA
    )
    for row in df.itertuples(index=False):
        buy_date = Date(row.buy_date.day, row.buy_date.month,
                        row.buy_date.year)
        sell_date = Date(row.sell_date.day,
                         row.sell_date.month, row.sell_date.year)
        simple, irr, pnl = bond.calc_ror(
            buy_date, sell_date, row.buy_ytm, row.sell_ytm)
        assert abs(simple - row.simple_return) < 0.00001
        assert abs(irr - row.irr) < 0.00001


def test_bond_zero_ror():
    test_case_file = 'test_cases_bond_zero_ror.csv'
    df = pd.read_csv('./tests/data/' + test_case_file,
                     parse_dates=['buy_date', 'sell_date'])
    # A 1-year bond with zero coupon per year. code: 092103011
    bond = BondZero(
        issue_date=Date(23, 7, 2021),
        maturity_date=Date(24, 8, 2022),
        issue_price=97.67
    )
    for row in df.itertuples(index=False):
        buy_date = Date(row.buy_date.day, row.buy_date.month,
                        row.buy_date.year)
        sell_date = Date(row.sell_date.day,
                         row.sell_date.month, row.sell_date.year)
        simple, irr, pnl = bond.calc_ror(
            buy_date, sell_date, row.buy_ytm, row.sell_ytm)
        assert abs(simple - row.simple_return) < 0.00001
        assert abs(irr - row.irr) < 0.00001


def test_bond_cfets():
    """
    Test ytms of bonds in CFETS convention, especially for those in last coupon period and
    have 2 or more coupon payments per year.
    """
    test_case_file = 'test_cases_bond_cfets.csv'
    df = pd.read_csv('./tests/data/' + test_case_file,
                     parse_dates=['settlement_date', 'issue_date', 'maturity_date'])
    for row in df.itertuples(index=False):
        bond = Bond(
            issue_date=Date(row.issue_date.day,
                            row.issue_date.month, row.issue_date.year),
            maturity_date=Date(row.maturity_date.day,
                               row.maturity_date.month, row.maturity_date.year),
            coupon=row.coupon / 100,
            freq_type=FrequencyTypes.ANNUAL if row.freq == 1 else FrequencyTypes.SEMI_ANNUAL,
            accrual_type=DayCountTypes.ACT_ACT_ICMA
        )
        settlement_date = Date(
            row.settlement_date.day, row.settlement_date.month, row.settlement_date.year)
        accrued_interest = bond.calc_accrued_interest(settlement_date)
        clean_price = row.full_price - accrued_interest
        calc_ytm = bond.yield_to_maturity(
            settlement_date, clean_price, YTMCalcType.CFETS) * 100
        try:
            assert abs(calc_ytm - row.ytm) < 0.0001
        except:
            print(bond)
            print(clean_price)
            print(settlement_date)
            print(bond.coupon_dates(settlement_date))
            print(f'calc_ytm:{calc_ytm}, correct_ytm:{row.ytm}')
            continue


def test_key_rate_durations():
    settlement_date = Date(21, 7, 2017)
    issue_date = Date(13, 5, 2012)
    maturity_date = Date(13, 5, 2022)
    coupon = 0.027
    freq_type = FrequencyTypes.SEMI_ANNUAL
    accrual_type = DayCountTypes.THIRTY_E_360_ISDA
    face = 100.0
    bond = Bond(issue_date, maturity_date, coupon,
                freq_type, accrual_type, face)

    yld = coupon

    key_rate_tenors, key_rate_durations = bond.key_rate_durations(
        settlement_date, yld)

    assert (key_rate_tenors == np.array(
        [0.25, 0.5, 1, 2, 3, 4, 5, 7, 8, 9, 10, 20, 30])).all()

    # The following test cases are rounded to 6 decimal places
    test_case_krds = [0.00308, 0.005003, 0.022352, 0.050164, 0.073384, 
                      0.890714, 3.414422, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

    for i in range(len(key_rate_durations)):
        assert round(key_rate_durations[i], 6) == test_case_krds[i]


def test_key_rate_durations_Bloomberg_example():
    accrual_type, frequencyType, settlementDays, exDiv, calendar = \
    get_bond_market_conventions(BondMarkets.UNITED_STATES)

    # interest accrues on this date. Issue date is 01/08/2022
    issue_date = Date(31, 7, 2022)
    maturity_date = Date(31, 7, 2027)
    cpn = 2.75/100
    bond = Bond(issue_date, maturity_date, cpn, frequencyType, accrual_type)

    # US Government Equivalent yield on Bloomberg as of 17 March 2023
    ytm = 3.803140/100

    settlement_date = Date(20, 3, 2023)  # next settle date for this bond
    key_rate_tenors, key_rate_durations = bond.key_rate_durations(
        settlement_date, ytm)

    assert (key_rate_tenors == np.array(
        [0.25, 0.5, 1, 2, 3, 4, 5, 7, 8, 9, 10, 20, 30])).all()

    # The following test cases are rounded to 6 decimal places
    test_case_krds = [0.002773, 0.005383, 0.023423, 0.051905, 0.075023, 2.502754, 
                      1.379869, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

    for i in range(len(key_rate_durations)):
        assert round(key_rate_durations[i], 6) == test_case_krds[i]
