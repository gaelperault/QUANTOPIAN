################################## ALGORITHME BANDE BOLLINGER #####################################

import numpy as np
import pandas as pd
# initialize -- Schedule Function

## on enonce notre plan :
#on a besoin de l'action puis de dire ce qu'on lui fait : 


####################################### 1ER ETAPE #############################################

# INITIALISATION

def initialize(context):
    context.jj = sid(39840)
    schedule_function(check_bands, date_rules.every_day()) # on dit qu'on schedule la fonction check_bands.


############################### 2EME ETAPE ###################################################

# QU'EST CE QUE LA FONCTION CHECK_BAND


def check_bands(context,data):
    cur_price = data.current(context.jj,'price')  # matrice des prix actuelle  sur la periode.
    prices = data.history(context.jj,'price',20,'1d') # retourne l'historique sur 20 jours de jj.
    # on va donc comparer dans les conditions if si le prix actuel est superieur ou inf à la #         #moyenne glisante sur 20 jours  c a dire moyenne des 20 prix precedents.
    avg_20 = prices.mean()
    std_20 = prices.std()
    
    lower_band = avg_20 - (2* std_20)   # bande de bollinger 
    upper_band = avg_20 + (2* std_20)
   
   
    
    if cur_price > upper_band:    # vente à découvert  ( short )
        order_target_percent(context.jj,1)
        print("vente à decouvert ")
        context.shorting_spread = True 
        context.long_on_spread = False
        
    

    elif cur_price < lower_band:    #  ACHAT  ( long ) 
        order_target_percent(context.jj,1)
        print("achat")
        context.long_on_spread = True
        context.shorting_spread = False
    
    if cur_price == avg_20:    # on liquide les positions quand ca revient au prix d'équilibre
       order_target_percent(context.jj,0)
    
    else : 
        pass
    
    record(upper =  upper_band , lower=lower_band, price = cur_price)
    ## RECORD PERMET LE TRAÇAGE DE L'ÉVOLUTION DE CES VARIABLES.
    
###################################End################################################    
    
    ######### STATEGIE TROP SIMPLISTE #########################