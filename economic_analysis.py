import numpy as np
import pandas as pd

pd.options.display.max_columns = 20

# Economic model inputs**************************************************
OCF = 0.78
FPF = 1.3
ecs_factor = 0.01
no_HZ_producer = 4
no_HZ_injector = 3
CO2_royalty_factor = 0.05

# Operation costs*******************************************************
oil_op_cost = 10  # $/bbl
gas_op_cost = 0.25  # /Msf
water_op_prod_cost = 1.5  # $/bbk
CO2_op_prod_cost = 0.9  # $/Msf
CO2_op_inj_cost = 4.5  # $/Mcf
water_op_inj_cost = 1.5  # $/bbl
HZ_producer_cost = 27  # M$/well
HZ_injector_cost = 33  # M$/well
other_fixed_cost = 375  # M$
total_well_opCost = 207  # M$
CO2_inj_coversion = 300  # M$

# Royalty costs**************************************************************
royalty_holiday_treatments = 0.05


# Uncertain inputs************************************************************
def set_tax_rate(tax_rate):
    return tax_rate


def set_discount_rate(discount_rate):
    return discount_rate


def set_oil_price(oil_price_range):
    return oil_price_range


def set_gas_price(gas_price_range):
    return gas_price_range


def set_NGL_price(NGL_price_range):
    return NGL_price_range


def set_CO2_incentive(CO2_incentive):
    return CO2_incentive


tax_rate = set_tax_rate(0.25)
discount_rate = set_discount_rate(0.05)
oil_price_range = set_oil_price([60, 95, 120])  # $/bbl
gas_price_range = set_gas_price([1, 3.5, 4])  # $/Mcf
NGL_price_range = set_NGL_price([10, 12, 16])  # $/bbl
CO2_incentive = set_CO2_incentive(10)  # $/tonne CO2

# Commodity prices***********************************************************************
def monthly_prices(base_price, ecs_factor, year_range):
    val = base_price * ((1 + ecs_factor) ** year_range)
    return val

def annual_cash_flow(oil_price_range, tax_rate, discount_rate, CO2_incentive):
    df_inputs = pd.read_csv('CO2_economic.csv', index_col='Year')
    df_inputs.drop('(yr)', axis=0, inplace=True)
    df_inputs.columns = [col.strip() for col in df_inputs.columns]
    year_range = df_inputs.index.values.astype(float)

    df_commodityPrices = pd.DataFrame(index=df_inputs.index)
    val_oil = monthly_prices(oil_price_range[1], ecs_factor, year_range)
    val_gas = monthly_prices(gas_price_range[1], ecs_factor, year_range)
    val_NGL = monthly_prices(NGL_price_range[1], ecs_factor, year_range)

    df_commodityPrices['oil_price'] = np.where(val_oil < oil_price_range[0], oil_price_range[0],
                                               np.where(val_oil > oil_price_range[2], oil_price_range[2], val_oil))
    df_commodityPrices['gas_price'] = np.where(val_gas < gas_price_range[0], gas_price_range[0],
                                               np.where(val_gas > gas_price_range[2], gas_price_range[2], val_gas))
    df_commodityPrices['NGL_price'] = np.where(val_NGL < NGL_price_range[0], NGL_price_range[0],
                                               np.where(val_NGL > NGL_price_range[2], NGL_price_range[2], val_NGL))
    df_salesVolume = pd.DataFrame(index=year_range)
    df_salesVolume['oil_sales'] = df_inputs['Oil_Production'].astype(float) * FPF * OCF * 365
    df_salesVolume['gas_sales'] = df_inputs['Gas_Production'].astype(float) * FPF * OCF * 365
    df_salesVolume['NGL_sales'] = df_salesVolume['gas_sales'] * 0.065

    df_salesRevenue = pd.DataFrame(index=year_range)
    df_salesRevenue['oil_revenue'] = df_salesVolume['oil_sales'] * df_commodityPrices['oil_price'] / 1000
    df_salesRevenue['gas_revenue'] = df_salesVolume['gas_sales'] * df_commodityPrices['gas_price'] / 1000
    df_salesRevenue['NGL_revenue'] = df_salesVolume['NGL_sales'] * df_commodityPrices['NGL_price'] / 1000

    df_opCost = pd.DataFrame(index=df_inputs.index)
    df_opCost['Oil_prod'] = oil_op_cost * df_inputs['Oil_Production'].astype(float) * FPF * OCF * 365 / 1000
    df_opCost['Gas_prod'] = gas_op_cost * df_inputs['Gas_Production'].astype(float) * FPF * OCF * 365 / 1000
    df_opCost['Water_prod'] = water_op_prod_cost * df_inputs['Water_Production'].astype(float) * 365 / 1000
    df_opCost['CO2_prod'] = CO2_op_prod_cost * df_inputs['CO2_Production'].astype(float) * 365 / 1000
    df_opCost['CO2_inj'] = CO2_op_inj_cost * df_inputs['CO2_Injection'].astype(float) * 365 / 1000
    df_opCost['Water_inj'] = water_op_inj_cost * df_inputs['Water_Injection'].astype(float) * 365 / 1000
    df_opCost['Total_cost'] = df_opCost.sum(axis=1) + other_fixed_cost + total_well_opCost
    df_opCost['Unit_op_cost'] = df_opCost['Total_cost'] / (
            df_opCost['Oil_prod'] / oil_op_cost + df_opCost['Gas_prod'] / gas_op_cost / 10)

    capEx = pd.Series(index=df_inputs.index)
    capEx[0] = CO2_inj_coversion * no_HZ_injector
    capEx[1:] = 0

    df_cashFlow = pd.DataFrame(index=df_inputs.index)
    df_cashFlow['Sales'] = df_salesRevenue.sum(axis=1) * (1 - royalty_holiday_treatments) - df_opCost['Total_cost']
    df_cashFlow['Discounted'] = df_cashFlow['Sales'] / (1 + discount_rate) ** year_range
    df_cashFlow['Net'] = np.where(df_cashFlow['Sales'] - capEx < 0,
                                  df_cashFlow['Sales'] - capEx,
                                  (df_cashFlow['Sales'] - capEx) * (1 - tax_rate))

    df_cashFlow['Cumulative'] = df_cashFlow['Net'].cumsum()

    df_CO2 = pd.DataFrame(index=year_range)
    df_CO2['Stored_mass'] = 365 * (
            df_inputs['CO2_Injection'].astype(float).cumsum() - df_inputs['CO2_Production'].astype(
        float).cumsum()) / (1000 * 17.4)
    df_CO2['Cash_flow'] = np.where(
        df_cashFlow['Sales'] - capEx + (df_CO2['Stored_mass'] * CO2_incentive) < 0,
        df_cashFlow['Sales'] - capEx + (df_CO2['Stored_mass'] * CO2_incentive),
        (df_cashFlow['Sales'] - capEx + (df_CO2['Stored_mass'] * CO2_incentive)) * (1 - tax_rate))
    df_CO2['RC_incentive'] = CO2_royalty_factor - (df_CO2['Stored_mass'] / 10000)
    df_CO2['RC_incentive_sales_CF'] = df_salesRevenue.sum(axis=1) * (1 - df_CO2['RC_incentive']) - \
                                      df_opCost['Total_cost']
    df_CO2['RC_incentive_net_CF'] = np.where(df_CO2['RC_incentive_sales_CF'] - capEx < 0,
                                             df_CO2['RC_incentive_sales_CF'] - capEx,
                                             (df_CO2['RC_incentive_sales_CF'] - capEx) * (1 - tax_rate))
    df_cashFlow['with_CO2'] = df_CO2['Cash_flow']
    df_cashFlow['with_CO2_RC'] = df_CO2['RC_incentive_net_CF']
    return df_cashFlow


def economic_summary(df_cashFlow):
    NPV = np.npv(discount_rate, df_cashFlow['Net']) / 1000
    NPV_CO2_storage = np.npv(discount_rate, df_cashFlow['with_CO2']) / 1000
    NPV_CO2_storage_RC = np.npv(discount_rate, df_cashFlow['with_CO2_RC']) / 1000
    IRR = np.irr(df_cashFlow['Net'])
    return [NPV, NPV_CO2_storage, NPV_CO2_storage_RC, IRR]


if __name__ == '__main__':
    ES = economic_summary(annual_cash_flow(oil_price_range, tax_rate, discount_rate, CO2_incentive))
    print('NPV: {0:3.2f}'.format(ES[0]))
    print('NPV with CO2 storage: {0:3.2f}'.format(ES[1]))
    print('NPV with RC incentivized CO2 storage: {0:3.2f}'.format(ES[2]))