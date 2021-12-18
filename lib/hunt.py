from lib.parser import conf

rarities = ['Common', 'Uncommon', 'Alolan', 'Super Rare', 'Rare', 'Full-odds', 'Shiny', 'Legendary']

cheap_legies=["Articuno", "Mew*", "Jirachi", 
              "Moltres", "Raikou", "Entei", 
              "Suicune", "Ho-oh", "Regirock", 
              "Regice", "Registeel", "Latias", 
              "Latios", "Deoxys", "Uxie", 
              "Mesprit", "Azelf", "Heatran", 
              "Regigigas", "Cresselia", "Cobalion", 
              "Terrakion", "Virizion", "Tornadus", 
              "Thundurus", "Landorus", "Xerneas", 
              "Yveltal", "Celebi", "Zygarde"]

def hunt(footer, description):
    for rarity in rarities:
        if rarity in footer:

            if rarity == "Legendary":
                if any(poke in description for poke in cheap_legies):
                    ball = conf.rarities.Cheap_legendary
                
                else:
                    ball = conf.rarities.Legendary
            
            else:
                ball = conf.rarities[str(rarity)]
            
            break

    return ball