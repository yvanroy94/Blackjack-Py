import random
import time


stats = open("stats.txt", "r")
cash = int(stats.read())
stats.close()


def calc(dealer_turn):

    total = 0

    if dealer_turn is False:
        list_cards = player_cards
    else:
        list_cards = dealer_cards

    for card in list_cards:
        if isinstance(card, int):
            total += card
        else:
            if card != "A":
                total += 10
            else:
                total += 11

    for card in list_cards:
        if total > 21:
            if card == "A":
                total -= 10

    return total


playing = True


while playing is True:

    wager = None
    betting = True

    deck = ["A", 2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K"] * 4

    player_cards = [random.choice(deck), random.choice(deck)]
    player_total = calc(False)
    player_dead = False
    player_stop = False
    player_win = False

    dealer_cards = [random.choice(deck)]
    dealer_total = calc(True)
    dealer_dead = False
    dealer_stop = False

    while betting is True:
        try:
            wager = int(input("\nPlease pass an integer amount to bet:"))
        except:
            print("\nThat is not a valid integer bet. Please try again.")
        else:
            break


    while player_stop is False and player_dead is False:

        print("\nDealer has [", *dealer_cards, "] =>", dealer_total)
        print("You have [", *player_cards, "] =>", player_total)


        if player_total == 21 and len(player_cards) == 2:
            player_win = True
            break

        choice = input("\nYou you want to (s)tand or (h)it?")

        if choice == "h":
            player_cards.append(random.choice(deck))
        elif choice == "s":
             player_stop = True


        player_total = calc(False)

        if player_total > 21:
            player_dead = True
            break


    if player_dead is False and player_win is False:

        while dealer_dead is False and dealer_stop is False:

            print("\nThe Dealer draws another card..")
            dealer_cards.append(random.choice(deck))
            time.sleep(1.5)

            dealer_total = calc(True)

            print("\nDealer has [", *dealer_cards, "] =>", dealer_total)
            print("You have [", *player_cards, "] =>", player_total)


            dealer_total = calc(True)

            if dealer_total > 21:
                dealer_dead = True

            if dealer_total >= 17:
                dealer_stop = True


    if player_win is False:

        if player_dead is False and dealer_dead is False:

            if player_total == dealer_total:
                print("\nDealer has [", *dealer_cards, "] =>", dealer_total, "/ You have [", *player_cards, "] =>", player_total, ", it's a draw! You get your bet back!\nYou currently have", cash, "bits!")
            elif player_total < dealer_total:
                cash -= wager
                print("\nDealer has [", *dealer_cards, "] =>", dealer_total, "/ You have [", *player_cards, "] =>", player_total, ", you lose!\nYou currently have", cash, "bits!")
            else:
                cash += wager
                print("\nDealer has [", *dealer_cards, "] =>", dealer_total, "/ You have [", *player_cards, "] =>", player_total, ", you win!\nYou currently have", cash, "bits!")

        elif dealer_dead is True:
            cash += wager
            print("\nThe dealer took one card too many and now has [", *dealer_cards, "] =>", dealer_total, ", you win!\nYou currently have", cash, "bits!")
        else:
            cash -= wager
            print("\nYou took one card too many and now have [", *player_cards, "] =>", player_total, ", you lose!\nYou currently have", cash, "bits!")

    else:
        cash += wager*2
        print("\nCongratulations, you hit blackjack and double your profit!\nYou currently have", cash, "bits!")

    stats = open("stats.txt", "w")
    stats.write(str(cash))
    stats.close()

    wager = None
    betting = True


    choice = input("\nThank you for playing! If you want to play another hand, press (enter). To quit, pass (x).")

    if choice == "x":
        break
