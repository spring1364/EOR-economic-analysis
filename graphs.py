import economic_analysis
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter
import Sensitivity_analysis
from Monte_Carlo import MonteCarlo
from scipy.stats import norm
import matplotlib.mlab as mlab
from matplotlib.ticker import FormatStrFormatter


tax_rate = 0.25
discount_rate = 0.05
oil_price_range = [60, 95, 120]  # $/bbl
gas_price_range = [1, 3.5, 4]  # $/Mcf
NGL_price_range = [10, 12, 16]  # $/bbl
CO2_incentive = 10  # $/tonne CO2
df_cashFlow = economic_analysis.annual_cash_flow(oil_price_range, tax_rate, discount_rate, CO2_incentive)
years = df_cashFlow.index.values


def millions(x, pos):
    return '$%1.0fM' % (x * 1e-3)


formatter = FuncFormatter(millions)
fig = plt.figure(figsize=(10, 6))
ax1 = fig.add_subplot(2, 2, 1)
ax2 = fig.add_subplot(2, 2, 2)
ax3 = fig.add_subplot(2, 2, 3)
# ax4 = fig.add_subplot(2, 2, 4)

ax1.bar(years, df_cashFlow['Net'])
ax2.bar(years, df_cashFlow['Cumulative'])
ax3.bar(years, df_cashFlow['with_CO2'])
 # ax4.bar(years, df_cashFlow['with_CO2_RC'])

ax1.yaxis.set_major_formatter(formatter)
ax2.yaxis.set_major_formatter(formatter)
ax3.yaxis.set_major_formatter(formatter)
# ax4.yaxis.set_major_formatter(formatter)
ax1.set_xlabel('Year')
ax2.set_xlabel('Year')
ax3.set_xlabel('Year')
 # ax4.set_xlabel('Year')
ax1.set_ylabel('Cash flow')
ax2.set_ylabel('Cash flow')
ax3.set_ylabel('Cash flow')
 # ax4.set_ylabel('Cash flow')
ax1.set_xticks(np.arange(0, 24, 2))
ax2.set_xticks(np.arange(0, 24, 2))
ax3.set_xticks(np.arange(0, 24, 2))
 # ax4.set_xticks(np.arange(0, 24, 2))
ax1.set_title('Net cash flow')
ax2.set_title('Cumulative cash flow')
ax3.set_title('With CO2 storage credit')
 # ax4.set_title('With CO2 storage royalty incentives')
plt.subplots_adjust(wspace=0.4, hspace=0.4)

plt.show()
 # ****************************************************************************************
low_oil_price = 20
high_oil_price = 50
oil_price_sensitivity_low_incentive = Sensitivity_analysis.find_oil_price_sensitivity(low_oil_price, high_oil_price, 20)
oil_price_sensitivity_high_incentive = Sensitivity_analysis.find_oil_price_sensitivity(low_oil_price, high_oil_price,
                                                                                    30)
fig2 = plt.figure(figsize=(10, 5))
ax1 = fig2.add_subplot(1, 2, 1)
ax2 = fig2.add_subplot(1, 2, 2)
ax1.bar(np.arange(low_oil_price, high_oil_price), oil_price_sensitivity_low_incentive)
ax1.set_xlabel('Average oil price $/bbl')
ax1.set_ylabel('NPV with CO2 storage, MM$')
ax2.bar(np.arange(low_oil_price, high_oil_price), oil_price_sensitivity_high_incentive)
ax2.set_xlabel('Average oil price $/bbl')
ax2.set_ylabel('NPV with CO2 storage credit, MM$')
ax1.set_title('CO2 incentive: $20/tonne CO2')
ax2.set_title('CO2 incentive: $30/tonne CO2')
plt.show()

# Monte Carlo Simulation*************************************************************************************
CO2_incentive_range = [10, 30]
oil_price_range = [20, 90]
noRuns = 1000
NPV = []
NPV_with_storage = []
NPV_with_storage_RC = []

for i in range(noRuns):
    monte_obj = MonteCarlo(oil_price_range, CO2_incentive_range).find_NPV()
    NPV.append(monte_obj[0])
    NPV_with_storage.append(monte_obj[1])
    NPV_with_storage_RC.append(monte_obj[2])

(mu, sigma) = norm.fit(NPV_with_storage)

n1, bins1, p1 = plt.hist(NPV, 10, density=True, facecolor='g', alpha=0.5, label='Without CO2 storage credit')
n2, bins2, p2 = plt.hist(NPV_with_storage, 10, facecolor='b', alpha=0.5, label='With CO2 storage credit')
n, bins, p3 = plt.hist(NPV_with_storage_RC, 20, density=True, facecolor='r', alpha=0.5, label='With CO2 storage-RC incentivized')
y = mlab.normpdf(bins2, mu, sigma)
l = plt.plot(bins2, y, 'r--', linewidth=2)
print(mu, sigma)
print(y)
plt.setp(p1, edgecolor='k')
plt.setp(p2, edgecolor='k')
plt.setp(p3, edgecolor='k')

plt.xlabel('NPV, $MM')
plt.ylabel('Probability')
plt.legend(loc='upper right')
plt.show()
