from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'survey'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    q1 = models.IntegerField(label="1. Please type your age in years. If you prefer not to say just input 0 below ", min=0)
    q2 = models.IntegerField(label="2. What gender do yu identify with?",
        choices=[
            [1, 'Male'],
            [2, 'Female'],
            [3, 'Other'],
        ],
        widget=widgets.RadioSelect
    )
    q3 = models.IntegerField(label="3. What degree are you doing?",
        choices=[
            [1, 'Business and Economics'],
            [2, 'Science and Medicine'],
            [3, 'Social Sciences'],
        ],
        widget=widgets.RadioSelect
    )
    q4 = models.IntegerField(label="4. What year are you in?",
        choices=[
            [1, 'Undergraduate'],
            [2, 'Post Graduate'],
        ],
        widget=widgets.RadioSelect
    )
    q5=  models.IntegerField(label="5. What religion do you identify with?",
        choices=[
            [1, 'I prefer not to say'],
            [2, 'Christianity'],
            [3, 'Muslim'],
            [4, 'Hinduisim'],
            [5, 'Buddhism'],
            [6, 'Other'],
            [7, 'Sikhism']
        ],
        widget=widgets.RadioSelect)
    #'Ethinicty'
   # q5= #'Religion'

    q6= models.IntegerField(label="6. What ethnicity do you identify with?",
        choices=[
            [1, 'I prefer not to say'],
            [2, 'Asian or Asian British'],
            [3, 'Black or Black British'],
            [4, 'Chinese'],
            [5, 'Mixed'],
            [6, 'White'],
            [7, 'Other ethnic group']
        ],
        widget=widgets.RadioSelect)

# PAGES
class Survey(Page):
    form_model = 'player'
    form_fields=['q1','q2','q3','q4','q5','q6']


class ResultsWaitPage(WaitPage):
    pass


class Finished(Page):
    pass


page_sequence = [Survey,Finished]
