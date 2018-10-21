from Model.Token import *
from Utils.Logger import my_logger
import Utils.VoiceGenerator as vg
CLASSIFICATION = 1
LINE = 2
MARK = '$'
TOP = -1
SUBTOP = -2
NUMBER = 'Number'
TENSE = 'Tense'
PERSON = 'Person'
TYPE = 'Type'
determiner_list_singular = ['this', 'that']
determiner_list_plural = ['these', 'those']
class Syntax:

    def __init__(self, lexical_input=[Token()]):
        self._lexical_input = []
        for lexical_entry in lexical_input:
            self._lexical_input.append(Token(lexical_entry))
        self._lexical_input = self._lexical_input[::-1]

        self.success = False
        self._last_read = Token()
        self._logger = my_logger('SyntaxAnalyzer')

    def _show_error(self, token=None, token_2=None, error_msg=''):
        self.success = False
        tk = token
        if not token:
            tk = self._last_read
        if not token_2:
            message = "We found an error on word: " + tk.get_token() + ". Error is: "  + error_msg
            self._logger.error('Token_read: ' + tk.get_token() + '. ' + error_msg)
            vg.saySomething(message)
        else:
            self._logger.error('Token_1: ' + tk.get_token() + ' Token_2: ' + token_2.get_token() + '. ' + error_msg)



    def _is_list_empty(self):
        return len(self._lexical_input) == 0

    def _get_next_token(self, pop=True):
        if len(self._lexical_input) == 0:
            return None
        if pop:
            self._last_read = self._lexical_input[-1]
            return self._lexical_input.pop()

        else:
            return self._lexical_input[-1]

    def _get_last_token_read(self):
        return self._last_read

    def _noun_validation(self, pronoun_token, noun_token):
        if pronoun_token.get_classification(PRONOUN).get_feature(NUMBER) == noun_token.get_classification(NOUN).get_feature(NUMBER):
            return True
        else:
            return False

    def _match_lexical_category(self, token, expected_category):
        if token.get_classification().get_lexical_category() == expected_category:
            return True
        else:
            return False

    def _determiner_checker(self, determiner_token, noun_token):
        self._logger.info('Checking agreement between Determiner and Noun.')
        if determiner_token.get_token() in determiner_list_singular:
            if noun_token.get_classification().get_feature(NUMBER) == 'Singular':
                return True
            self._show_error(token=determiner_token, token_2=noun_token,
                             error_msg='The determiner and the noun don\'t match in agreement.')
            return False
        elif determiner_token.get_token() in determiner_list_plural:
            if noun_token.get_classification().get_feature(NUMBER) == 'Plural':
                return True
            self._show_error(token=determiner_token, token_2=noun_token,
                             error_msg='The determiner and the noun don\'t match in agreement.')
            return False
        return True

    def _pronoun_checker(self, personal_pronoun=None, possessive_pronoun=None, noun=None):
        if personal_pronoun:
            if personal_pronoun.get_classification().get_feature(PERSON):
                return True
            else:
                return False
        elif possessive_pronoun and noun:
            if not possessive_pronoun.get_classification().get_feature(PERSON):
                if possessive_pronoun.get_classification().get_feature(NUMBER) == noun.get_classification().get_feature(NUMBER):
                    return True
                else:
                    self._show_error(token=possessive_pronoun,token_2=noun,
                                     error_msg='Possessive pronoun and noun don\'t match in agreement.')
                    return False
            else:
                self._show_error(token=possessive_pronoun, error_msg='Expected possessive pronoun')
                return False

    def _verb_checker(self, noun_pronoun, verb):
        self._logger.info('Checking agreement between noun|pronoun and verb. Token_1: ' + noun_pronoun.get_token() + ' Token_2: ' + verb.get_token() + '.')
        person_feature = verb.get_classification().get_feature(PERSON)
        if person_feature:
            if person_feature == '3d':
                if self._pronoun_checker(personal_pronoun=noun_pronoun):
                    if noun_pronoun.get_classification().get_feature(PERSON) == '3d':
                        return True
                    else:
                        self._show_error(token=noun_pronoun, token_2=verb,
                                         error_msg='Pronoun and verb don\'t match in agreement.')
                        return False
                else:
                    if noun_pronoun.get_classification().get_feature(NUMBER) == 'Singular':
                        return True
                    else:
                        self._show_error(token=noun_pronoun, token_2=verb,
                                         error_msg='Noun and verb don\'t match in agreement.')
                        return False
            else:
                if self._pronoun_checker(personal_pronoun=noun_pronoun):
                    if noun_pronoun.get_classification().get_feature(PERSON) != '3d':
                        return True
                    else:
                        self._show_error(token=noun_pronoun, token_2=verb,
                                         error_msg='Pronoun and verb don\'t match in agreement.')
                        return False
                else:
                    if noun_pronoun.get_classification().get_feature(NUMBER) == 'Plural':
                        return True
                    else:
                        self._show_error(token=noun_pronoun, token_2=verb,
                                         error_msg='Noun and verb don\'t match in agreement.')
                        return False

        if verb.get_classification().get_feature(TYPE) == 'Gerund':
            self._show_error(token=verb,
                             error_msg='Cannot use verb in gerund without \'is\' or \'are\' before it.')
            return False
        return True

    def _preposition_checker(self, preposition_token, verb_token):
        self._logger.info('Checking preposition and verb. Token_1: ' + preposition_token.get_token() + ' Token_2: ' + verb_token.get_token() +'.')
        if preposition_token.get_token() == 'of':
            if verb_token.get_classification().get_feature(TYPE) == 'Gerund':
                return True
            else:
                self._show_error(token=preposition_token, token_2=verb_token,error_msg='\'Of\' can only be used along with verb in gerund.')
                return False

        elif preposition_token.get_token() == 'to':
            if verb_token.get_classification().get_feature(TYPE) == 'Base':
                return True
            else:
                self._show_error(token=preposition_token, token_2=verb_token, error_msg='\'To\' can only be used along with verb in infinitive.')
                return False

        else:
            self._show_error(token=preposition_token, error_msg='Only \'to\' and \'of\' are accepted as prepositions.')
            return False

    def start(self):
        # print(self._lexical_input)
        self.success = True
        self._logger.info('Initiating syntax analysis.')
        self._program_routine()
        if self.success:
            self._logger.info('Your program syntax is correct.')

    def _program_routine(self):
        if self._sentence_routine():
            token = self._get_next_token()
            if (not token) or (token and not self._match_lexical_category(token, DOT)):
                self._show_error(token=token, error_msg='Missing expected period.')

    def _sentence_routine(self):
        if self._sintagma_nominal_routine():
            if self._sintagma_verbal_routine():
                return True
            else:
                return False
        else:
            return False

    def _sintagma_nominal_routine(self):
        if self._is_list_empty():
            return False
        token = self._get_next_token()
        if self._match_lexical_category(token, DETERMINER):
            self._logger.info('Determiner has been read. Token: ' + token.get_token() + '.')

            if self._is_list_empty():
                return False
            token_aux = self._get_next_token()

            if not self._match_lexical_category(token_aux, NOUN):
                self._show_error(token=token, error_msg='Missing expected Noun.')
                return False
            self._logger.info('Noun has been read. Token: ' + token_aux.get_token() + '.')
            if not self._determiner_checker(token, token_aux):
                return False

        elif self._match_lexical_category(token, PRONOUN):
            self._logger.info('Pronoun has been read. Token: ' + token.get_token() + '.')
            if not self._pronoun_checker(personal_pronoun=token):
                self._logger.info('Possessive pronoun has been read. Token: ' + token.get_token() + '.')
                if self._is_list_empty():
                    return False
                token = self._get_next_token()

                if not self._match_lexical_category(token, NOUN):
                    self._show_error(token=token, error_msg='Missing expected Noun after Possessive Pronoun.')
                    return False
                else:
                    self._logger.info('Noun has been read after possessive pronoun. Token: ' + token.get_token() + '.')
            else:
                self._logger.info('Personal pronoun has been read. Token: ' + token.get_token() + '.')

        elif not self._match_lexical_category(token, NOUN):
            self._show_error(token=token, error_msg='Missing expected Noun.')
            return False
        else:
            self._logger.info('Noun has been read. Token: ' + token.get_token() + '.')

        return True

    def _sintagma_verbal_routine(self):
        noun_token = self._last_read
        if self._is_list_empty():
            return False
        token = self._get_next_token()

        if not self._match_lexical_category(token, VERB):
            self._show_error(token=token, error_msg='Missing expected verb.')
            return False
        else:
            if self._verb_checker(noun_pronoun=noun_token, verb=token):
                return self._phrase_construction()
            else:
                return False

    def _phrase_construction(self):
        if self._is_list_empty():
            return False
        token = self._get_next_token(pop=False)
        token_aux = None

        result = True
        result = self._preposition_construction()
        if not result:
            return result

        token_aux = self._get_next_token(pop=False)
        if token == token_aux:
            result = self._adverb_construction()
            if not result:
                return result

        token_aux = self._get_next_token(pop=False)
        if token == token_aux:
            result = self._adjective_construction()
            if not result:
                return result

        token_aux = self._get_next_token(pop=False)
        if token == token_aux:
            if self._match_lexical_category(token, NOUN) or self._match_lexical_category(token, PRONOUN):
                self._get_next_token()
        return True

    def _preposition_construction(self):
        token = self._get_next_token(pop=False)
        if self._match_lexical_category(token, PREPOSITION):
            self._logger.info('Preposition has been read. Token: ' + token.get_token() + '.')
            self._get_next_token()

            if self._is_list_empty():
                return False
            token_aux = self._get_next_token()

            if not (self._match_lexical_category(token_aux, VERB) or self._match_lexical_category(token_aux,NOUN)):
                self._show_error(token=token_aux, error_msg='Expected missing verb or noun.')
                return False
            else:
                self._logger.info('%s has been read after preposition. Token: '
                                  % (token_aux.get_classification().get_lexical_category()) + token_aux.get_token() + '.')
                if self._match_lexical_category(token_aux, VERB):
                    if not self._preposition_checker(token, token_aux):
                        return False

        return True

    def _adverb_construction(self):
        token = self._get_next_token(pop=False)

        if token.get_token() == 'not':
            self._get_next_token()
            self._logger.info('\'Not\' adverb has been read.')

            if self._is_list_empty():
                return False
            token = self._get_next_token()

            if not (self._match_lexical_category(token, NOUN) or
                    self._match_lexical_category(token, ADJECTIVE) or self._match_lexical_category(token, VERB)):
                self._show_error(token=token, error_msg='Missing expected Noun|Adjective|Verb after \'not\' adverb.')
                return False
            else:
                self._logger.info('%s has been read after \'not\'.' % (token.get_classification().get_lexical_category()) + ' Token: ' + token.get_token() + '.')
                if self._match_lexical_category(token, VERB):
                    if not token.get_classification().get_feature(TYPE) == 'Gerund':
                        self._show_error(token=token, error_msg='Only verb in gerund can be used after \'not\'.')
                        return False

        elif self._match_lexical_category(token, ADVERB):
            self._logger.info('Adverb has been read. Token: ' + token.get_token() + '.')
            self._get_next_token()

        return True

    def _adjective_construction(self):
        token = self._get_next_token(pop=False)
        if not self._match_lexical_category(token, ADJECTIVE):
            return True
        self._get_next_token()
        self._logger.info('Adjective has been read. Token: ' + token.get_token() + '.')

        if self._is_list_empty():
            return True

        token = self._get_next_token(pop=False)
        if self._match_lexical_category(token, NOUN):
            self._get_next_token()
            self._logger.info('Noun has been read after adjective. Token: ' + token.get_token() + '.')
            return True
        if not self._match_lexical_category(token, ADJECTIVE):
            return True
        while not self._is_list_empty():
            token = self._get_next_token(pop=False)
            if self._match_lexical_category(token, ADJECTIVE):
                self._logger.info('Adjective has been read. Token: ' + token.get_token() + '.')
                self._get_next_token()
            elif self._match_lexical_category(token, NOUN):
                self._get_next_token()
                self._logger.info('Noun has been read after adjective. Token: ' + token.get_token() + '.')
                break
            else:
                self._show_error(token=token, error_msg='Missing expected Noun|Adjective.')
                return False
        return True
