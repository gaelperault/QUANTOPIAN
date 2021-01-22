################################# Le Trading de pairs #############################################
import numpy as np 


# initialize -- Schedule Function


def initialize(context):
    
    context.aa = sid(45971)
    context.ual = sid(28051)
    
    context.long_on_spread = False  # Verificateurs ou drapeau.
    context.shorting_spread = False 
    
    schedule_function(check_pairs ,date_rules.every_day(),
                     time_rules.market_close(minutes = 60))

    
    
#check_pairs


def check_pairs(context,data):
    aa = context.aa
    ual = context.ual
    # obtenir les données de prix sous dataframe : 
    prices = data.history([aa,ual],'price',30,'1d')
    # permet d'obtenir les prix à l'heure actuelle de mon backtest car on  selectionne les derniers prix de chaque action 
    short_prices= prices.iloc[-1,:]
    
    
    #Spread
    
    mavg_30 = np.mean(prices[aa]-prices[ual])
    std_30 = np.std(prices[aa]-prices[ual])
    mavg_1 = np.mean(short_prices[aa]-short_prices[ual])
    
    
    
    if std_30 > 0  : # ca veut dire qu'on a au moins 30 jours d'informations.
        zscore_30  =  ( mavg_1 - mavg_30 ) / std_30   #z score normalisé à 30 jours 

        if zscore_30 > 0.5 and not context.shorting_spread :
        # si zscore > 0 ca veut dire que American airline est sur évalué donc devrait revenir à 0 car coorélé avec l'autre.donc je vais shorter American airlines.
         order_target_percent(aa,-0.5) # short
         order_target_percent(ual,0.5)   # long
        
        # il faut dire a l'algo ce qu'il se passe sur le spread American airlines.
         #on precise qu'on ouvre le short sur le spread American airlines
         context.shorting_spread = True 
         context.long_on_spread = False  
        
        
        
        elif zscore_30 < -1 and not context.long_on_spread :
            order_target_percent(aa,0.50)
            order_target_percent(ual,-0.5)
               
            context.long_on_spread = True  
            context.shorting_spread= False  #on precise qu'on ferme le short American airlines.
            
            #LA CLOTURE D'UNE TRANSACTION SE TERMINE PAR L'OPPOSÉ.
            #SI J'ACHÈTE ALORS JE VEND
           # SI JE VEND A DEC ALORS JE RACHETE.
           
            
##. le if et le elif definisse la stratégie : 
### quand le spread est positif on short american airline et on achete ual.
#car on se dit que le spread revient vers 0.
# quand le spread passe en negatif alors ual sur evalué et/ou aa sur evalué donc on vend ual et on rachete aa. et dans la situatio inverse aussi 
            
    
    
        elif abs(zscore_30) < 0.1 : 
            
              order_target_percent(aa,0)
              order_target_percent(ual,0)
              context.long_on_spread = False
              context.shorting_spread= False
            
            
              record(Z_score  = zscore_30)