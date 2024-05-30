import telebot
import random
import time
from telebot import types

bot = telebot.TeleBot('6917149428:AAG8uOv3QH4ldh59WFyuUX6qIgoCSnwY-zw')

class Card:

    numsList = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A']
    mastList = ['❤️', '♠️', '♣️', '♦️']

    def __init__(self, num=None, mast=None):

        self.num = num if num else random.choice(Card.numsList)
        self.mast = mast if mast else random.choice(Card.mastList)

#___function to calculate the value of the card___#
    def what_value(self, ace_equal_1, ace_equal_11):

        if self.num in ('J', 'Q', 'K'):
            ace_equal_1 = 10
            ace_equal_11 = 10

        elif isinstance(self.num, int):
            ace_equal_1 = self.num
            ace_equal_11 = self.num

        elif self.num == 'A':
            ace_equal_1 = 1
            ace_equal_11 = 11

        return ace_equal_1, ace_equal_11

#___Player's score___#
class Player:

    def __init__(self):
        self.pl, self.pl_a = 0, 0

    def all_add(self, p, o):

        self.pl += p
        self.pl_a += o

        if self.pl_a > 21:
            self.pl_a = self.pl + 10

            if self.pl_a > 21:
                self.pl_a = self.pl

        return self.pl, self.pl_a

#___Dealer's score___#
class Dealer:

    def __init__(self):
        self.dl, self.dl_a = 0, 0

    def all_add(self, r, e):

        self.dl += r
        self.dl_a += e

        if self.dl_a > 21:
            self.dl_a = self.dl + 10

            if self.dl_a > 21:
                self.dl_a = self.dl

        return self.dl, self.dl_a

def dealer_take_card():
    c = Card()
    q, w = c.what_value(d.dl, d.dl_a)
    d.all_add(q, w)
    return c.num, c.mast

def player_take_card():
    c = Card()
    q, w = c.what_value(p.pl, p.pl_a)
    p.all_add(q, w)
    return c.num, c.mast


def handle_end_game(message, result):

    if result == "win":
        bot.send_message(message.chat.id, "You win")

    elif result == "draw":
        bot.send_message(message.chat.id, "Draw")

    else:
        bot.send_message(message.chat.id, "You lose")

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item = types.KeyboardButton("🎲 let's start")
    markup.add(item)
    bot.send_message(message.chat.id, "Start a new game?", reply_markup=markup)

d = Dealer()
dealers_cards = ""
p = Player()

@bot.message_handler(commands=['start'])
def start(message):

#___Creating buttons to help and start___#
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("🎲 let's start")
    item2 = types.KeyboardButton("😊 How to play?")
    markup.add(item1, item2)

#___First message___#
    bot.send_message(message.chat.id,
                     "Hello, {0.first_name}!\nI'm - {1.first_name}, I exist to spend time and get some experience.".format(
                         message.from_user, bot.get_me()), reply_markup=markup)

@bot.message_handler(content_types=['text'])
def first_cards(message):
    global dealers_cards, d, p
    if message.chat.type == 'private':
        if message.text == "🎲 let's start":

            dealers_cards = ""
            d = Dealer()
            p = Player()

        #___first Player's and Dealer's cards___#
            a, b = dealer_take_card()
            c, h = player_take_card()
            e, f = player_take_card()
            dealers_cards += f"{str(a)}{str(b)}"

        #___buttons to take(or not) next card___#
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("YES")
            item2 = types.KeyboardButton("NO")
            markup.add(item1, item2)

            bot.send_message(message.chat.id, f"""Dealer has: {dealers_cards}
You have: {c}{h},  {e}{f}
One more?""", reply_markup=markup)

        #___Explanation of the game___#
        elif message.text == "😊 How to play?":

            bot.send_message(message.chat.id, """<em><b>Goal🛑:</b></em> Get a hand value as close to 21 as possible without exceeding it.


<em><b>Card Values🃏:</b></em> Number cards are worth their face value, face cards (King, Queen, Jack) are worth 10, and Aces can be worth 1 or 11.


<em><b>Starting the Game💣:</b></em> Each player is dealt two cards, and the dealer also gets two cards, with one card face up.


<em><b>Player's Turn🥸:</b></em> Players can choose to "hit" (take another card) or "stand" (keep their current hand). Players can hit as many times as they want but must not exceed 21.


<em><b>Dealer's Turn🤵‍♂️:</b></em> After all players have finished, the dealer reveals their hidden card and must hit until their hand value is 17 or higher.


<em><b>Winning🥂:</b></em> If a player's hand is closer to 21 than the dealer's, or the dealer busts (exceeds 21), the player wins. If the player's hand exceeds 21, they bust and lose. If the dealer and player have the same value, it's a draw.

<b>GOOD LUCK!😇😇😇</b>""",
                             parse_mode='HTML')


        elif message.text == "YES":
            c, l = player_take_card()
            bot.send_message(message.chat.id, f"{c}{l}")

            if p.pl > 21:
                p.pl, p.pl_a = 0, 0
                handle_end_game(message, "lose")

        elif message.text == "NO":
            while d.dl < 21 and d.dl_a < 17:
                g, h = dealer_take_card()
                dealers_cards += f", {str(g)}{str(h)}"

            bot.send_message(message.chat.id, f"Dealer has: {dealers_cards}")

            if d.dl > 21:
                handle_end_game(message, "win")

            else:
                if p.pl_a > d.dl_a:
                    handle_end_game(message, "win")

                elif p.pl_a == d.dl_a:
                    handle_end_game(message, "draw")

                elif p.pl_a < d.dl_a:
                    handle_end_game(message, "lose")

        else:
            bot.send_message(message.chat.id, 'Please, choose just one option😢')

bot.polling(none_stop=True)