
import pandas as pd


def export_csv(test_cases):

    dataframe = pd.DataFrame(test_cases)

    return dataframe.to_csv(
        index=False
    ).encode("utf-8-sig")
