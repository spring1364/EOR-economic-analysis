import economic_analysis
import numpy as np


class MonteCarlo:
    def __init__(self, oil_price_range, CO2_incentive_range):
        # self.discount_rate_range = discount_rate_range
        # self.tax_rate_range = tax_rate_range
        self.oil_price_range = oil_price_range
        self.CO2_incentive_range = CO2_incentive_range

    def set_random_parameter(self):
        oil_price = economic_analysis.set_gas_price(np.random.uniform(self.oil_price_range[0], self.oil_price_range[1]))
        CO2_incentive = economic_analysis.set_CO2_incentive(
            np.random.uniform(self.CO2_incentive_range[0], self.CO2_incentive_range[1]))
        return oil_price, CO2_incentive

    def find_NPV(self):
        oil_price_range = [self.oil_price_range[0], self.set_random_parameter()[0], self.oil_price_range[1]]
        CO2_incentive = self.set_random_parameter()[1]

        NPVs = economic_analysis.economic_summary(
            economic_analysis.annual_cash_flow(oil_price_range, 0.25, 0.05, CO2_incentive))
        return NPVs[0], NPVs[1], NPVs[2]




