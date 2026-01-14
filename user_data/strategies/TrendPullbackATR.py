from freqtrade.strategy import IStrategy
from pandas import DataFrame
import talib.abstract as ta


class TrendPullbackATR(IStrategy):
    timeframe = "5m"

    minimal_roi = {
        "0": 0.02,
        "60": 0.01,
        "180": 0
    }

    stoploss = -0.15

    startup_candle_count = 240

    trailing_stop = True
    trailing_stop_positive = 0.01
    trailing_stop_positive_offset = 0.02
    trailing_only_offset_is_reached = True

    use_exit_signal = True

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe["ema50"] = ta.EMA(dataframe["close"], timeperiod=50)
        dataframe["ema200"] = ta.EMA(dataframe["close"], timeperiod=200)
        dataframe["rsi"] = ta.RSI(dataframe["close"], timeperiod=14)
        dataframe["atr"] = ta.ATR(dataframe, timeperiod=14)
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                    (dataframe["ema50"] > dataframe["ema200"]) &      # 上升趋势
                    (dataframe["close"] > dataframe["ema200"]) &     # 不做逆势
                    (dataframe["close"] < dataframe["ema50"] * 1.01) &  # 回踩 EMA50
                    (dataframe["rsi"] < 45)                           # 中度回撤
            ),
            "enter_long",
        ] = 1
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                    (dataframe["rsi"] > 65) |                          # 动量耗尽
                    (dataframe["close"] < dataframe["ema50"])          # 跌破短期趋势
            ),
            "exit_long",
        ] = 1
        return dataframe
