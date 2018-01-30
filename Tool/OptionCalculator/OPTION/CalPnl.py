# -*- coding:utf-8 -*-
class CalPnl():
    # this class will help to calculate the profit or Loss of one option
    # contract

    def __init__(self):
        self.action_code = None
        """self.CalMargin=CalMargin()
        lastDayConSettlementPrice
        LastCloseUndeylingPrice
        StrikePrice
        currentUnderlyingPrice
        OptionType,Count,action"""
        self.CalMaxMinChange = CalMaxMinChange()

        pass

    def __version(self):
        version = 0.1
        return version

    def AddCalMargin(self, lastDayConSettlementPrice, LastCloseUndeylingPrice, StrikePrice, currentUnderlyingPrice, OptionType, Count, action, exchangerate=100 * 100, OptionFormat='E'):

        self.CalMargin = CalMargin(lastDayConSettlementPrice, LastCloseUndeylingPrice, StrikePrice,
                                   currentUnderlyingPrice, OptionType, Count, action, exchangerate=exchangerate, OptionFormat=OptionFormat)
        return self.CalMargin.OpenMarginRule()

    def MaturityPnLFree(self, b, Strike, currentUnderlyingPrice, ContractNum, action, OptionType, w=3, n=1000, exchangerate=100 * 100):
        w = w * n
        #pricelist=np.array([currentUnderlyingPrice*(draft/float(w)+1) for draft in xrange(1-w,1+w,1)])
        out = [(currentUnderlyingPrice * (draft / float(w) + 1), self.CalProfitOrLossofMaturityVersion1(b, Strike, currentUnderlyingPrice *
                                                                                                        (draft / float(w) + 1), ContractNum, action, OptionType, exchangerate=exchangerate)) for draft in xrange(1 - w, 1 + w, 1)]

        return pd.DataFrame(out, columns=['UnderlyingPrice', 'PnL'])

    def MaturityPnLHigh_Low(self, b, Strike, currentUnderlyingPrice, ContractNum, action, OptionType, LastCloseUndeylingPrice, w=3, n=1000, exchangerate=100 * 100):
        Highchange, Lowchange = self.CalMaxMinChange.getBoundry(
            LastCloseUndeylingPrice, Strike, OptionType)
        High = currentUnderlyingPrice * (1 + Highchange)
        Low = currentUnderlyingPrice * (1 - Highchange)
        if float(High - Low) < 20.0 / n:
            gap = float(High - Low) / 20
        else:
            gap = 1.0 / n
        #np.arange(Low, High, gap)
        print High, Low
        out = [(price, self.CalProfitOrLossofMaturityVersion1(b, Strike, price, ContractNum,
                                                              action, OptionType, exchangerate=exchangerate)) for price in np.arange(Low, High, gap)]
        return pd.DataFrame(out, columns=['UnderlyingPrice', 'PnL'])

    def CalPnlofMaturityV1(self, BuyorSellPrice, StrikePrice, currentUnderlyingPrice, ContractNum, action, OptionType, exchangerate=100 * 100):
        self.action_code = - \
            1 if action in ['buy', 'Buy', 'B', 'b', 'BUY'] else 1
        if OptionType in ['Put', 'P', 'p']:
            perG = max(StrikePrice - currentUnderlyingPrice, 0)
        elif OptionType in ['Call', 'C', 'c']:
            perG = max(currentUnderlyingPrice - StrikePrice, 0)
        else:
            raise ValueError('Unknown OptionType: %s' % OptionType)
        OptionFee = BuyorSellPrice  # RealCost
        return ContractNum * exchangerate * self.action_code * (OptionFee - perG)

    def CalProfitOrLossofMaturityVersion1(self, BuyorSellPrice, StrikePrice, currentUnderlyingPrice, ContractNum, action, OptionType, exchangerate=100 * 100):
        self.action_code = - \
            1 if action in ['buy', 'Buy', 'B', 'b', 'BUY'] else 1
        if OptionType in ['Put', 'P', 'p']:
            if currentUnderlyingPrice < StrikePrice:
                # print 'will Execute Put contract'
                # step 1 Buy Low market stock
                VirtualBuySpendMoney = currentUnderlyingPrice
                # step 2 Sell bought stock to the Contract Writer with strike
                # Price
                VirtualSellObtainMoney = StrikePrice
                G = VirtualSellObtainMoney - VirtualBuySpendMoney
            else:
                #
                G = 0
            """OptionFee=BuyorSellPrice#RealCost
            finalProft=ContractNum*exchangerate*(self.action_code*(OptionFee-G))
            return finalProft"""
        elif OptionType in ['Call', 'C', 'c']:
            # print 'Call'
            if currentUnderlyingPrice > StrikePrice:
                # print 'will Execute Call contract'
                # step 1 Buy Low  price to the Contract Writer with strike
                # Price
                VirtualBuySpendMoney = StrikePrice

                # step 2 Sell High stock
                VirtualSellObtainMoney = currentUnderlyingPrice
                G = VirtualSellObtainMoney - VirtualBuySpendMoney
            else:
                G = 0

        else:
            raise ValueError('Unknown OptionType: %s' % OptionType)
        OptionFee = BuyorSellPrice  # RealCost
        finalProft = ContractNum * exchangerate * \
            self.action_code * (OptionFee - G)
        return finalProft


class CalMaxMinChange():

    def __init__(self):
        """认购期权最大涨幅＝max｛合约标的前收盘价×0.5%，min [（2×合约标的前收盘价－行权价格），合约标的前收盘价]×10％｝
        认购期权最大跌幅＝合约标的前收盘价×10％
        认沽期权最大涨幅＝max｛行权价格×0.5%，min [（2×行权价格－合约标的前收盘价），合约标的前收盘价]×10％｝
        认沽期权最大跌幅＝合约标的前收盘价×10％"""
        pass

    def getBoundry(self, LastCloseUndeylingPrice, StrikePrice, OptionType):
        if OptionType in ['Call', 'C', 'c']:
            return self.getCallBoundry(LastCloseUndeylingPrice, StrikePrice)
        elif OptionType in ['Put', 'P', 'p']:
            return self.getPutBoundry(LastCloseUndeylingPrice, StrikePrice)
        else:
            raise ValueError('Unknown OptionType: %s' % OptionType)

    def getCallBoundry(self, LastCloseUndeylingPrice, StrikePrice):
        CallHigh = max(LastCloseUndeylingPrice * (0.5 / 100), (min(2 *
                                                                   LastCloseUndeylingPrice - StrikePrice, LastCloseUndeylingPrice * 0.1)) * 0.1)
        CallLow = LastCloseUndeylingPrice * 0.1
        return CallHigh, CallLow

    def getPutBoundry(self, LastCloseUndeylingPrice, StrikePrice):
        PutHigh = max(StrikePrice * (0.5 / 100), (min(2 * StrikePrice -
                                                      LastCloseUndeylingPrice, LastCloseUndeylingPrice)) * 0.1)
        PutLow = LastCloseUndeylingPrice * 0.1
        return PutHigh, PutLow


class CalMargin():
    # this class will calculate the Open Margin  and Maintain Margin

    def __init__(self, lastDayConSettlementPrice, LastCloseUndeylingPrice, StrikePrice, currentUnderlyingPrice, OptionType, Count, action, exchangerate=100 * 100, OptionFormat='E'):
        self.lastDayConSettlementPrice = lastDayConSettlementPrice
        self.LastCloseUndeylingPrice = LastCloseUndeylingPrice
        self.OptionType = OptionType
        self.StrikePrice = StrikePrice
        self.currentUnderlyingPrice = currentUnderlyingPrice
        self.action = action
        self.Count = Count * exchangerate
        self.OptionClss = {'50ETF': {'CallOps1': 0.12,
                                     'CallOps2': 0.07, 'PutOps1': 0.12, 'PutOps2': 0.07}}

    def __version(self):
        version = 0.1
        return version

    def CalOutofMoney(self):
        # 认购期权虚值=Max（行权价-合约标的前收盘价，0）
        # 认沽期权虚值=max（合约标的前收盘价-行权价，0）。
        if self.OptionType in ['Call', 'C', 'c']:
            return max(self.StrikePrice - self.LastCloseUndeylingPrice, 0)
        elif self.OptionType in ['Put', 'P', 'p']:
            return max(self.LastCloseUndeylingPrice - self.StrikePrice, 0)
        else:
            raise ValueError('Unknown OptionType: %s' % self.OptionType)

    def OpenMarginRule(self):
        CallOps1 = self.OptionClss['50ETF']['CallOps1']
        CallOps2 = self.OptionClss['50ETF']['CallOps2']
        PutOps1 = self.OptionClss['50ETF']['PutOps1']
        PutOps2 = self.OptionClss['50ETF']['PutOps2']

        """认购期权义务仓开仓保证金＝[合约前结算价+Max（12%×合约标的前收盘价-认购期权虚值，7%×合约标的前收盘价）]×合约单位
        认沽期权义务仓开仓保证金＝Min[合约前结算价+Max（12%×合约标的前收盘价-认沽期权虚值，7%×行权价格），行权价格] ×合约单位"""

        if self.action == 'Buy':
            return 0
        else:
            if self.OptionType in ['Call', 'C', 'c']:
                OutofMoney = max(self.StrikePrice -
                                 self.LastCloseUndeylingPrice, 0)
                return self.Count * (self.lastDayConSettlementPrice + max(CallOps1 * self.LastCloseUndeylingPrice - OutofMoney, CallOps2 * self.LastCloseUndeylingPrice))
            elif self.OptionType in ['Put', 'P', 'p']:
                OutofMoney = max(
                    self.LastCloseUndeylingPrice - self.StrikePrice, 0)
                # print OutofMoney,self.lastDayConSettlementPrice,self.LastCloseUndeylingPrice,self.StrikePrice,PutOps1,PutOps2,1*100*100*min(0.0014+max(0.12*2.637-OutofMoney,0.07*2.45),2.45)
                # print  self.Count*min(self.lastDayConSettlementPrice+max(PutOps1*self.LastCloseUndeylingPrice-OutofMoney,PutOps1*self.StrikePrice),self.StrikePrice)
                # print
                # self.Count*min(self.lastDayConSettlementPrice+max(PutOps1*self.LastCloseUndeylingPrice-OutofMoney,PutOps2*self.StrikePrice),self.StrikePrice)
                return self.Count * min(self.lastDayConSettlementPrice + max(PutOps1 * self.LastCloseUndeylingPrice - OutofMoney, PutOps2 * self.StrikePrice), self.StrikePrice)

            else:
                raise ValueError('Unknown OptionType: %s' % self.OptionType)

    def MaintainMarginRule(self, CloseUndeylingPrice, ToDayConSettlementPrice):
        self.CloseUndeylingPrice = CloseUndeylingPrice
        self.ToDayConSettlementPrice = ToDayConSettlementPrice
        CallOps1 = self.OptionClss['50ETF']['CallOps1']
        CallOps2 = self.OptionClss['50ETF']['CallOps2']
        PutOps1 = self.OptionClss['50ETF']['PutOps1']
        PutOps2 = self.OptionClss['50ETF']['PutOps2']

        """
        认购期权义务仓维持保证金＝[合约结算价+Max（12%×合约标的收盘价-认购期权虚值，7%×合约标的收盘价）]×合约单位
        认沽期权义务仓维持保证金＝Min[合约结算价 +Max（12%×合标的收盘价-认沽期权虚值，7%×行权价格），行权价格]×合约单位
        """
        if self.action == 'Buy':
            return 0
        else:
            if self.OptionType in ['Call', 'C', 'c']:
                OutofMoney = max(self.StrikePrice -
                                 self.CloseUndeylingPrice, 0)
                # CallOps1=0.12
                # CallOps2=0.07
                return self.Count * (self.ToDayConSettlementPrice + max(CallOps1 * self.CloseUndeylingPrice - OutofMoney, CallOps2 * self.CloseUndeylingPrice))
            elif self.OptionType in ['Put', 'P', 'p']:
                OutofMoney = max(self.CloseUndeylingPrice -
                                 self.StrikePrice, 0)
                return self.Count * min(self.ToDayConSettlementPrice + max(PutOps1 * self.CloseUndeylingPrice - OutofMoney, PutOps2 * self.StrikePrice), self.StrikePrice)
            else:
                raise ValueError('Unknown OptionType: %s' % self.OptionType)

StrikePrice = 2.45
LastCloseUndeylingPrice = 2.637
max(LastCloseUndeylingPrice - StrikePrice, 0)  # CalOutofMoney虚值期权
