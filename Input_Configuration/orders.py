from model_db import models
from django.db import IntegrityError
from asgiref.sync import sync_to_async



store_words = lambda s: [word.strip('.,') for word in s.split()]
get_names_from_queryset = lambda queryset: [obj.chat_name for obj in queryset]

def List_Chat_Syncro():

    return get_names_from_queryset(models.Chat.objects.all())

@sync_to_async
def List_Chat():

    return list(models.Chat.objects.all())

@sync_to_async
def List_Trigger():

    return list(models.Trigger.objects.all())

@sync_to_async
def List_Recipent():

    return list(models.Recipent.objects.all())

#Create a String from the input recursevly
def Stringify_List(lista1:list, lista2:list):

    if len(lista1) == 0 :

        return ""
    
    else:

        return lista1.pop() + "\n " + str(lista2.pop()) + "\n " + Stringify_List(lista1, lista2)


def Help():

    return "Basic Usage: \n  [Order][Input] /n  EXAMPLE:    add_trigger call \n  ORDERS: \n  add_chat Add a new chat to filter messages, if the chat is already added you'll be notified \n add_trigger add a new trigger for filter the chats, if the trigger already exists you'll be notified \n add_recipient add a chat to send the forwaded messages, if none it's added it will be send to your saved mesages, use 'me' to refer at your saved messages. \n you can add more than one input separating with spaces \n list: structure: \n List [Options] \n OPTIONS: \n c: list all the chats. \n t: list all the triggers \n r: list all the recipents \n if you dont introduce none of them you recieve all the lists \n delete_chat: delete chats given the names \n delete_trigger: delete triggers given the names \n delete_recipent: delete recipents given the names."
#Add a chat
async def add_chat(lista:list):

    for i in lista:

        try:
            
            obj = await models.Chat.objects.acreate(chat_name=i)
            await obj.asave()

        except IntegrityError:

            return "Ojeto "+ i +" ya existente"
            
    return "Objetos creados"

#Add a trigger
async def add_trigger(lista:list):

    print('Go for add trigger')
    for i in lista:

        try:
            
            obj =  await models.Trigger.objects.acreate(trigger_name=i)
            await obj.asave()

        except IntegrityError:

            return "Ojeto "+ i +" ya existente"
            
    return "Objetos creados"

#Add a recipent
async def add_recipent(lista:list):

    for i in lista:

        try:
            
            obj = await models.Recipent.objects.acreate(chat_name=i)
            await obj.asave()

        except IntegrityError:

            return "Ojeto "+ i +" ya existente"
            
    return "Objetos creados"

#List Elements
async def List(lista:list):

    if len(lista) == 0:
        #If the options would not be specified it returns all
        chats = await List_Chat()
        triggers = await List_Trigger()
        recipents = await List_Recipent()
        
        return "Chats: \n " + str(chats) + " \n Triggers: \n" + str(triggers) + "\n Recipents: \n" + str(recipents)
    
    elements = []

    for i in lista:
        #Evaluate the options asked and find all the elements
        if i == 'c':

            elements.append(await List_Chat())

        elif i == 't':

            elements.append(await List_Trigger())

        elif i == 'r':

            elements.append(await List_Recipent())
        
        else:

            return "Wrong Entry"

    return Stringify_List(lista, elements)


async def delete_chat(lista:list):

    for i in lista:

        try:

            aux = await  models.Chat.objects.aget(chat_name=i)
            await aux.adelete()

        except models.Chat.DoesNotExist :

            return "The element does not exists"
        
    return "elements deleted"


async def delete_trigger(lista:list):

    for i in lista:

        try:

            
            aux = await models.Trigger.objects.aget(trigger_name=i)
            await aux.delete()

        except models.Trigger.DoesNotExist:

            return "The element does not exists"
        
    return "elements deleted"


async def delete_recipent(lista:list):

    for i in lista:

        try:
      
            aux = await models.Recipent.objects.aget(chat_name=i)
            await aux.adelete()

        except models.Recipent.DoesNotExist:

            return "The element does not exists"
        
    return "elements deleted"

#Recognize the operation of the user
async def Interpreter(input:str):

    lista = store_words(input)
    print('Interpreter Init')
    for i in lista:

        if i.lower() == 'help':

            return Help()    
        
        elif i.lower() == 'add_chat':

            return await add_chat(lista[lista.index(i) + 1 :])
        
        elif i.lower() == 'add_trigger':
            print('Detected entry trigger')
            return await add_trigger(lista[lista.index(i) + 1 :])
        
        elif i.lower() == 'add_recipent':
            
            return await add_recipent(lista[lista.index(i) + 1:])
        
        elif i.lower() == 'list':

            return await List(lista[lista.index(i) + 1:])
        
        elif i.lower() == 'delete_chat':

            return await  delete_chat(lista[lista.index(i) + 1:])
        
        elif i.lower() == 'delete_trigger':

            return await delete_trigger(lista[lista.index(i) + 1:])
        
        elif i.lower() == 'delete_recipent':

            return await delete_recipent(lista[lista.index(i)+ 1:])