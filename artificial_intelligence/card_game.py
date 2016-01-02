__author__ = 'sunary'


import random
import math


class Card():
    NAME_SUITS = ['Spades', 'Clubs', 'Diamonds', 'Hearts']
    NAME_RANKS = ['3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', '2']

    def __init__(self, value):
        self.suit = value % 4
        self.rank = value / 4

    def get_score(self, subtract_cards):
        same_suit = 0
        num_card_lager = 0

        if self.rank == 12:
            for i in range(len(subtract_cards)):
                if subtract_cards[i]:
                    same_suit += 1
                    if int(self) > i:
                        num_card_lager += 1
        else:
            for i in range(len(subtract_cards)):
                if i / 4 == 12:
                    if subtract_cards[i]:
                        same_suit += 1
                elif subtract_cards[i] and (int(self) % 4 == i % 4):
                    same_suit += 1
                    if int(self) > i:
                        num_card_lager += 1

        return same_suit if same_suit == 0 else num_card_lager * 1.0/same_suit

    def __int__(self):
        return self.rank * 4 + self.suit

    def __str__(self):
        return self.NAME_RANKS[self.rank] + '.' + self.NAME_SUITS[self.suit]


class Group():

    def __init__(self, cards, straight):
        self.cards = cards
        self.straight = straight

    def get_probability(self, players_cards):
        if sum(players_cards) < len(self.cards):
            return 0

        prob = 0
        for p in players_cards:
            prob_card = 1.0
            for i in range(1, (len(self.cards))):
                prob_card *= (p - i)*1.0 /(sum(players_cards) - i)

            prob += prob_card
        return 1 if prob > 1 else prob

    def get_score(self, subtract_cards):
        same_form = 0
        form_larger = 0

        if self.straight:
            for i in range(0, 12 - len(self.cards)):
                and_cards = True
                for j in range(len(self.cards)):
                    and_cards = and_cards and subtract_cards[(i + j)* 4 + self.cards[j].suit]

                if and_cards:
                    same_form += 1
                    if self.cards[0].rank > i:
                        form_larger += 1
        else:
            for i in range(0, 12):
                and_cards = True
                for j in range(len(self.cards)):
                    and_cards = and_cards and subtract_cards[i* 4 + self.cards[j].suit]

                if and_cards:
                    same_form += 1
                    if self.cards[0].rank > i:
                        form_larger += 1

            count_rank_2 = 0
            for j in range(12*4, len(subtract_cards)):
                if subtract_cards[j]:
                    count_rank_2 += 1

            if count_rank_2 >= len(self.cards):
                same_form += math.factorial(count_rank_2)/(math.factorial(count_rank_2 - len(self.cards)) * math.factorial(len(self.cards)))

        return same_form if same_form == 0 else form_larger * 1.0/same_form

    def __str__(self):
        text = ''
        for c in self.cards:
            text += str(c) + ' '

        return  '[' + text[ :-1] + ']'


class Player():

    def __init__(self, value_cards):
        self.cards = [Card(v) for v in value_cards]
        self.sort()
        self.check_group()
        self.distinct_card()

    def sort(self):
        for i in range(len(self.cards) - 1):
            for j in range(i + 1, len(self.cards)):
                if int(self.cards[i]) > int(self.cards[j]):
                    temp = self.cards[i]
                    self.cards[i] = self.cards[j]
                    self.cards[j] = temp

    def check_group(self):
        self.group_straight = []
        self.group_same_rank = []

        straigth_cards = [self.cards[0]]
        same_rank_cards = [self.cards[0]]
        for c in self.cards[1: ]:
            if c.rank != 12 and \
                    c.suit == straigth_cards[-1].suit and c.rank == straigth_cards[-1].rank + 1:
                straigth_cards.append(c)
            else:
                if len(straigth_cards) >= 3:
                    self.group_straight.append(Group(straigth_cards, True))

                straigth_cards = [c]

            if c.rank == same_rank_cards[-1].rank:
                same_rank_cards.append(c)
            else:
                if len(same_rank_cards) == 2:
                    if (same_rank_cards[0].suit == 0 and same_rank_cards[1].suit == 1) or \
                        (same_rank_cards[0].suit == 2 and same_rank_cards[1].suit == 3):
                        self.group_same_rank.append(Group(same_rank_cards, False))
                elif len(same_rank_cards) >= 3:
                    self.group_same_rank.append(Group(same_rank_cards, False))

                same_rank_cards = [c]

            if c == self.cards[-1]:
                if len(straigth_cards) >= 3:
                    self.group_straight.append(Group(straigth_cards, True))

                if len(same_rank_cards) == 2:
                    if (same_rank_cards[0].suit == 0 and same_rank_cards[1].suit == 1) or \
                            (same_rank_cards[0].suit == 2 and same_rank_cards[1].suit == 3):
                        self.group_same_rank.append(Group(same_rank_cards, False))
                elif len(same_rank_cards) >= 3:
                    self.group_same_rank.append(Group(same_rank_cards, False))

    def distinct_card(self):
        for gr_straight in self.group_straight:
            for gr_same_rank in self.group_same_rank:
                i = j = 0
                while i < len(gr_straight.cards):
                    while j < len(gr_same_rank.cards):
                        if int(gr_straight.cards[i]) == int(gr_same_rank.cards[j]):
                            if len(gr_straight.cards) > len(gr_same_rank.cards):
                                self.group_same_rank.remove(gr_same_rank)
                            else:
                                self.group_straight.remove(gr_straight)
                            i = len(gr_straight.cards)
                            j = len(gr_same_rank.cards)

                        j += 1
                    i += 1

    def mine_cards(self):
        mine_cards = [False for _ in range(52)]
        for c in self.cards:
            mine_cards[int(c)] = True

        return mine_cards

    def get_score(self, remain_cards, cards=None):
        cards = cards or self.cards
        mine_cards = self.mine_cards()
        subtract_cards = [((not mine_cards[i]) and remain_cards[i]) for i in range(len(remain_cards))]

        score = 0
        num_group = 0
        for c in cards:
            exist_in_group = False
            for gr in self.group_straight:
                if c in gr.cards:
                    exist_in_group = True
            for gr in self.group_same_rank:
                if c in gr.cards:
                    exist_in_group = True

            if not exist_in_group:
                num_group += 1
                score += c.get_score(subtract_cards)

        players_cards = [13, 13, 13]
        for gr in self.group_straight:
            num_group += 1
            score += gr.get_score(subtract_cards)/(gr.get_probability(players_cards) **0.5)

        for gr in self.group_same_rank:
            num_group += 1
            score += gr.get_score(subtract_cards)/(gr.get_probability(players_cards) **0.5)

        return num_group, score/num_group

    def holder(self, remain_cards):
        pass

    def guest(self, remain_cards):
        pass

    def __str__(self):
        text = ''
        for c in self.cards:
            text += str(c) + ' '

        for gr in self.group_straight:
            text += str(gr) + ' '
        for gr in self.group_same_rank:
            text += str(gr) + ' '

        return text


class GameCard():

    def __init__(self):
        self.player = []

    def start(self):
        self.shuffle()

        for p in self.player:
            print p
            print p.get_score(self.remain_cards)

    def shuffle(self):
        self.remain_cards = [True for _ in range(52)]
        self.cards = [x for x in range(52)]
        random.shuffle(self.cards)

        self.player = [Player(self.cards[i * 13: (i + 1) * 13]) for i in range(4)]


if __name__ == '__main__':
    game_card = GameCard()
    game_card.start()

    card1 = Card(8)
    card2 = Card(10)
    print card1.get_score([True for _ in range(52)])
    print card2.get_score([True for _ in range(52)])

    group = Group([Card(8), Card(9)], False)
    print group.get_probability([13, 13, 13])
    print group.get_score([True for _ in range(52)])