from freqtrade.strategy import IStrategy
from pandas import DataFrame
import talib.abstract as ta


class RsiRebound15m(IStrategy):
    """
    15m 数据专用演示策略（Trades 一定 > 0）：
    - 入场：RSI 从低位反弹上穿 35 + 价格仍在MA20下方（回撤后转强）
    - 出场：RSI > 60 或价格上穿MA20（走出回撤区）
    """

    timeframe = "15m"
    startup_candle_count = 50

    # 让它容易出场，便于你观察交易
    minimal_roi = {"0": 0.01}   # 1% 即可出场（演示用）
    stoploss = -0.05           # 5% 止损（演示用）

    use_exit_signal = True
    exit_profit_only = False
    ignore_roi_if_entry_signal = False

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe["rsi"] = ta.RSI(dataframe["close"], timeperiod=14)
        dataframe["ma20"] = ta.SMA(dataframe["close"], timeperiod=20)
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # RSI 上穿 35：代表“从弱到强”的反弹
        # 同时 close < MA20：代表仍处于“回撤区”，不是追高
        dataframe.loc[
            (
                    (dataframe["rsi"] > 35) &
                    (dataframe["rsi"].shift(1) <= 35) &
                    (dataframe["close"] < dataframe["ma20"])
            ),
            "enter_long"
        ] = 1
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                    (dataframe["rsi"] > 60) |
                    (dataframe["close"] > dataframe["ma20"])
            ),
            "exit_long"
        ] = 1
        return dataframe
