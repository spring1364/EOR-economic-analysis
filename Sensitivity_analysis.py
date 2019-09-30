import economic_analysis

oil_price_range = [20, 40, 60]

def find_CO2_incentive_sensitivity(low, high):
    CO2_incentive_sensitivity = []
    for CO2_incentive in range(low, high):
        ES = economic_analysis.economic_summary(
            economic_analysis.annual_cash_flow(oil_price_range=oil_price_range, tax_rate=0.25, discount_rate=0.05,
                                               CO2_incentive=CO2_incentive))
        CO2_incentive_sensitivity.append(ES[1])
    return CO2_incentive_sensitivity


def find_oil_price_sensitivity(low_price, high_price, CO2_incentive):
    oil_price_sensitivity = []
    for oil_price in range(low_price, high_price):
        oil_price_range = [low_price, oil_price, high_price]
        ES = economic_analysis.economic_summary(
            economic_analysis.annual_cash_flow(oil_price_range=oil_price_range, tax_rate=0.25, discount_rate=0.05,
                                               CO2_incentive=CO2_incentive))
        oil_price_sensitivity.append(ES[1])
    return oil_price_sensitivity
