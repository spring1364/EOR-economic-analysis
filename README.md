# EOR-economic-analysis
## Economic analysis of CO2 storage into oil reservoir
### Prerequisites
You need to install the following packages to be able to execute this code:
```
-Python 3.6
-pandas
-numpy
-matplotlib
-scipy.stat
```

In this project, I have performed the economic analysis of CO2-EOR project. I have the following input yearly data (year 0 to 22):
```
-Oil_Production (bbl/day)
-Gas_Production (MSCF/day)
-Water_Production (bbl/day)
-CO2_Production (MSCF/day)	
-Water_Injection (bbl/day)	
-CO2_Injection (MSCF/day)
```
I have calculated annual cash flow from sales of oil, and gas with CO2 injection and without it. I have also calculated the total NPV and IRR for EOR project. The following charts show the cash flow:
![Figure_1](https://user-images.githubusercontent.com/26604290/65998570-ca12de80-e458-11e9-8087-afefe8002847.png)

In the next section, I have performed a sensitivity analysis to study the impact of oil price change for two CO2 incentive levels on the economic results. The following charts show the obtained results. 
![Figure_2](https://user-images.githubusercontent.com/26604290/65998571-ca12de80-e458-11e9-8c29-c099eca8f5e3.png)

To study the uncertainties, I have performed a Monte Carlo simulation that assumes that oil price and CO2 incentive ($/tonne CO2) follow a uniform probability distribution. The following graph show the obtained NPV distribution for 100,000 monte Carlo runs. You can see that considering credits for CO2 storage will make the project profitable (NPV can go up to 25 $million )
![Figure_3](https://user-images.githubusercontent.com/26604290/65998573-ca12de80-e458-11e9-8ddf-de8b1598d38a.png)
