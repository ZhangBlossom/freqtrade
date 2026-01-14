from freqtrade.strategy import IStrategy
from pandas import DataFrame
import talib.abstract as ta


class MA5CrossMA20_4h(IStrategy):
    """
    4h 趋势示例策略：
    - 入场：MA5 > MA20
    - 出场：MA5 < MA20
    """

    timeframe = "4h"
    startup_candle_count = 30

    minimal_roi = {
        "0": 0.10   # 给一个宽松止盈（演示用）
    }

    stoploss = -0.10  # 10% 止损（演示用）

    use_exit_signal = True
    exit_profit_only = False

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe["ma5"] = ta.SMA(dataframe["close"], timeperiod=5)
        dataframe["ma20"] = ta.SMA(dataframe["close"], timeperiod=20)
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
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
