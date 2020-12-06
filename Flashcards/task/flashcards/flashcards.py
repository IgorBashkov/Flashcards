from random import choice
from io import StringIO
import argparse


class FlashCard:
    cards = []
    straight_dict = {}
    reverse_dict = {}
    run = True
    log = StringIO()
    save_exit = None

    def __init__(self, term, definition, errors=0):
        self.term = term
        self.definition = definition
        self.errors = int(errors)
        FlashCard.cards.append(self)
        FlashCard.straight_dict[term] = definition
        FlashCard.reverse_dict[definition] = term

    def check(self, definition):
        if self.definition == definition:
            res = 'Correct!'
        else:
            self.errors += 1
            res = f'Wrong. The right answer is "{self.definition}"'
            if definition in self.reverse_dict:
                res += f', but your definition is correct for "{self.reverse_dict[definition]}"'
            res += '.'
        FlashCard.log.write(res + '\n')
        print(res)

    @classmethod
    def get_card(cls, term):
        for card in cls.cards:
            if card.term == term:
                return card
        return None

    @classmethod
    def read_from_file(cls, file_name=None):
        if file_name is None:
            text = 'File name:\n'
            file_name = input(text)
            cls.log.write(text)
            cls.log.write(file_name + '\n')
        try:
            with open(file_name) as file:
                for n, row in enumerate(file):
                    r = row.strip().split('|')
                    if r[0] in cls.straight_dict:
                        cls.delete_card(r[0])
                    cls(r[0], r[1], r[2])
                text = f'{n + 1} cards have been loaded.'
                print(text)
                cls.log.write(text + '\n')
        except OSError:
            text = 'File not found.'
            cls.log.write(text + '\n')
            print(text)

    def __str__(self):
        return f'{self.term}|{self.definition}|{self.errors}\n'

    @classmethod
    def write_to_file(cls, file_name=None):
        if file_name is None:
            text = 'File name:\n'
            cls.log.write(text)
            file_name = input(text)
            cls.log.write(file_name + '\n')
        with open(file_name, 'w') as file:
            n = -1
            for n, card in enumerate(cls.cards):
                file.write(str(card))
            text = f'{n + 1} cards have been saved.'
            cls.log.write(text + '\n')
            print(text)

    @classmethod
    def ask_number_cards(cls):
        text = 'How many times to ask?\n'
        cls.log.write(text)
        number = int(input(text))
        cls.log.write(str(number) + '\n')
        for _ in range(number):
            card = choice(cls.cards)
            text = f'Print the definition of "{card.term}":\n'
            cls.log.write(text)
            text = input(text)
            cls.log.write(text + '\n')
            card.check(text)

    @classmethod
    def delete_card(cls, t=None):
        if t is None:
            text = 'Which card?\n'
            cls.log.write(text)
            term = input(text)
        else:
            term = t
        card = cls.get_card(term)
        if card is not None:
            cls.straight_dict.pop(card.term)
            cls.reverse_dict.pop(card.definition)
            cls.cards.remove(card)
            if not t:
                text = 'The card has been removed.'
                cls.log.write(text + '\n')
                print(text)
        else:
            text = f'Can\'t remove "{term}": there is no such card.'
            cls.log.write(text + '\n')
            print(text)

    @classmethod
    def exit(cls):
        cls.run = False
        if cls.save_exit is not None:
            cls.write_to_file(cls.save_exit)
        print('Bye bye!')

    @classmethod
    def from_input(cls):
        text = 'The card:'
        cls.log.write(text + '\n')
        print(text)
        while True:
            term = input()
            if term in cls.straight_dict:
                text = f'The term "{term}" already exists. Try again:'
                cls.log.write(text + '\n')
                print(text)
            else:
                break
        text = 'The definition of the card:'
        cls.log.write(text + '\n')
        print(text)
        while True:
            definition = input()
            cls.log.write(definition + '\n')
            if definition in cls.reverse_dict:
                text = f'The definition "{definition}" already exists. Try again:'
                cls.log.write(text + '\n')
                print(text)
            else:
                break
        cls(term, definition)
        text = f'The pair ("{term}":"{definition}") has been added.'
        cls.log.write(text + '\n')
        print(text)

    @classmethod
    def print_hardest_card(cls):
        if cls.cards:
            cls.cards.sort(key=lambda x: x.errors, reverse=True)
            ers = cls.cards[0:1]
            if ers[0].errors:
                for card in cls.cards[1:]:
                    if card.errors == ers[0].errors:
                        ers.append(card)
                    else:
                        break
                # card_form = 'card is ' if len(ers) > 1 else 'cards are '
                text = 'The hardest card is ' + \
                       ', '.join([f'"{card.term}"' for card in ers]) + \
                       f'. You have {len(ers) * ers[0].errors} errors answering it.'
                cls.log.write(text + '\n')
                print(text)
                return
        text = 'There are no cards with errors.'
        cls.log.write(text + '\n')
        print(text)

    @classmethod
    def create_log(cls):
        text = 'File name:\n'
        cls.log.write(text)
        file_name = input(text)
        cls.log.write(file_name + '\n')
        with open(file_name, 'w') as file:
            file.write(cls.log.getvalue())
        text = 'The log has been saved'
        cls.log.write(text + '\n')
        print(text)

    @classmethod
    def reset_card_errors(cls):
        for card in cls.cards:
            card.errors = 0
        text = 'Card statistics have been reset.'
        cls.log.write(text + '\n')
        print(text)

    @classmethod
    def main_menu(cls):
        menu = {
            'add': cls.from_input,
            'remove': cls.delete_card,
            'import': cls.read_from_file,
            'export': cls.write_to_file,
            'ask': cls.ask_number_cards,
            'exit': cls.exit,
            'log': cls.create_log,
            'hardest card': cls.print_hardest_card,
            'reset stats': cls.reset_card_errors,
        }
        while cls.run:
            text = f'Input the action ({", ".join(menu)}):'
            cls.log.write(text + '\n')
            print(text)
            inp = input()
            cls.log.write(inp + '\n')
            menu[inp]()
            print()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--import_from')
    parser.add_argument('--export_to')
    args = parser.parse_args()
    if args.import_from:
        FlashCard.read_from_file(args.import_from)
    if args.export_to:
        FlashCard.save_exit = args.export_to
    FlashCard.main_menu()


if __name__ == '__main__':
    main()
