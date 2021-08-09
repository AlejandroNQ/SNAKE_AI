import requests as req
import numpy as np
import time
import json

path = "master/players/0"
game = {}
player = json.loads(req.get("http://127.0.0.1:5000/" + path).text) 

banned_dir = [0, 2, 1, 4, 3] #doesn't allow snakes to go backwards

#   {
#       'id': 1,       #int
#       'x': 2,        #int
#       'y': 2,        #int
#       'score': 4,    #int
#       'dir': 4,      #int
#       'prevdir': 4,  #int
#       'alive': True  #bool
#   }

while player['alive']:
    #time.sleep(0.4)
    while player['dir'] != 0:   #waits for game to reply
        player.update(json.loads(req.get("http://127.0.0.1:5000/" + path).text))
    
    food = json.loads(req.get("http://127.0.0.1:5000/master/food").text) 
    
    game.update(json.loads(req.get("http://127.0.0.1:5000/" + 'master/game').text))
    
    card_dist_food = [0 for f in food]
    dist_food      = [0 for f in food]
    
    for f in food:
        card_dist_food[f['id']] = [
               -(f['y'] - player['y']) % game['height'], #up
                (f['y'] - player['y']) % game['height'], #down
               -(f['x'] - player['x']) % game['width'],  #left
                (f['x'] - player['x']) % game['width']   #right
            ]   #stores cardinal distances to each f in food
        
        dist_food[f['id']] = min(
               -(f['y'] - player['y']) % game['height'], #up
                (f['y'] - player['y']) % game['height'], #down
            ) + min(
               -(f['x'] - player['x']) % game['width'],  #left
                (f['x'] - player['x']) % game['width']   #right
            )   #manhattan distance to each f in food
        
    closest_food_id = min(range(len(dist_food)), key=dist_food.__getitem__)
    
    max_dist = max(card_dist_food[closest_food_id])
    
    
    if max_dist == card_dist_food[closest_food_id][0]:
        player['dir'] = 2
    elif max_dist == card_dist_food[closest_food_id][1]:
        player['dir'] = 1
    elif max_dist == card_dist_food[closest_food_id][2]:
        player['dir'] = 4
    elif max_dist == card_dist_food[closest_food_id][3]:
        player['dir'] = 3
    
    #avoid collision
    gonna_crash = True  #just so it checks
    while gonna_crash:
        gonna_crash = False
        if player['dir'] == 1:
            if game['board'][(player['y'] - 1) % game['height']][player['x']] > 0:
                gonna_crash = True
        elif player['dir'] == 2:
            if game['board'][(player['y'] + 1) % game['height']][player['x']] > 0:
                gonna_crash = True
        elif player['dir'] == 3:
            if game['board'][player['y']][(player['x'] - 1) % game['width']] > 0:
                gonna_crash = True
        elif player['dir'] == 4:
            if game['board'][player['y']][(player['x'] + 1) % game['width']] > 0:
                gonna_crash = True
        if gonna_crash:
            player['dir'] = np.random.randint(1,5)
    
    #avoids going backwards
    if player['dir'] == banned_dir[player['prevdir']]:
        player['dir'] = player['prevdir']
    
    #for i in range(game['height']):
    #    string = '│'
    #    for j in range(game['width']):
    #        if game['board'][i][j] > 0:
    #            #string = string + ' ' + str(int(data['game']['board'][i][j] / len(data['players'])))
    #            string = string + ' ' + str(int(game['board'][i][j]))
    #        elif game['board'][i][j] < 0:
    #            string = string + ' @'
    #        else:
    #            string = string + ' ·'
    #    print(string + ' │')
    #print()
    
    print(player['dir'])
    req.put("http://127.0.0.1:5000/player0/dir", data = json.dumps({'dir':player['dir']}))






#path = "master/game"
#response = json.loads(req.get("http://127.0.0.1:5000/" + path).text)
#
#response['width']=16
#req.put("http://127.0.0.1:5000/login", data = json.dumps({'game':response}))