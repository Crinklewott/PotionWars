"""
Copyright 2014, 2015 Andrew Russell

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
        set_commands(['(#) Select a character.', '<==Back'])
        set_command_interpreter(select_character_to_buy_interpreter)

def window_shop_person_chosen():
    say_title('Matrons: ' + str(chosenPerson.coins))
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
    global chosenPerson
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
    say_title('Matrons: ' + str(chosenPerson.coins))
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
            say_title([chosenPerson.name + "'s", 'Matrons: ', str(chosenPerson.coins)])
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
        if 0 <= num and num < len(universal.state.party):
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
    say_title([chosenPerson.name + "'s", 'Matrons: ', str(chosenPerson.coins)])
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
            set_commands(['(#) Select item to sell:' + str(partialNum) + '_', '<==Back'])
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
        except IndexError:
            return
        else:
            confirm_sell()

def confirm_sell():
    say_title('Matrons: ' + str(chosenPerson.coins))
    universal.say(chosenGood.display())
    set_commands([' '.join(['Sell for', str(chosenGood.price // 2), 
        ('matrons' if chosenGood.price // 2 > 1 else 'matron') + "?", '(Y/N)'])])
    global partialNum
    partialNum = ''
    set_command_interpreter(confirm_sell_interpreter)

def confirm_sell_interpreter(keyEvent):
    if keyEvent.key == K_y:
        universal.say([chosenPerson.name, 'has sold', chosenGood.name, 'for', str(chosenGood.price // 2), 
                'matrons.'])
        success = chosenPerson.drop_item(chosenGood)
        if success:
            chosenPerson.coins += chosenGood.price // 2
            shopkeeper.take_item(chosenGood)
        set_goods()
        acknowledge(window_sell_person_chosen, ())
    elif keyEvent.key == K_n:
        window_sell_person_chosen()

gemList = []

def done_shopping():
    if litany is None:
        townmode.town_mode()
    else:
        shopkeeper.litany = litany
        conversation.converse_with(shopkeeper, townmode.town_mode)

def select_gem(shopkeeperIn=None, doneShoppingLitany=None):
    global partialNum
    if sum(person.coins for person in universal.state.party) < 30 and (
            universal.state.enchantmentFreebies == 0):
        universal.say("You don't have enough money to enchant anything!")
        universal.acknowledge(done_shopping, ())
        return
    universal.say_title("Select Enhancement Gem")
    global gemList, litany, shopkeeper
    shopkeeper = shopkeeperIn
    litany = doneShoppingLitany
    gemList = []
    for person in universal.state.party:
        gemList.extend([(person, item) for item in person.get_inventory() if 
            hasattr(item, "enchantmentType")])
        gemStrings = [''.join([person.name, ": ", item.name]) for person, item in gemList]
    universal.say('\n'.join(gemStrings))
    universal.set_commands(["(#) Select Gem: " + str(partialNum) + '_', "<==Back"])
    universal.set_command_interpreter(select_gem_interpreter)
    partialNum = ''
        

chosenPersonGem = None
def select_gem_interpreter(keyEvent, testing=False):
    global partialNum, chosenPersonGem
    if keyEvent.key in NUMBER_KEYS:
        if len(playerGoods) < 10:
            num = int(pygame.key.name(keyEvent.key)) - 1
            if 0 <= num and num < len(playerGoods):
                global chosenPersonGem
                chosenPersonGem = gemList[num]
                if not testing:
                    select_equipment()
        else:
            partialNum += pygame.key.name(keyEvent.key)
            set_commands(['(#) Select Gem:' + str(partialNum) + '_', '<==Back'])
    elif keyEvent.key == K_BACKSPACE:
        if len(playerGoods) >= 10 and partialNum != '':
            partialNum = partialNum[:-1]
        elif litany is None:
            townmode.town_mode()
        else:
            shopkeeper.litany = litany
            conversation.converse_with(shopkeeper, townmode.town_mode)
    elif keyEvent.key == K_RETURN:
        if len(playerGoods) >= 10 and partialNum:
            try:
                chosenPersonGem = gemList[int(partialNum)-1]
            except IndexError:
                return
            else:
                if not testing:
                    select_equipment()

equipmentList = []
def select_equipment():
    universal.say_title("Select Equipment to Enchant:")
    global equipmentList
    global partialNum
    equipmentList = []
    partialNum = ''
    for person in universal.state.party:
        equipmentList.extend([(person, equipment) for equipment in person.equipmentList
             if not items.is_empty_item(equipment) and 
            not items.is_pajamas(equipment)])
    personEquipmentStrings = [''.join([person.printedName, ": ", equipment.name]) for
            person, equipment in equipmentList]
    universal.say('\n'.join(universal.numbered_list(personEquipmentStrings)))
    universal.set_commands(["(#) Select Equipment: " + str(partialNum) + '_', "<==Back"])
    universal.set_command_interpreter(select_equipment_interpreter)

chosenEquipment = None
def select_equipment_interpreter(keyEvent, testing=False):
    global partialNum, chosenEquipment
    if keyEvent.key in NUMBER_KEYS:
        if len(playerGoods) < 10:
            num = int(pygame.key.name(keyEvent.key)) - 1
            if 0 <= num and num < len(playerGoods):
                global chosenEquipment
                chosenEquipment = equipmentList[num][1]
                gem = chosenPersonGem[1]
                maxEnchantment = chosenEquipment.maxEnchantment
                enchantmentLevel = chosenEquipment.enchantment_level()
                if maxEnchantment - enchantmentLevel < gem.cost:
                    universal.say(' '.join(["Cannot enchant", chosenEquipment.name, "with", 
                        gem.name + ".", gem.name, "requires", str(gem.cost), "enchantment points,",
                        "but", chosenEquipment.name, "only has", str(maxEnchantment - 
                            enchantmentLevel), "points available."]))
                    universal.acknowledge(select_equipment, ())
                else:
                    if not testing:
                        confirm_enchantment()
        else:
            partialNum += pygame.key.name(keyEvent.key)
            set_commands(['(#) Select Equipment:' + str(partialNum) + '_', '<==Back'])
    elif keyEvent.key == K_BACKSPACE:
        if len(playerGoods) >= 10 and partialNum != '':
            partialNum = partialNum[:-1]
        elif litany is None:
            townmode.town_mode()
        else:
            shopkeeper.litany = litany
            conversation.converse_with(shopkeeper, townmode.town_mode)
    elif keyEvent.key == K_RETURN:
        if len(playerGoods) < 10 and partialNum:
            try:
                chosenEquipment = equipmentList[int(partialNum)-1][1]
            except IndexError:
                return
            else:
                gem = chosenPersonGem[1]
                maxEnchantment = chosenEquipment.maxEnchantment
                enchantmentLevel = chosenEquipment.enchantment_level()
                if maxEnchantment - enchantmentLevel < gem.cost:
                    universal.say(' '.join(["Cannot enchant", chosenEquipment.name, "with", 
                        gem.name + ".", gem.name, "requires", str(gem.cost), "enchantment points,",
                        "but", chosenEquipment.name, "only has", str(maxEnchantment - 
                            enchantmentLevel), "points available."]))
                    universal.acknowledge(select_equipment, ())
                else:
                    if not testing:
                        confirm_enchantment()

def confirm_enchantment():
    universal.say_title("Confirm:")
    universal.say(' '.join(["Enchant", chosenEquipment.name, "with", 
        chosenPersonGem[1].name + "?"]))
    set_commands(["(Enter) Enchant", "<==Back", "(Esc) Cancel"])
    set_command_interpreter(confirm_enchantment_interpreter)

def confirm_enchantment_interpreter(keyEvent):
    if keyEvent.key == K_RETURN:
        enchant_equipment()
    elif keyEvent.key == K_ESCAPE:
        select_gem()
    elif keyEvent.key == K_BACKSPACE:
        select_equipment()

def enchant_equipment():
    gem = chosenPersonGem[1]
    enchantment = gem.enchantmentType()
    chosenEquipment.add_enchantment(enchantment)
    chosenPersonGem[0].drop_item(gem)
    universal.say( ' '.join([chosenEquipment.name, "has been enchanted with", gem.name + "."]))
    universal.acknowledge(select_gem, (shopkeeper, litany))
    if universal.state.enchantmentFreebies > 0:
        universal.state.enchantmentFreebies -= 1
    else:
        assert sum(person.coins for person in universal.state.party) >= 30, (
            "We shouldn't reach this point without more than 30 coins:%d" % (
                sum(person.coins for person in universal.state.party),))
        totalToPay = 30
        while totalToPay:
            cost = totalToPay // len(universal.state.party)
            for person in universal.state.party:
                if person.coins >= cost:
                    person.coins -= cost
                    totalToPay -= cost
        
            



