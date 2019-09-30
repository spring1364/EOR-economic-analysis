import pandas as pd
import numpy as np


def convert_ysftomsf_pct(ysf_percentage):
    msf_percentage = 100 * ((1.0 + ysf_percentage / 100) ** (1.0 / 12) - 1.0)
    return msf_percentage


def get_monthly_escalated_prices(base_price, price_ysf_pct):
    dummy_rng = np.arange(0, 100)
    df_monthly_esf = pd.DataFrame(index=dummy_rng)

    factor = 1.0 + convert_ysftomsf_pct(price_ysf_pct) / 100
    val = base_price * (factor ** dummy_rng)

    df_monthly_esf['escalated_price'] = np.where(val < 60,
                                                 60, np.where(val > 120,
                                                              120,
                                                              val))
    return df_monthly_esf


if __name__ == '__main__':
    df = get_monthly_escalated_prices(95, 2.0)
    print(df)
