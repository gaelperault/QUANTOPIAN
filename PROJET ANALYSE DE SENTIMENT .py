from quantopian.algorithm import attach_pipeline, pipeline_output


from quantopian.pipeline import Pipeline
from quantopian.pipeline.factors import AverageDollarVolume

from quantopian.pipeline.data.sentdex import sentiment_free as sentdex

from quantopian.pipeline.factors import CustomFactor

import numpy as np


def initialize(context):
    schedule_function(my_rebalance,date_rules.every_day())
    
    attach_pipeline(make_pipeline(),'pipeline')
    
class AvgSentiment(CustomFactor):
    def compute(self,today,assets,out,impact):
        np.mean(impact,axis=0,out=out)
    
def make_pipeline():
    dollar_volume = AverageDollarVolume(window_length = 30)
    is_liquid = dollar_volume.top(500)
    
    avg_sentiment = AvgSentiment(inputs=[sentdex.sentiment_signal],window_length =10)

    
    return Pipeline(columns = {
            'sentiment': avg_sentiment
        },screen = is_liquid)
                    
                    
def my_rebalance(context,data):
    for security in context.portfolio.positions:
        if security not in context.longs and security not in context.short and data.can_trade(security):
            order_target_percent(security,0)
                    
    for security in context.longs:
        if data.can_trade(security):            
            order_target_percent(security,context.long_weight)
                    
    for security in context.short:
        if data.can_trade(security):            
            order_target_percent(security,context.short_weight)                
                    
    print(context.something)
                    
def before_trading_start(context,data):
    portfo = pipeline_output('pipeline')# extrait les données de la fonction make_pipeline.
    context.something = portfo['sentiment']               
    
                    
    context.longs =  portfo[portfo['sentiment'] > 0 ].index.tolist()
    context.short =  portfo[portfo['sentiment'] < 0 ].index.tolist()                
                    
    context.long_weight,context.short_weight = my_compute_weight(context)               


                    
                    
def my_compute_weight(context):
    if len(context.longs) == 0 :
        long_weight = 0 
    else:      
        long_weight = 0.5/len(context.longs)
    
    
    if len(context.short) == 0 :
        short_weight = 0  
    else: 
        short_weight = -0.5/len(context.short)
                    
                    
    return long_weight,short_weight
                    
                   
                    
### Conclusion: 
#les données sont passées donc on prend des position aprés l'engouement 
# necessaires de construires avec des sentiment concret, plus exploitable.

                    