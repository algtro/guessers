import random as rnd
from typing import List

from flask import session

GUESS_MIN: int = 10  # minimum value for guess number
GUESS_MAX: int = 99  # maximum value for guess number

GUESSERS_COUNT: int = 3  # count of guessers for testing

USER_HISTORY_KEY: str = "user_history"  # key for user history in session
GUESSER_HISTORY_KEY: str = "guesser_history"  # key for guesser history in session
GUESSER_CONFIDENCE_KEY: str = "guesser_confidence"  # key for guesser confidence level


class User:
    """Implements user data"""

    def __init__(self):
        """Constructor"""
        self.guessers = []  # list of guessers
        i = 0
        while i < GUESSERS_COUNT:
            self.guessers.append(Guesser(i))  # create guesser
            i += 1
        self.selected_number = 0

    @property
    def guessers_json(self) -> []:
        """Returns list of guessers data in JSON"""
        guessers_data = []
        for guesser in self.guessers:
            guessers_data.append({"index": guesser.index,
                                  "confidence": guesser.confidence_level,
                                  "guess": guesser.guess,
                                  "history": guesser.history})
        return guessers_data

    @property
    def history(self) -> []:
        """
        Get user history from session object
        :return: List of integers selected by current user
        """
        if USER_HISTORY_KEY in session:
            return session.get(USER_HISTORY_KEY)
        return []

    def _update_history(self) -> None:
        """Store value to user history"""
        user_history_value: List[int] = []
        if USER_HISTORY_KEY in session:
            user_history_value = session.get(USER_HISTORY_KEY)
        user_history_value.append(self.selected_number)
        session[USER_HISTORY_KEY] = user_history_value

    def _update_guessers(self) -> None:
        """Calculate guessers confidence level and update guessers history"""
        for guesser in self.guessers:
            guesser.apply_user_answer(self.selected_number)

    def set_selected_number(self, selected_number: int) -> None:
        """
        Receive new number selected by the user,
        update user history, update guessers confidence and history
        :param selected_number: Integer selected by the user
        """
        self.selected_number = selected_number
        self._update_history()
        self._update_guessers()
        print("user :: set_selected_number :: done")


class Guesser:
    """Implements data manipulations for one extrasensory individual person"""

    def __init__(self, index: int):
        """
        Constructor
        :param index: The unique sequence number of current guesser
        """
        self.index = str(index)
        self._update_guess_number()

    @property
    def confidence_level(self) -> int:
        data_object = self._get_session_data()
        if GUESSER_CONFIDENCE_KEY in data_object:
            return data_object[GUESSER_CONFIDENCE_KEY]
        return 0

    @property
    def history(self) -> []:
        data_object = self._get_session_data()
        if GUESSER_HISTORY_KEY in data_object:
            return data_object[GUESSER_HISTORY_KEY]
        return []

    def _update_guess_number(self):
        self.guess = GuessNumberGenerator.get_guess(GUESS_MIN, GUESS_MAX)

    def _update_confidence_level(self, user_answer: int) -> None:
        """
        Update confidence level for current guesser.
        If user`s answer is equal to answer prepared by guesser,
        then confidence level sets higher by one, else lower by one
        :param user_answer: integer selected by the user
        """
        confidence_level: int = 0
        data_object = self._get_session_data()
        if GUESSER_CONFIDENCE_KEY in data_object:
            confidence_level = data_object[GUESSER_CONFIDENCE_KEY]
        if self.guess == user_answer:
            confidence_level += 1
        else:
            confidence_level -= 1
        data_object[GUESSER_CONFIDENCE_KEY] = confidence_level
        self._update_session_data(data_object)

    def _update_history(self) -> None:
        """Update history for current guesser"""
        history: List[int] = []
        data_object = self._get_session_data()
        if GUESSER_HISTORY_KEY in data_object:
            history = data_object[GUESSER_HISTORY_KEY]
        history.append(self.guess)
        data_object[GUESSER_HISTORY_KEY] = history
        self._update_session_data(data_object)

    def _get_session_data(self) -> {}:
        """Returns data container for self index from session or empty"""
        if self.index in session:  # check for the self index in session
            return session.get(self.index)  # get stored data if is there
        return {}

    def _update_session_data(self, data_object):
        """Update data for the self index in session"""
        session[self.index] = data_object

    def apply_user_answer(self, user_answer: int) -> None:
        self._update_confidence_level(user_answer)
        self._update_history()
        self._update_guess_number()


class GuessNumberGenerator:
    """Implements generation of numbers for guessing"""
    @staticmethod
    def get_guess(value_min: int, value_max: int) -> int:
        """
        Generates random int number in selected range and returns it
        :param value_min: Minimum value of random int number
        :param value_max: Maximum value of random int number
        :return: Random integer
        """
        return rnd.randint(value_min, value_max)
