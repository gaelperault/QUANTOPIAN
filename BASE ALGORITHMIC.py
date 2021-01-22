# code python

##### Optimisation de portefeuille

# Portefeuille : Appl , Cisco ,Amazon, IBM

##### OBJECTIF : 

 # Optimisation de l'allocation des titres.
    
   # on va simuler l'achat de trois action et les garder un certain temps


############################   INITIALISATION  ############################

#def initialize(context):
    #context.techies = [sid(16841),sid(24),sid(1900)]
    # context.appl = sid(24)
    # context.csco = sid(1900)
    # context.amzn = sid(16841)
    
#def handle_data(context,data): # appeler une fois a la fin de chaque minute
    #price_history = data.history(context.techies,fields = 'price',
                                 #bar_count = 5, frequency = '1d')
    
    #print(price_history)

    
    
#methode 
    #if data.can_trade(sid(16841)):
        #order_target_percent(sid(16841),1.0)
        # regarde si l'actif est sur le marché et retourne True
        # si c'est le cas il place l'ordre d'achat
        # sinon on ne peut pas le placer.
# methode  : 

    # print(data.is_stale(sid(24)))
    #retourne True si l'actif a déja était échangeais et False sinon.
    # permet de savoir si notre methode est en accord avec celle du backtest

#methode 
   #tech_close = data.current(context.techies,'close')
  # print(tech_close)
   # on obtient pour chaque minute le prix de cloture de chaque actifs.
 
# methode :   
    # order_target_percent(24,.27)
    # order_target_percent(1900,.20)
    # order_target_percent(16841,.53) 
    # permet d'envoyer un ordre d'achat avec des caracteristiques
    
    
####### Fonction de  Planification ( schedule function ) 




# cette fonction donne des ordres de trading , elle achette ou vend tel sid avec tel pourcentage.

def initialize(context):
    context.aapl = sid(24)
    
    schedule_function(open_positions,date_rules.week_start(),
                      time_rules.market_open())
    
    schedule_function(close_positions,date_rules.week_end(),
                      time_rules.market_close(minutes = 30 ))  # ici on planifie la liquidation de nos actions appl 30 minutes avant la fin de la seance. 

def open_positions(context,data):
    order_target_percent (context.aapl,0.10)
    
 
def close_positions(context,data):    
    order_target_percent(context.aapl,0)
    
    
#On a une fonction qui a l'ouverture alloue 10% du portefeuille sur les actions appl.
#et une autre qui liquide notre position en fin de journée.



    
    