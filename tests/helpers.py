###############################################################################
# Copyright (C) 2018, 2019, 2020 Dominic O'Kane
###############################################################################

from financepy.utils.global_types import SwapTypes
from financepy.utils.date import Date
from financepy.utils.day_count import DayCountTypes
from financepy.utils.frequency import FrequencyTypes
from financepy.products.credit.cds_curve import CDSCurve
from financepy.products.rates.ibor_single_curve import IborSingleCurve
from financepy.products.rates.ibor_swap import IborSwap
from financepy.products.rates.ibor_deposit import IborDeposit
from financepy.products.credit.cds import CDS

from os.path import dirname, join


def build_Ibor_Curve(tradeDate):

    valuation_date = tradeDate.add_days(1)
    dcType = DayCountTypes.ACT_360

    depos = []
    fras = []
    swaps = []

    dcType = DayCountTypes.THIRTY_E_360_ISDA
    fixedFreq = FrequencyTypes.SEMI_ANNUAL
    settlement_date = valuation_date

    maturity_date = settlement_date.add_months(12)
    swap1 = IborSwap(
        settlement_date,
        maturity_date,
        SwapTypes.PAY,
        0.0502,
        fixedFreq,
        dcType)
    swaps.append(swap1)

    maturity_date = settlement_date.add_months(24)
    swap2 = IborSwap(
        settlement_date,
        maturity_date,
        SwapTypes.PAY,
        0.0502,
        fixedFreq,
        dcType)
    swaps.append(swap2)

    maturity_date = settlement_date.add_months(36)
    swap3 = IborSwap(
        settlement_date,
        maturity_date,
        SwapTypes.PAY,
        0.0501,
        fixedFreq,
        dcType)
    swaps.append(swap3)

    maturity_date = settlement_date.add_months(48)
    swap4 = IborSwap(
        settlement_date,
        maturity_date,
        SwapTypes.PAY,
        0.0502,
        fixedFreq,
        dcType)
    swaps.append(swap4)

    maturity_date = settlement_date.add_months(60)
    swap5 = IborSwap(
        settlement_date,
        maturity_date,
        SwapTypes.PAY,
        0.0501,
        fixedFreq,
        dcType)
    swaps.append(swap5)

    libor_curve = IborSingleCurve(valuation_date, depos, fras, swaps)

    return libor_curve


def buildIssuerCurve(tradeDate, libor_curve):

    valuation_date = tradeDate.add_days(1)

    cdsMarketContracts = []

    cdsCoupon = 0.0048375
    maturity_date = Date(29, 6, 2010)
    cds = CDS(valuation_date, maturity_date, cdsCoupon)
    cdsMarketContracts.append(cds)

    recovery_rate = 0.40

    issuer_curve = CDSCurve(valuation_date,
                            cdsMarketContracts,
                            libor_curve,
                            recovery_rate)

    return issuer_curve


def buildFlatIssuerCurve(tradeDate, libor_curve, spread, recovery_rate):

    valuation_date = tradeDate.add_days(1)

    cdsMarketContracts = []

    maturity_date = Date(29, 6, 2010)
    cds = CDS(valuation_date, maturity_date, spread)
    cdsMarketContracts.append(cds)

    issuer_curve = CDSCurve(valuation_date,
                            cdsMarketContracts,
                            libor_curve,
                            recovery_rate)

    return issuer_curve


def buildFullIssuerCurve(valuation_date):

    dcType = DayCountTypes.ACT_360
    depos = []
    irBump = 0.0

    m = 1.0  # 0.00000000000

    spot_days = 0
    settlement_date = valuation_date.add_days(spot_days)

    maturity_date = settlement_date.add_months(1)
    depo1 = IborDeposit(settlement_date, maturity_date, m * 0.0016, dcType)

    maturity_date = settlement_date.add_months(2)
    depo2 = IborDeposit(settlement_date, maturity_date, m * 0.0020, dcType)

    maturity_date = settlement_date.add_months(3)
    depo3 = IborDeposit(settlement_date, maturity_date, m * 0.0024, dcType)

    maturity_date = settlement_date.add_months(6)
    depo4 = IborDeposit(settlement_date, maturity_date, m * 0.0033, dcType)

    maturity_date = settlement_date.add_months(12)
    depo5 = IborDeposit(settlement_date, maturity_date, m * 0.0056, dcType)

    depos.append(depo1)
    depos.append(depo2)
    depos.append(depo3)
    depos.append(depo4)
    depos.append(depo5)

    fras = []

    spot_days = 2
    settlement_date = valuation_date.add_days(spot_days)

    swaps = []
    dcType = DayCountTypes.THIRTY_E_360_ISDA
    fixedFreq = FrequencyTypes.SEMI_ANNUAL

    maturity_date = settlement_date.add_months(24)
    swap1 = IborSwap(
        settlement_date,
        maturity_date,
        SwapTypes.PAY,
        m * 0.0044 + irBump,
        fixedFreq,
        dcType)
    swaps.append(swap1)

    maturity_date = settlement_date.add_months(36)
    swap2 = IborSwap(
        settlement_date,
        maturity_date,
        SwapTypes.PAY,
        m * 0.0078 + irBump,
        fixedFreq,
        dcType)
    swaps.append(swap2)

    maturity_date = settlement_date.add_months(48)
    swap3 = IborSwap(
        settlement_date,
        maturity_date,
        SwapTypes.PAY,
        m * 0.0119 + irBump,
        fixedFreq,
        dcType)
    swaps.append(swap3)

    maturity_date = settlement_date.add_months(60)
    swap4 = IborSwap(
        settlement_date,
        maturity_date,
        SwapTypes.PAY,
        m * 0.0158 + irBump,
        fixedFreq,
        dcType)
    swaps.append(swap4)

    maturity_date = settlement_date.add_months(72)
    swap5 = IborSwap(
        settlement_date,
        maturity_date,
        SwapTypes.PAY,
        m * 0.0192 + irBump,
        fixedFreq,
        dcType)
    swaps.append(swap5)

    maturity_date = settlement_date.add_months(84)
    swap6 = IborSwap(
        settlement_date,
        maturity_date,
        SwapTypes.PAY,
        m * 0.0219 + irBump,
        fixedFreq,
        dcType)
    swaps.append(swap6)

    maturity_date = settlement_date.add_months(96)
    swap7 = IborSwap(
        settlement_date,
        maturity_date,
        SwapTypes.PAY,
        m * 0.0242 + irBump,
        fixedFreq,
        dcType)
    swaps.append(swap7)

    maturity_date = settlement_date.add_months(108)
    swap8 = IborSwap(
        settlement_date,
        maturity_date,
        SwapTypes.PAY,
        m * 0.0261 + irBump,
        fixedFreq,
        dcType)
    swaps.append(swap8)

    maturity_date = settlement_date.add_months(120)
    swap9 = IborSwap(
        settlement_date,
        maturity_date,
        SwapTypes.PAY,
        m * 0.0276 + irBump,
        fixedFreq,
        dcType)
    swaps.append(swap9)

    libor_curve = IborSingleCurve(valuation_date, depos, fras, swaps)

    cdsMarketContracts = []
    cdsCoupon = 0.005743
    maturity_date = valuation_date.next_cds_date(6)
    cds = CDS(valuation_date, maturity_date, cdsCoupon)
    cdsMarketContracts.append(cds)

    cdsCoupon = 0.007497
    maturity_date = valuation_date.next_cds_date(12)
    cds = CDS(valuation_date, maturity_date, cdsCoupon)
    cdsMarketContracts.append(cds)

    cdsCoupon = 0.011132
    maturity_date = valuation_date.next_cds_date(24)
    cds = CDS(valuation_date, maturity_date, cdsCoupon)
    cdsMarketContracts.append(cds)

    cdsCoupon = 0.013932
    maturity_date = valuation_date.next_cds_date(36)
    cds = CDS(valuation_date, maturity_date, cdsCoupon)
    cdsMarketContracts.append(cds)

    cdsCoupon = 0.015764
    maturity_date = valuation_date.next_cds_date(48)
    cds = CDS(valuation_date, maturity_date, cdsCoupon)
    cdsMarketContracts.append(cds)

    cdsCoupon = 0.017366
    maturity_date = valuation_date.next_cds_date(60)
    cds = CDS(valuation_date, maturity_date, cdsCoupon)
    cdsMarketContracts.append(cds)

    cdsCoupon = 0.020928
    maturity_date = valuation_date.next_cds_date(84)
    cds = CDS(valuation_date, maturity_date, cdsCoupon)
    cdsMarketContracts.append(cds)

    cdsCoupon = 0.022835
    maturity_date = valuation_date.next_cds_date(120)
    cds = CDS(valuation_date, maturity_date, cdsCoupon)
    cdsMarketContracts.append(cds)

    recovery_rate = 0.40

    issuer_curve = CDSCurve(valuation_date,
                            cdsMarketContracts,
                            libor_curve,
                            recovery_rate)

    return libor_curve, issuer_curve


def loadHomogeneousSpreadCurves(valuation_date,
                                libor_curve,
                                cdsSpread3Y,
                                cdsSpread5Y,
                                cdsSpread7Y,
                                cdsSpread10Y,
                                num_credits):

    maturity3Y = valuation_date.next_cds_date(36)
    maturity5Y = valuation_date.next_cds_date(60)
    maturity7Y = valuation_date.next_cds_date(84)
    maturity10Y = valuation_date.next_cds_date(120)

    recovery_rate = 0.40

    cds3Y = CDS(valuation_date, maturity3Y, cdsSpread3Y)
    cds5Y = CDS(valuation_date, maturity5Y, cdsSpread5Y)
    cds7Y = CDS(valuation_date, maturity7Y, cdsSpread7Y)
    cds10Y = CDS(valuation_date, maturity10Y, cdsSpread10Y)

    contracts = [cds3Y, cds5Y, cds7Y, cds10Y]

    issuer_curve = CDSCurve(valuation_date,
                            contracts,
                            libor_curve,
                            recovery_rate)

    issuer_curves = []
    for _ in range(0, num_credits):
        issuer_curves.append(issuer_curve)

    return issuer_curves


def loadHeterogeneousSpreadCurves(valuation_date, libor_curve):

    maturity3Y = valuation_date.next_cds_date(36)
    maturity5Y = valuation_date.next_cds_date(60)
    maturity7Y = valuation_date.next_cds_date(84)
    maturity10Y = valuation_date.next_cds_date(120)

    path = dirname(__file__)
    filename = "CDX_NA_IG_S7_SPREADS.csv"
    full_filename_path = join(path, "data", filename)
    f = open(full_filename_path, 'r')

    data = f.readlines()
    issuer_curves = []

    for row in data[1:]:

        splitRow = row.split(",")
        spd3Y = float(splitRow[1]) / 10000.0
        spd5Y = float(splitRow[2]) / 10000.0
        spd7Y = float(splitRow[3]) / 10000.0
        spd10Y = float(splitRow[4]) / 10000.0
        recovery_rate = float(splitRow[5])

        cds3Y = CDS(valuation_date, maturity3Y, spd3Y)
        cds5Y = CDS(valuation_date, maturity5Y, spd5Y)
        cds7Y = CDS(valuation_date, maturity7Y, spd7Y)
        cds10Y = CDS(valuation_date, maturity10Y, spd10Y)
        cds_contracts = [cds3Y, cds5Y, cds7Y, cds10Y]

        issuer_curve = CDSCurve(valuation_date,
                                cds_contracts,
                                libor_curve,
                                recovery_rate)

        issuer_curves.append(issuer_curve)

    return issuer_curves
