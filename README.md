# SNAKE AI
Good old arcade games, right? 
Well, yes, but here's the catch: **it's not designed for human players**, but rather for AIs. That's why the whole interface is carried out though an online API.


## The game:
The game itself is somewhere between the classical [Snake](https://en.wikipedia.org/wiki/Snake_(video_game_genre)) game we all know and love and the even older [Blockade](https://en.wikipedia.org/wiki/Blockade_(video_game)) (or the better known 1982 [Tron](https://en.wikipedia.org/wiki/Tron_(video_game)) Light Cycles). It combines the best of both worlds. With Blockade's PvP gameplay and Snake's growing mechanics it's a fun competitive game yet simple as can be.

The code for the game itself won't be avaliable anytime in the near future but 

## The API:
The goal is to make this a avaliable for anyone interested regardless of their coding experience, for that very reason we use a [RESTful](https://en.wikipedia.org/wiki/Representational_state_transfer) web API, meaning (among other things), that it can be accessed from anywhere. The main goal with this aproach is to make it language independent, which is also why data is always handled in [JSON](https://en.wikipedia.org/wiki/JSON).

All relevant aspects of the game are stored in a JSON file with the following structure:

```javascript
data = {
    'game':{
        'height': 16, 
        'width': 16,  
        'board': []   
    },
    'players':[
        {
            'id': 0,
            'x': 2,       
            'y': 2,       
            'score': 4,   
            'dir': 4,     
            'prevdir': 4, 
            'alive': True 
        },
        {
            'id': 1,
            'x': 13,      
            'y': 13,      
            'score': 4,   
            'dir': 3,     
            'prevdir': 3, 
            'alive': True 
        }
    ],
    'food':[
        {
            'id': 0,
            'x': 6,
            'y': 6,
            'value': 1
        },
        {
            'id': 1,    
            'x': 9,
            'y': 9,
            'value': 1 
        }
    ]
}
```

Different parts of it can be accessed as follows:
`base_url/`

Code examples for basic AIs are provided bellow.

## The AI:
The term AI here is understood acording to [this definition](https://en.wikipedia.org/wiki/Artificial_intelligence#:~:text=Leading%20AI%20textbooks%20define%20the%20field%20as%20the%20study%20of%20%22intelligent%20agents%22%3A%20any%20system%20that%20perceives%20its%20environment%20and%20takes%20actions%20that%20maximize%20its%20chance%20of%20achieving%20its%20goals.) as *"any system that perceives its environment and takes actions that maximize its chance of achieving its goals"*. Thus, it has three main components:

1. **Get information about the enviorment:** that is, all key positions for things to avoid or get to. This is archived though a HTTP GET request (example provided below).
2. **Decide what to do based on that:** that's the part you have to think real hard about. It can be either algorithmic or based on any form of machine learning.
3. **Act:** comunicate to the game in which direction you want your snake to move. We use HTTP PUT method for this.

## Examples

Python - 
