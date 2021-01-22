def initialize(context):
    context.tesla = sid(39840)
    context.amzn = sid(16841)
    
    #set_max_leverage(1.05)
    schedule_function(rebalance,date_rules.every_day(),time_rules.market_open())     
    schedule_function(record_vars,date_rules.every_day(),time_rules.market_close())                                                           
                                                                                     

def rebalance(context,data):
    #order_target_percent(context.amzn,0.5)
    #order_target_percent(context.ibm,-0.5)
    
    #effet de levier mannuelle 
    order_target_percent(context.tesla,2)
    order_target_percent(context.amzn,-2)
    
    
def record_vars(context,data):
    
    record(amzn_close = data.current(context.tesla,'close'))
    record(ibm_close = data.current(context.amzn,'close'))
    record(leverage = context.account.leverage)
    record(exposure = context.account.net_leverage)
    
    
    
## effet de levier  = dette+base/ base 


#  leverage =  effet de levier reel = exposition  au risque brute / liquidation net

##. exposition au risque :
# exposure = exposition  au risque net/ liquidation net




# on peut emprunter de l'argent specifiant une valeur > 1 dans order_target_percent.