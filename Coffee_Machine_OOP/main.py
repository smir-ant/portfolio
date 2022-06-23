from menu import Menu
from coffee_maker import CoffeeMaker
from money_machine import MoneyMachine

money_machine = MoneyMachine()
coffee_maker = CoffeeMaker()
menu = Menu()

is_on = True

while is_on:
    options = menu.get_items()
    choice = input(f'Choice one of: {options}').lower()
    if choice == 'off':
        is_on = False
    elif choice == 'report':
        coffee_maker.report()
        money_machine.report()
    else:
        drink = menu.find_drink(choice)
        is_resources_enough = coffee_maker.is_resource_sufficient(drink)
        is_payment_succesfull = money_machine.make_payment(drink.cost)
        if is_payment_succesfull and is_resources_enough:
            coffee_maker.make_coffee(drink)