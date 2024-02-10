from model_db import models
from .orders import List_Trigger




def Check(message:str, lista:list):

    if message.__contains__(lista.pop().trigger_name):

        return True
    
    elif len(lista) == 0:
        
        return False

    else:

        return False or Check(message, lista)


async def Filter(message:str):

    triggers = await List_Trigger()
    return Check(message, triggers)
    
