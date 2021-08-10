import requests as req
import numpy as np
import json

base_url = 'https://alejandronq.pythonanywhere.com/'
path = "master"
data = json.loads(req.get(base_url + path).text)  

while player['alive']:
    while player['dir'] != 0:   #waits for game to reply
        player.update(json.loads(req.get(base_url + path).text))
    
    food = json.loads(req.get(base_url + "master/food").text) 
    
    game.update(json.loads(req.get(base_url + 'master/game').text))
    
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
    req.put(base_url + "player0/dir", data = json.dumps({'dir':player['dir']}))
