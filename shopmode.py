
"""
Copyright 2014 Andrew Russell

This file is part of PotionWars.
PotionWars is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

PotionWars is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with PotionWars.  If not, see <http://www.gnu.org/licenses/>.
"""
from __future__ import division
import universal
from universal import *
import items
import person
import townmode
import conversation
import person

shopkeeper = None
shopGoods = []
playerGoods = []
INDEX = 0
ITEM = 1
PRICE = 2

#Note: This code is not written for a party. It defaults to the PC. Not good.
global chosenPerson
def set_goods():
    global shopGoods, playerGoods
    shopGoods = zip([str(i) for i in range(1, len(shopkeeper.inventory)+1)], 
            shopkeeper.inventory, [str(good.price) for good in shopkeeper.inventory])
    playerGoods = zip([str(i) for i in range(1, len(universal.state.player.inventory) + len(universal.state.player.equipmentList)+1)], 
            universal.state.player.inventory + universal.state.player.equipmentList, 
            [str(good.price // 2) for good in universal.state.player.inventory + universal.state.player.equipmentList])

litany = None
def shop_mode(personIn=None, doneShoppingLitany=None):
    global shopkeeper, litany
    if personIn is not None:
        shopkeeper = personIn
    set_goods()
    say_title(' '.join(['''Shopping with''', shopkeeper.printedName]))
    litany = doneShoppingLitany
    universal.say('"What can I do for you?"')
    set_commands(['(B)uy', '(S)ell', '<==Leave'])
    set_command_interpreter(shop_interpreter)

def shop_interpreter(keyEvent):
    if keyEvent.key == K_b: 
        window_shop() 
    elif keyEvent.key == K_s:
        window_sell()
    elif keyEvent.key == K_BACKSPACE:
        if litany is None:
            townmode.town_mode()
        else:
            shopkeeper.litany = litany
            say_title(universal.state.location.name)
            conversation.converse_with(shopkeeper, townmode.town_mode)

def window_shop():
    global chosenPerson
    if person.get_party().len() == 1:
        chosenPerson = universal.state.player
        window_shop_person_chosen()
    else:
        say_title('Please select a character to go shopping.')
        universal.say(person.get_party().display())
        set_commands('(#) Select a character.', '<==Back')
        set_command_interpreter(select_character_to_buy_interpreter)

def window_shop_person_chosen():
    say_title('Coins: ' + str(chosenPerson.coins))
    listOne = [i + ". " + good.name + ': ' + price for (i, good, price) in shopGoods[:10]]
    #listOne.append('\t')
    listTwo = [i + ". " + good.name + ': ' + price for (i, good, price) in shopGoods[10:]]
    #listTwo.append('\t')
    universal.say('\t'.join(['\n'.join(listOne), '\n'.join(listTwo)]), columnNum=2, justification=0)
    if len(shopGoods) < 10:
        set_commands(['(#) Select item to examine.', '<==Back'])
    else:
        set_commands(['(#) Select item to examine:_', '(Enter)Choose', '<==Back'])
    set_command_interpreter(window_shop_interpreter)

def select_character_to_buy_interpreter(keyEvent):
    if keyEvent.key in NUMBER_KEYS:
        num = int(pygame.key.name(keyEvent.key)) - 1
        if 0 <= num and num < person.get_party().len():
            chosenPerson = person.get_party().get_member(num)
            window_shop_person_chosen()
    elif keyEvent.key == K_BACKSPACE:
        if len(playerGoods) >= 10 and partialNum != '':
            partialNum = partialNum[:-1]
        elif person.get_party().len() == 1:
            shop_mode(doneShoppingLitany=litany)
        else:
            window_shop()

partialNum = ''
def window_shop_interpreter(keyEvent):
    if keyEvent.key in NUMBER_KEYS:
        num = int(pygame.key.name(keyEvent.key))
        if len(shopGoods) < 10:
            if 0 < num and num <= len(shopGoods)+1:
                buy(num)
        else:
            global partialNum
            partialNum += pygame.key.name(keyEvent.key)
            set_commands([''.join(['(#) Select item to examine:', partialNum, '_']), 
                '(Enter)Choose', '<==Back'])
    elif keyEvent.key == K_BACKSPACE and len(shopGoods) >= 10:
        if partialNum:
            partialNum = partialNum[:-1]
            set_commands([''.join(['(#) Select item to examine:', partialNum, '_']), 
                '(Enter)Choose', '<==Back'])
        else:
            shop_mode(doneShoppingLitany=litany)
    elif keyEvent.key == K_BACKSPACE:
        shop_mode(doneShoppingLitany=litany)
    elif keyEvent.key == K_RETURN:
        try:
            num = int(partialNum)
        except ValueError:
            return
        partialNum = ''
        if 0 < num and num <= len(shopGoods)+1:
            buy(num)
        

chosenGood = None
def buy(num):
    global chosenGood
    chosenGood = shopGoods[num-1][ITEM]
    say_title('Coins: ' + str(chosenPerson.coins))
    universal.say(chosenGood.display())
    set_commands(['(Enter) Purchase', '<==Back'])
    set_command_interpreter(confirm_buy_interpreter)

def buy_interpreter(keyEvent):
    """ No longer used. """
    pass
    """
    if keyEvent.key == K_B:
        if chosenPerson.coins >= chosenGood.price:
            universal.say(format_text([['Is', chosenPerson.name, 'sure', heshe(chosenPerson), 
                'would like to purchase', chosenGood.name, '?'],
                [chosenPerson.name, 'has', str(chosenPerson.coins), 'coins, and', 
                    chosenGood.name, 'costs', str(chosenGood.price),' coins.']]))
            set_commands(['(Y)es', '(N)o'])
            set_command_interpreter(confirm_buy_interpreter)
        else:
            universal.say(format_text([chosenPerson.name, "doesn't have enough money.", 
                ["The", chosenGood.name, 
                    "costs", str(chosenGood.price), "coins, but", chosenPerson.name, "only has", 
                    str(universal.state.player.coins), "coins."]]))
            window_shop_person_chosen()
    elif keyEvent.key == K_BACKSPACE:
        window_shop_person_chosen()
    """

def confirm_buy_interpreter(keyEvent):
    if keyEvent.key == K_RETURN:
        if chosenPerson.coins >= chosenGood.price:
            chosenPerson.coins -= chosenGood.price
            shopkeeper.inventory.remove(chosenGood)
            chosenPerson.take_item(chosenGood)
            say_title([chosenPerson.name + "'s", 'Coins: ', str(chosenPerson.coins)])
            if chosenGood.is_equippable():
                if len(person.get_party()) == 1:
                    universal.say(['\nShould', chosenPerson.printedName, 'equip it?'])
                else:
                    universal.say('\nShould someone equip it?')
                set_commands(['(Y)es', '(N)o'])
                set_command_interpreter(equip_interpreter)
            else:
                choose_character_to_carry_item()
        else:
            universal.say([chosenPerson.name, "doesn't have enough money!"])
            acknowledge(window_shop_person_chosen, ())
        set_goods()
    elif keyEvent.key == K_BACKSPACE:
        window_shop_person_chosen()

def equip_interpreter(keyEvent):
    if keyEvent.key == K_y:
        choose_character_to_equip_item()
    elif keyEvent.key == K_n:
        choose_character_to_carry_item()

def choose_character_to_equip_item():
    if len(person.get_party()) == 1:
        universal.say([universal.state.player.name, 'has equipped', chosenGood.name + "."])
        universal.state.player.equip(chosenGood)
        acknowledge(window_shop_person_chosen, ())
    else:
        say_title(['Who should equip', chosenGood.name + "?"])
        universal.say(person.get_party().display())
        if len(person.get_party()) < 10:
            set_commands(['(#) Select party member'])
        else:
            set_commands(['(#) Select party member:_', '(Enter)Done'])
        set_command_interpreter(choose_character_to_equip_item_interpreter)

def choose_character_to_equip_item_interpreter(keyEvent):
    global chosenPerson, partialNum
    if keyEvent.key in NUMBER_KEYS:
        num = int(pygame.key.name(keyEvent.key)) - 1
        if len(person.get_party()) < 10:
            if 0 <= num and num < len(person.get_party()):
                personWhoBoughtGood = chosenPerson
                chosenPerson = person.get_party().get_member(num)
                personWhoBoughtGood.drop_item(chosenGood)
                chosenPerson.take_item(chosenGood)
                chosenPerson.equip(chosenGood)
                universal.say([chosenPerson.name, 'has equipped', chosenGood.name + '.'])
                chosenPerson = personWhoBoughtGood
                acknowledge(window_shop_person_chosen, ())
        else:
            partialNum += pygame.key.name(keyEvent.key)
    elif keyEvent.key == K_BACKSPACE and len(person.get_party()) < 10:
        partialNum = partialNum[:-1]
    elif keyEvent.key == K_RETURN and len(person.get_party()) < 10:
        try:
            num = int(partialNum)
        except ValueError:
            return
        partialNum = ''
        personWhoBoughtGood = chosenPerson
        chosenPerson = person.get_party().get_member(num)
        chosenPerson.equip(chosenGood)
        universal.say([chosenPerson.name, 'has equipped', chosenGood.name + '.'])
        chosenPerson = personWhoBoughtGood
        acknowledge(window_shop_person_chosen, ())

def choose_character_to_carry_item():
    if len(person.get_party()) == 1:
        universal.say([universal.state.player.name, 'is now carrying', chosenGood.name])
        universal.state.player.take_item(chosenGood)
        set_goods()
        acknowledge(window_shop_person_chosen, ())
    else:
        universal.say(['Who should carry', chosenGood.name + "?"])
        universal.say(person.get_party().display())
        set_commands(['(#) Select party member'])
        set_command_interpreter(choose_character_to_carry_item_interpreter)

def choose_character_to_carry_item_interpreter(keyEvent):
    if keyEvent.key in NUMBER_KEYS:
        num = int(pygame.key.name(keyEvent.key)) - 1
        if 0 <= num and num < get_party.len():
            personWhoBoughtGood = chosenPerson
            chosenPerson = person.get_party().get_member(num)
            chosenPerson.take_item(chosenGood)
            universal.say([chosenPerson.name, 'has taken', chosenGood.name + "."])
            chosenPerson = personWhoBoughtGood
            acknowledge(window_shop_person_chosen, ())

def window_sell():
    say_title('Sell')
    global chosenPerson
    if person.get_party().len() == 1:
        chosenPerson = universal.state.player
        window_sell_person_chosen()
    else:
        say_title('Select a party member whose inventory you would like to look at.')
        universal.say(person.get_party().display())
        set_commands(['(#) Select party member', '<==Back'])
        set_command_interpreter(select_party_member_to_sell_interpreter)

def window_sell_person_chosen():
    say_title([chosenPerson.name + "'s", 'Coins: ', str(chosenPerson.coins)])
    playerGoods = zip([str(i) for i in range(1, len(chosenPerson.inventory) + 
            len(chosenPerson.equipmentList)+1)], 
        chosenPerson.inventory + chosenPerson.equipmentList, 
        [str(good.price // 2) + (' E' if good in chosenPerson.equipmentList else '') for good in chosenPerson.inventory + chosenPerson.equipmentList])
    universal.say('\n'.join([str(i) + ". " + good.name + ": " + str(price) 
        for (i, good, price) in playerGoods]))
    if len(playerGoods) < 10:
        set_commands(['(#) Select item to sell.', '<==Back'])
    else:
        partialNum = ''
        set_commands(['(#) Select item to sell:_', '<==Back'])
    set_command_interpreter(window_sell_interpreter)

def select_party_member_to_sell_interpreter(keyEvent):
    if keyEvent.key in NUMBER_KEYS:
        num = int(pygame.key.name(keyEvent.key)) - 1
        if 0 <= num and num < person.get_party().len():
            global chosenPerson, playerGoods
            chosenPerson = person.get_party().get_member(num)
            window_sell_person_chosen()
    elif keyEvent.key == K_BACKSPACE:
        shop_mode(doneShoppingLitany=litany)

def window_sell_interpreter(keyEvent):
    global partialNum
    if keyEvent.key in NUMBER_KEYS:
        if len(playerGoods) < 10:
            num = int(pygame.key.name(keyEvent.key)) - 1
            if 0 <= num and num < len(playerGoods):
                global chosenGood
                chosenGood = chosenPerson.get_item(num)
                confirm_sell()
        else:
            partialNum += pygame.key.name(keyEvent.key)
    elif keyEvent.key == K_BACKSPACE:
        if len(playerGoods) >= 10 and partialNum != '':
            partialNum = partialNum[:-1]
        elif person.get_party().len() == 1:
            shop_mode(doneShoppingLitany=litany)
        else:
            window_sell()
    elif keyEvent.key == K_RETURN:
        try:
            chosenGood = chosenPerson.get_item(int(partialNum)-1)
        except:
            return
        else:
            confirm_sell()

def confirm_sell():
    say_title('Coins: ' + str(chosenPerson.coins))
    universal.say(chosenGood.display())
    set_commands([' '.join(['Sell for', str(chosenGood.price // 2), 
        ('coins' if chosenGood.price // 2 > 1 else 'coin') + "?", '(Y/N)'])])
    set_command_interpreter(confirm_sell_interpreter)

def confirm_sell_interpreter(keyEvent):
    if keyEvent.key == K_y:
        universal.say([chosenPerson.name, 'has sold', chosenGood.name, 'for', str(chosenGood.price // 2), 
                'coins.'])
        success = chosenPerson.drop_item(chosenGood)
        if success:
            chosenPerson.coins += chosenGood.price // 2
            shopkeeper.take_item(chosenGood)
        set_goods()
        acknowledge(window_sell_person_chosen, ())
    elif keyEvent.key == K_n:
        window_sell_person_chosen()
