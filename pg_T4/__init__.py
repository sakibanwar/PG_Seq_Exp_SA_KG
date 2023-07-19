from otree.api import *


doc = """
Treatment 4: History Length 2, No position Uncertainty
"""

class C(BaseConstants):
    NAME_IN_URL = 'pg_T4'
    PLAYERS_PER_GROUP = 4
    NUM_ROUNDS = 10
    MULTIPLIER=3
    ENDOWMENT=cu(10)
    M=2 #No. of Predecessors
    FORM_TEMPLATE = __name__ + '/form.html'
    EXAMPLE=cu(10)
    EXAMPLE_PAYOFF=EXAMPLE*MULTIPLIER/PLAYERS_PER_GROUP
    SHOW_UP=5
    EXCHANGE =50 # 50 P per token
   
def get_quiz_data():
    return [
        dict(
            name='a',
            solution=False,
            explanation=" False: groups are re-matched randomly before the beginning of each round.",
        ),
        dict(
            name='b',
            solution=True,
            explanation="True: All players will learn about their position.",
        ),
        dict(
            name='c',
            solution=1,
            explanation="0: No one contributed to the common project. So your income will be 0.",
        ),
        dict(
            name='d',
            solution=1,
            explanation="0: You contributed to the common project account. So your income will be 0 from the private account.",
        ),
        dict(
            name='e',
            solution= ((C.ENDOWMENT*2*C.MULTIPLIER)/4)+C.ENDOWMENT,
            explanation=f"So your income will be  {((C.ENDOWMENT*2*C.MULTIPLIER)/4)+C.ENDOWMENT}. This is calculated by ({C.ENDOWMENT} + ({C.ENDOWMENT*2}x{C.MULTIPLIER})/4). ",
        ),
        dict(
            name='f',
            solution= C.M,
            explanation=f"Here M is {C.M} ",
        ),
    ]


class Subsession(BaseSubsession):
    pass
def creating_session(subsession):
    import random
    if subsession.round_number==1:
        subsession.session.my_round=random.randint(1, C.NUM_ROUNDS)
    print(subsession.session.my_round)

class Group(BaseGroup):
    total_contribution=models.CurrencyField()
    individual_share=models.CurrencyField()





class Player(BasePlayer):
    #Comprehension Test/quiz
    a = models.BooleanField(label="In every round the composition of the group remains the same.")
    b = models.BooleanField(label="You will  learn about your position in the sequence.")
    c = models.IntegerField(label="If none of the 4 members of the group contributes anything to the common project account, what will your income be from the common project account?",
        widget=widgets.RadioSelectHorizontal,
        choices=[
        [1, '0'],
        [2, '10'],
        [3, '20'],
    ])
    d = models.IntegerField(
        label="If all the 4 members of the group contribute their endowment to the common project account, what will your income be from the private account?",
        widget=widgets.RadioSelectHorizontal,
        choices=[
        [1, '0'],
        [2, '10'],
        [3, '20'],
    ])
    
    e = models.IntegerField(
        label="If only two members of the group have contributed to the common project account and you decide to put your endowment to your private account, what will your total income be (income from private account + income from common project account). ",
        )
    f = models.IntegerField(
        label="In each round, you will receive scenarios revealing you the potential total contribution of  <strong> M </strong>  immediate players before you. What is <strong> M </strong>? ",
        )
    contribution=models.CurrencyField()
    #Response for player in position 1
    response_0p1=models.CurrencyField(
            label="There was no previous player. How much do you want to contribute to the common project account?",
            widget=widgets.RadioSelectHorizontal,
            choices=[[cu(0),'Contribute 0 tokens'],[C.ENDOWMENT,'Contribute 10 tokens']])

    #Response for player in position 2        
    response_0p2=models.CurrencyField(
            label="If the previous player contributed 0 in total to the common project, how much do you want to contribute to the common project account?",
            widget=widgets.RadioSelectHorizontal,
            choices=[[cu(0),'Contribute 0 tokens'],[C.ENDOWMENT,'Contribute 10 tokens']])
    response_1p2=models.CurrencyField(
            label="If the previous player contributed 10 in total to the common project, how much do you want to contribute to the common project account?",
            widget=widgets.RadioSelectHorizontal,
            choices=[[cu(0),'Contribute 0 tokens'],[C.ENDOWMENT,'Contribute 10 tokens']])

    #Response for players in position 3 and 4 
    response_0p34=models.CurrencyField(
            label="If the previous 2 players contributed 0 in total to the common project, how much do you want to contribute to the common project account?",
            widget=widgets.RadioSelectHorizontal,
            choices=[[cu(0),'Contribute 0 tokens'],[C.ENDOWMENT,'Contribute 10 tokens']])       
    response_1p34=models.CurrencyField(
            label="If the previous 2 players contributed 10 in total to the common project, how much do you want to contribute to the common project account?",
            widget=widgets.RadioSelectHorizontal,
            choices=[[cu(0),'Contribute 0 tokens'],[C.ENDOWMENT,'Contribute 10 tokens']])
    response_2p34=models.CurrencyField(
            label="If the previous 2 players contributed 20 in total to the common project, how much do you want to contribute to the common project account?",
            widget=widgets.RadioSelectHorizontal,
            choices=[[cu(0),'Contribute 0 tokens'],[C.ENDOWMENT,'Contribute 10 tokens']])
    #response_3=models.CurrencyField(
    #        label="The previous players contributed 3. you have two options",
    #        widget=widgets.RadioSelectHorizontal,
    #        choices=[[1,'Yes'],[0,'No']])


def set_payoffs(group: Group):
    p1 = group.get_player_by_id(1)
    p2 = group.get_player_by_id(2)
    p3 = group.get_player_by_id(3)
    p4 = group.get_player_by_id(4)
    players = group.get_players()

    #Total 16 scenarios
    #sceanrio1 - 1,1,1,1
    if p1.response_0p1==C.ENDOWMENT and p2.response_1p2==C.ENDOWMENT and p3.response_2p34==C.ENDOWMENT and p4.response_2p34==C.ENDOWMENT:
        p1.contribution=C.ENDOWMENT
        p2.contribution=C.ENDOWMENT
        p3.contribution=C.ENDOWMENT
        p4.contribution=C.ENDOWMENT
        contributions = [p.contribution for p in players]
        group.total_contribution = sum(contributions)
        group.individual_share = (group.total_contribution * C.MULTIPLIER / C.PLAYERS_PER_GROUP)
        for player in players:
            player.payoff = C.ENDOWMENT - player.contribution + group.individual_share
        print('outcome1')
    #2 - 1,1,1,0
    elif p1.response_0p1==C.ENDOWMENT and p2.response_1p2==C.ENDOWMENT and p3.response_2p34==C.ENDOWMENT and p4.response_2p34==cu(0):
        p1.contribution=C.ENDOWMENT
        p2.contribution=C.ENDOWMENT
        p3.contribution=C.ENDOWMENT
        p4.contribution=cu(0)
        contributions = [p.contribution for p in players]
        group.total_contribution = sum(contributions)
        group.individual_share = (group.total_contribution * C.MULTIPLIER / C.PLAYERS_PER_GROUP)
        for player in players:
            player.payoff = C.ENDOWMENT - player.contribution + group.individual_share
        print('outcome2')
     #3   1,1,0,1
    elif p1.response_0p1==C.ENDOWMENT and p2.response_1p2==C.ENDOWMENT and p3.response_2p34==cu(0) and p4.response_1p34==C.ENDOWMENT:
        p1.contribution=C.ENDOWMENT
        p2.contribution=C.ENDOWMENT
        p3.contribution=cu(0)
        p4.contribution=C.ENDOWMENT
        contributions = [p.contribution for p in players]
        group.total_contribution = sum(contributions)
        group.individual_share = (group.total_contribution * C.MULTIPLIER / C.PLAYERS_PER_GROUP)
        for player in players:
            player.payoff = C.ENDOWMENT - player.contribution + group.individual_share
        print('outcome3')

    #4  1, 1, 0, 0
    elif p1.response_0p1==C.ENDOWMENT and p2.response_1p2==C.ENDOWMENT and p3.response_2p34==cu(0) and p4.response_1p34==cu(0):
        p1.contribution=C.ENDOWMENT
        p2.contribution=C.ENDOWMENT
        p3.contribution=cu(0)
        p4.contribution=cu(0)
        contributions = [p.contribution for p in players]
        group.total_contribution = sum(contributions)
        group.individual_share = (group.total_contribution * C.MULTIPLIER / C.PLAYERS_PER_GROUP)
        for player in players:
            player.payoff = C.ENDOWMENT - player.contribution + group.individual_share
        print('outcome4')
    #5  1 0 1 1 1
    elif p1.response_0p1==C.ENDOWMENT and p2.response_1p2==cu(0) and p3.response_1p34==C.ENDOWMENT and p4.response_1p34==C.ENDOWMENT:
        p1.contribution=C.ENDOWMENT
        p2.contribution=cu(0)
        p3.contribution=C.ENDOWMENT
        p4.contribution=C.ENDOWMENT
        contributions = [p.contribution for p in players]
        group.total_contribution = sum(contributions)
        group.individual_share = (group.total_contribution * C.MULTIPLIER / C.PLAYERS_PER_GROUP)
        for player in players:
            player.payoff = C.ENDOWMENT - player.contribution + group.individual_share
        print('outcome5')
    #6 1 0 1 0
    elif p1.response_0p1==C.ENDOWMENT and p2.response_1p2==cu(0) and p3.response_1p34==C.ENDOWMENT and p4.response_1p34==cu(0):
        p1.contribution=C.ENDOWMENT
        p2.contribution=cu(0)
        p3.contribution=C.ENDOWMENT
        p4.contribution=cu(0)
        contributions = [p.contribution for p in players]
        group.total_contribution = sum(contributions)
        group.individual_share = (group.total_contribution * C.MULTIPLIER / C.PLAYERS_PER_GROUP)
        for player in players:
            player.payoff = C.ENDOWMENT - player.contribution + group.individual_share
        print('outcome6')
    #7 1 0 0 1
    elif p1.response_0p1==C.ENDOWMENT and p2.response_1p2==cu(0) and p3.response_1p34==cu(0) and p4.response_0p34==C.ENDOWMENT:
        p1.contribution=C.ENDOWMENT
        p2.contribution=cu(0)
        p3.contribution=cu(0)
        p4.contribution=C.ENDOWMENT
        contributions = [p.contribution for p in players]
        group.total_contribution = sum(contributions)
        group.individual_share = (group.total_contribution * C.MULTIPLIER / C.PLAYERS_PER_GROUP)
        for player in players:
            player.payoff = C.ENDOWMENT - player.contribution + group.individual_share
        print('outcome7')
    #8    1 0 0 0
    elif p1.response_0p1==C.ENDOWMENT and p2.response_1p2==cu(0) and p3.response_1p34==cu(0) and p4.response_0p34==cu(0) :
        p1.contribution=C.ENDOWMENT
        p2.contribution=cu(0)
        p3.contribution=cu(0)
        p4.contribution=cu(0)
        contributions = [p.contribution for p in players]
        group.total_contribution = sum(contributions)
        group.individual_share = (group.total_contribution * C.MULTIPLIER / C.PLAYERS_PER_GROUP)
        for player in players:
            player.payoff = C.ENDOWMENT - player.contribution + group.individual_share
        print('outcome8')
    #9  0 1 1 1
    elif p1.response_0p1==cu(0) and p2.response_0p2==C.ENDOWMENT and p3.response_1p34==C.ENDOWMENT and p4.response_2p34==C.ENDOWMENT :
        p1.contribution=cu(0)
        p2.contribution=C.ENDOWMENT
        p3.contribution=C.ENDOWMENT
        p4.contribution=C.ENDOWMENT
        contributions = [p.contribution for p in players]
        group.total_contribution = sum(contributions)
        group.individual_share = (group.total_contribution * C.MULTIPLIER / C.PLAYERS_PER_GROUP)
        for player in players:
            player.payoff = C.ENDOWMENT - player.contribution + group.individual_share
        print('outcome9')
      
    #10  0 1 1 0  
    elif p1.response_0p1==cu(0) and p2.response_0p2==C.ENDOWMENT and p3.response_1p34==C.ENDOWMENT and p4.response_2p34==cu(0):
        p1.contribution=cu(0)
        p2.contribution=C.ENDOWMENT
        p3.contribution=C.ENDOWMENT
        p4.contribution=cu(0)
        contributions = [p.contribution for p in players]
        group.total_contribution = sum(contributions)
        group.individual_share = (group.total_contribution * C.MULTIPLIER / C.PLAYERS_PER_GROUP)
        for player in players:
            player.payoff = C.ENDOWMENT - player.contribution + group.individual_share
        print('outcome10')
    #11  0 1 0 1  
    elif p1.response_0p1==cu(0) and p2.response_0p2==C.ENDOWMENT and p3.response_1p34==cu(0) and p4.response_1p34==C.ENDOWMENT:
        p1.contribution=cu(0)
        p2.contribution=C.ENDOWMENT
        p3.contribution=cu(0)
        p4.contribution=C.ENDOWMENT
        contributions = [p.contribution for p in players]
        group.total_contribution = sum(contributions)
        group.individual_share = (group.total_contribution * C.MULTIPLIER / C.PLAYERS_PER_GROUP)
        for player in players:
            player.payoff = C.ENDOWMENT - player.contribution + group.individual_share
        print('outcome11')
    #12  0 1 0 0   
    elif p1.response_0p1==cu(0) and p2.response_0p2==C.ENDOWMENT and p3.response_1p34==cu(0) and p4.response_1p34==cu(0):
        p1.contribution=cu(0)
        p2.contribution=C.ENDOWMENT
        p3.contribution=cu(0)
        p4.contribution=cu(0)
        contributions = [p.contribution for p in players]
        group.total_contribution = sum(contributions)
        group.individual_share = (group.total_contribution * C.MULTIPLIER / C.PLAYERS_PER_GROUP)
        for player in players:
            player.payoff = C.ENDOWMENT - player.contribution + group.individual_share
        print('outcome12')
    #13 0 0 1 1
    elif p1.response_0p1==cu(0) and p2.response_0p2==cu(0) and p3.response_0p34==C.ENDOWMENT and p4.response_1p34==C.ENDOWMENT:
        p1.contribution=cu(0)
        p2.contribution=cu(0)
        p3.contribution=C.ENDOWMENT
        p4.contribution=C.ENDOWMENT
        contributions = [p.contribution for p in players]
        group.total_contribution = sum(contributions)
        group.individual_share = (group.total_contribution * C.MULTIPLIER / C.PLAYERS_PER_GROUP)
        for player in players:
            player.payoff = C.ENDOWMENT - player.contribution + group.individual_share
        print('outcome13')
    #14  0 0 1 0  
    elif p1.response_0p1==cu(0) and p2.response_0p2==cu(0) and p3.response_0p34==C.ENDOWMENT and p4.response_1p34==cu(0):
        p1.contribution=cu(0)
        p2.contribution=cu(0)
        p3.contribution=C.ENDOWMENT
        p4.contribution=cu(0)
        contributions = [p.contribution for p in players]
        group.total_contribution = sum(contributions)
        group.individual_share = (group.total_contribution * C.MULTIPLIER / C.PLAYERS_PER_GROUP)
        for player in players:
            player.payoff = C.ENDOWMENT - player.contribution + group.individual_share
        print('outcome15')
    #15    0 0 0 1 
    elif p1.response_0p1==cu(0) and p2.response_0p2==cu(0) and p3.response_0p34==cu(0) and p4.response_0p34==C.ENDOWMENT:
        p1.contribution=cu(0)
        p2.contribution=cu(0)
        p3.contribution=cu(0)
        p4.contribution=C.ENDOWMENT
        contributions = [p.contribution for p in players]
        group.total_contribution = sum(contributions)
        group.individual_share = (group.total_contribution * C.MULTIPLIER / C.PLAYERS_PER_GROUP)
        for player in players:
            player.payoff = C.ENDOWMENT - player.contribution + group.individual_share
    #16 0 0 0 0s
    elif p1.response_0p1==cu(0) and p2.response_0p2==cu(0) and p3.response_0p34==cu(0) and p4.response_0p34==cu(0):
        p1.contribution=cu(0)
        p2.contribution=cu(0)
        p3.contribution=cu(0)
        p4.contribution=cu(0)
        contributions = [p.contribution for p in players]
        group.total_contribution = sum(contributions)
        group.individual_share = (group.total_contribution * C.MULTIPLIER / C.PLAYERS_PER_GROUP)
        for player in players:
            player.payoff = C.ENDOWMENT - player.contribution + group.individual_share
        print('outcome16')            




# PAGES
class InstructionsT4(Page):
    def is_displayed(player):
        return player.round_number==1
# Comprehension Test/quiz
class Comprehension(Page):
    form_model = 'player'
    form_fields = ['a', 'b','c','d','e','f']

    @staticmethod
    def vars_for_template(player: Player):
        fields = get_quiz_data()
        return dict(fields=fields, show_solutions=False)
    def is_displayed(player):
        return player.round_number==1
class ComprehensionResults(Page):
    form_model = 'player'
    form_fields = ['a', 'b','c','d','e','f']

    @staticmethod
    def vars_for_template(player: Player):
        fields = get_quiz_data()
        # we add an extra entry 'is_correct' (True/False) to each field
        for d in fields:
            d['is_correct'] = getattr(player, d['name']) == d['solution']
        return dict(fields=fields, show_solutions=True)
    def is_displayed(player):
        return player.round_number==1

    @staticmethod
    def error_message(player: Player, values):
        for field in values:
            if getattr(player, field) != values[field]:
                return "A field was somehow changed but this page is read-only."
class ShuffleWaitPage(WaitPage):
    body_text='Creating Groups'
    wait_for_all_groups = True
    @staticmethod
    def after_all_players_arrive(subsession):
        subsession.group_randomly()


#Position 1     ############
class ContributeP1(Page):
    form_model='player'
    form_fields=['response_0p1']
    @staticmethod
    def is_displayed(player):
        return player.id_in_group==1
class MyWaitPage234(WaitPage):
    body_text='Waiting for Player 1 to make a decision'
    @staticmethod
    def is_displayed(player):
        return player.id_in_group>1

#Position 2        ############
class ContributeP2(Page):
    form_model='player'
    form_fields=['response_0p2','response_1p2']
    @staticmethod
    def is_displayed(player):
        return player.id_in_group==2

class MyWaitPage34(WaitPage):
    body_text='Waiting for Player 2 to make a decision'
    def is_displayed(player):
        return player.id_in_group>2

#Position 3       
class ContributeP3(Page):
    form_model='player'
    form_fields=['response_0p34','response_1p34','response_2p34']
    def is_displayed(player):
        return player.id_in_group==3
class MyWaitPage4(WaitPage):
    body_text='Waiting for Player 3 to make a decision'
    def is_displayed(player):
        return player.id_in_group>3

#Position 4
class ContributeP4(Page):
    form_model='player'
    form_fields=['response_0p34','response_1p34','response_2p34']
    def is_displayed(player):
        return player.id_in_group==4


class ResultsWaitPage(WaitPage):
    #after_all_players_arrive='set_payoffs'
    body_text='Waiting for other players to make a decision'
    after_all_players_arrive = set_payoffs

class Results(Page):
    @staticmethod
    def before_next_page(player: Player, timeout_happened):

        participant = player.participant
        #subsession.session.my_round

        # if it's the last round
        if player.round_number == C.NUM_ROUNDS:
            # player_in_selected_round = player.in_round(random_round)
            # player.payoff = C.ENDOWMENT - player_in_selected_round.give_amount
            player_in_selected_round = player.in_round(player.session.my_round)
            participant.payoff = player_in_selected_round.payoff
            print('selected_round_results',player.session.my_round)

class FinalResults(Page):
    body_text='You finished the experiment'
    @staticmethod
    def vars_for_template(player):
        participant = player.participant
        # random_round=random.randint(1, C.NUM_ROUNDS)
        return dict (
            my_cont=player.in_round(player.session.my_round).contribution,
            tc=player.in_round(player.session.my_round).group.total_contribution,
            mypayoff=player.in_round(player.session.my_round).payoff,
            payoff_round=player.session.my_round,
            earnings=participant.payoff_plus_participation_fee()
        )
    def is_displayed(player):
        return player.round_number==C.NUM_ROUNDS 


# class FinalResults(Page):
#     body_text='You finished the experiment'
    
#     @staticmethod
#     def vars_for_template(player):
#         import random
#         random_round=random.randint(1, C.NUM_ROUNDS)
#         return dict (
#             my_cont=player.in_round(random_round).contribution,
#             tc=player.in_round(random_round).group.total_contribution,
#             mypayoff=player.in_round(random_round).payoff,
#             payoff_round=random_round
#         )
#     def is_displayed(player):
#         return player.round_number==C.NUM_ROUNDS

page_sequence = [
                InstructionsT4,
                Comprehension,ComprehensionResults,
                ShuffleWaitPage,
                ContributeP1,MyWaitPage234,
                ContributeP2,MyWaitPage34,
                ContributeP3,MyWaitPage4,
                ContributeP4,ResultsWaitPage,
                Results,FinalResults]
