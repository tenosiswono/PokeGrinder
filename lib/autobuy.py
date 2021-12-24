import re
from lib.parser import conf

balls = [["pokeball", "1"], ["ultraball", "3"], ["greatball", "2"], ["masterball", "4"]]

async def get_balls(embed):
    n = 0

    for f in [i for i in re.sub("[^0-9]", " ", str(embed).split("═════ Balls left ═════\\n")[1].replace(",", "")).split(" ") if i.isdigit()]:
        if int(f) == 0:
            n = n
            break

        else:
            n += 1
    
    if n > 3:
        return
    
    msg = f";s b {(balls[n][1])} {conf.autobuy[str(balls[n][0])]}"

    return msg