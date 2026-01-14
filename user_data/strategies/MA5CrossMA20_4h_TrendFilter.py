from freqtrade.strategy import IStrategy
from pandas import DataFrame
import talib.abstract as ta


class MA5CrossMA20_4h_TrendFilter(IStrategy):
    timeframe = "4h"
    startup_candle_count = 210  # MA200 需要

    minimal_roi = {"0": 0.10}
    stoploss = -0.10

    use_exit_signal = True
    exit_profit_only = False

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe["ma5"] = ta.SMA(dataframe["close"], 5)
        dataframe["ma20"] = ta.SMA(dataframe["close"], 20)
        dataframe["ma50"] = ta.SMA(dataframe["close"], 50)
        dataframe["ma200"] = ta.SMA(dataframe["close"], 200)
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                # 大趋势过滤
                    (dataframe["ma50"] > dataframe["ma200"]) &
                    # 原 MA5/20 交叉
                    (dataframe["ma5"] > dataframe["ma20"]) &
                    (dataframe["ma5"].shift(1) <= dataframe["ma20"].shift(1))
            ),
            "enter_long"
        ] = 1
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                    (dataframe["ma5"] < dataframe["ma20"]) &
                    (dataframe["ma5"].shift(1) >= dataframe["ma20"].shift(1))
            ),
            "exit_long"
        ] = 1
        return dataframe
