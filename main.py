#!/usr/bin/env python3
  
import decks
import random
from art import logo

def check_aces(player_data):
    check_aces = [ace for ace in player_data["Hand"] if "Ace of" in ace]
    for check_ace in check_aces:
        if check_ace not in player_data["Aces_in_hand"] and player_data["Score"] > 21:
            player_data["Score"] -= 10
            player_data["Aces_in_hand"].append(check_ace)
    return player_data

def add_card(player_data, card):
    player_data["Hand"].append(card)
    player_data["Score"] += decks.standard[card]
    player_data = check_aces(player_data)
    return player_data

def create_deck(base_deck):
    deck = []
    for card in decks.standard:
        deck.append(card)
    return random.sample(deck, len(deck))

def print_hands(deck_data, turn):
    print("\nYour Cards: " + ', '.join(deck_data['Player']['Hand']))
    print("Current Score: " + str(deck_data['Player']['Score']))
    if turn == "Player":
        print("Dealer's hand: Facedown Card, " + ', '.join(deck_data['Dealer']['Hand'][1:]))
        print("Dealer's Score: " + str(deck_data['Dealer']['Shown_Score']))
    elif turn == "Dealer":
        print("Dealer's hand: " + ', '.join(deck_data['Dealer']['Hand']))
        print("Dealer's Score: " + str(deck_data['Dealer']['Score']))


def blackjack(dealers_deck): 
    gamedata = {
        "Player": {
            "Hand": [dealers_deck[0], dealers_deck[2]],
            "Score": decks.standard[dealers_deck[0]] + decks.standard[dealers_deck[2]],
            "Aces_in_hand": [] 
        },
        "Dealer": {
            "Hand": [dealers_deck[1], dealers_deck[3]],
            "Score": decks.standard[dealers_deck[1]] + decks.standard[dealers_deck[3]],
            "Shown_Score": decks.standard[dealers_deck[3]],
            "Aces_in_hand": [] 
        }
    }
    dealers_deck = dealers_deck[4:]
    whos_turn = "Player"

    print(logo)
    # Turn Logic
    while whos_turn == "Player" or whos_turn == "Dealer":
        gamedata[whos_turn] = check_aces(gamedata[whos_turn])
        print_hands(gamedata, whos_turn)
        if gamedata[whos_turn]["Score"] > 21:
            print(f"The {whos_turn} busted. Game Over.")
            whos_turn = "Game Over"
        elif whos_turn == "Player":
            player_choice = input("Would you like another card? 'y' or 'n': ").lower()
            if player_choice == 'y':
                gamedata[whos_turn] = add_card(gamedata[whos_turn], dealers_deck[0])
                dealers_deck = dealers_deck[1:]
            elif player_choice == 'n':
                whos_turn = "Dealer"
        elif whos_turn == "Dealer":
            if gamedata[whos_turn]['Score'] < 17:
                print("The dealer takes a card.")
                gamedata[whos_turn] = add_card(gamedata[whos_turn], dealers_deck[0])
                dealers_deck = dealers_deck[1:]
            else:
                print("The dealer stands.")
                whos_turn = ""
    
    if whos_turn != "Game Over":
        if gamedata["Player"]["Score"] > gamedata["Dealer"]["Score"]:
            print("Congrats the player wins!")
        elif gamedata["Player"]["Score"] < gamedata["Dealer"]["Score"]:
            print("Game over, the house wins.")
        elif gamedata["Player"]["Score"] == gamedata["Dealer"]["Score"]:
            print("The game ends in a push resulting in a tie.")
    another_game = input("Would you like to play another game? 'y' or 'n': ").lower()
    if another_game == 'y':
        blackjack(create_deck(decks.standard))

blackjack(create_deck(decks.standard))