from typing import List, Callable
from card import Card
import evaluator
import pickle

def read_file(filename: str) -> List[List]:
    # Read in the file and return the list of lists
    # where each list is a line in the file
    # This also splits each line based on the tab delimiter
    with open(filename) as f:
        file = f.read().splitlines()
    
    return [line.split('\t') for line in file]

def filter_lines_by_class(lines: List[List], class_names: List[str]) -> List[List]:
    # Filter the list of lists by the class names
    # This will return a list of lists where each list
    # is a line in the file that has the class names
    return [line for line in lines[1:] if line[-1] in class_names]

def make_dict(lines: List[List], func: Callable) -> dict:
    # This function will create a dictionary where the input keys are
    # some aggregation of the cards and the values are the values for the
    # equivalence class
    return {func(cl): value for (value, cl) in [process_line(line) for line in lines]}

def process_line(line: List[str]) -> (int, List[Card]):
    # This function takes the value of the line and 
    # generates a list of cards. Both are returned
    value = int(line[0])
    card_list = eval(line[5])
    list_cards = [Card(card, 's') for card in card_list]
    return (value, list_cards)

def pickle_dict(filename: str, dict: dict):
    # This function will pickle the dictionary
    with open(filename, 'wb') as f:
        pickle.dump(dict, f, protocol=pickle.HIGHEST_PROTOCOL)

if __name__ == "__main__":
    filelines = read_file('equivalence.tsv')

    flush_lines = filter_lines_by_class(filelines, ['F', 'SF'])
    flush_dict = make_dict(flush_lines, evaluator._unique5)
    pickle_dict('flush_dict.pkl', flush_dict)

    unique5_lines = filter_lines_by_class(filelines, ['S', 'HC'])
    unique5_dict = make_dict(unique5_lines, evaluator._unique5)
    pickle_dict('unique5_dict.pkl', unique5_dict)

    pair_plus_lines = filter_lines_by_class(filelines, ['1P', '2P', '3K', 'FH', '4K'])
    pair_plus_dict = make_dict(pair_plus_lines, evaluator._matched_hand)
    pickle_dict('matched_hand_dict.pkl', pair_plus_dict)

