from otree.api import *
import random
import json
import pandas as pd
from itertools import accumulate

class C(BaseConstants):
     ## Number of question pages
    NAME_IN_URL = 'DesExp'
    PLAYERS_PER_GROUP = None
    ANIMATION = 1
    GROUPS = ["A","B"]


    PAGES_wITH_IMAGES = {
        "EndowmentEffect": "image/ceramic_mug_navy.jpg"
    }
    PAGES_TO_QUESTIONS = {
        "ConjunctionFallacy": ['conjunction_bank_teller', 'conjunction_bank_teller_feminist'],
        "GamblersFallacy": ['gambler_heads', 'gambler_tails'],
        "HotHandFallacy": ['hotHand'],
        "BaseRateFallacy": ['baseRate'],
        "IllusionofControl": ['illusionControl'],
        "AnchoringEffect": ['anchoring'],
        "HindsightBias": ['hindsight'],
        "PresentBias": ['presentBias'],
        "LossAversion": ['lossAversion'],
        "EndowmentEffect": ['endowment'],
        "DecoyEffect": ['decoy'],
        "FramingEffect": ['framing'],
        "StatusQuoBias": ['statusQuo'],
        "SunkCostFallacy": ['sunkCost'],
        "MentalAccounting": ['mentalAccounting'],
        "UltimatumGame": ['ultimatum_offer', 'ultimatum_accept'],
        "DictatorGame": ['dictator_amount'],
        "TrustInvestmentGame": ['trust_send'] +  [f'trust_return_{x}' for x in range(3,31,3)],
        "PublicGoodsGame": ['public_goods_contrib'],
        "PrisonersDilemma": ['prisoner_choice'],
        "CoordinationGame": ['coord_restaurant_choice', 'coord_other_likelihood'],
        "BertrandCompetition": ['bertrand_price'],
        "CournotCompetition": ['cournot_quantity'],
        "SSWMarket": [f"ssw_{prefix}_{period}" for period in range(12) for prefix in ("wtp", "wta")],
        "WisdomofCrowd": ['wisdom_michael', 'wisdom_daniel', 'wisdom_christoph']
    }
    
    PAGES = list(PAGES_TO_QUESTIONS.keys()) + ["CognitiveLimitInvestment","CognitiveLimitBox","CognitiveLimitInsurance"]

    ## On/off switch per experiment: session config key -> page name.
    ## Set the keys to True/False in settings.py (or in the admin "Configure session" form).
    ## Keys missing from the session config default to on.
    EXPERIMENT_TOGGLES = {
        "E01_ConjunctionFallacy": "ConjunctionFallacy",
        "E02_GamblersFallacy": "GamblersFallacy",
        "E03_HotHandFallacy": "HotHandFallacy",
        "E05_BaseRateFallacy": "BaseRateFallacy",
        "E06_IllusionofControl": "IllusionofControl",
        "E07_AnchoringEffect": "AnchoringEffect",
        "E08_HindsightBias": "HindsightBias",
        "E09_PresentBias": "PresentBias",
        "E10_LossAversion": "LossAversion",
        "E11_EndowmentEffect": "EndowmentEffect",
        "E12_DecoyEffect": "DecoyEffect",
        "E13_FramingEffect": "FramingEffect",
        "E14_StatusQuoBias": "StatusQuoBias",
        "E15_SunkCostFallacy": "SunkCostFallacy",
        "E16_MentalAccounting": "MentalAccounting",
        "E17_UltimatumGame": "UltimatumGame",
        "E18_DictatorGame": "DictatorGame",
        "E19_TrustInvestmentGame": "TrustInvestmentGame",
        "E20_PublicGoodsGame": "PublicGoodsGame",
        "E21_PrisonersDilemma": "PrisonersDilemma",
        "E22_CoordinationGame": "CoordinationGame",
        "E23_BertrandCompetition": "BertrandCompetition",
        "E24_CournotCompetition": "CournotCompetition",
        "E25_SSWMarket": "SSWMarket",
        "E26_WisdomofCrowd": "WisdomofCrowd",
        "E27_30_CountingHeuristic": "CognitiveLimitInvestment",
        "E31_DeterministicMirror": "CognitiveLimitBox",
        "E32_InsurancePlan": "CognitiveLimitInsurance",
    }
    PAGE_TO_TOGGLE = {page: key for key, page in EXPERIMENT_TOGGLES.items()}

    ## Fixed id saved in the "question" field (Stata maps question_id -> experiment_id).
    ## Ids stay the same when experiments are removed so data stays comparable across sessions.
    ## Retired ids: 3 = DispositionEffect (E4)
    QUESTION_IDS = {
        "ConjunctionFallacy": 0,
        "GamblersFallacy": 1,
        "HotHandFallacy": 2,
        "BaseRateFallacy": 4,
        "IllusionofControl": 5,
        "AnchoringEffect": 6,
        "HindsightBias": 7,
        "PresentBias": 8,
        "LossAversion": 9,
        "EndowmentEffect": 10,
        "DecoyEffect": 11,
        "FramingEffect": 12,
        "StatusQuoBias": 13,
        "SunkCostFallacy": 14,
        "MentalAccounting": 15,
        "UltimatumGame": 16,
        "DictatorGame": 17,
        "TrustInvestmentGame": 18,
        "PublicGoodsGame": 19,
        "PrisonersDilemma": 20,
        "CoordinationGame": 21,
        "BertrandCompetition": 22,
        "CournotCompetition": 23,
        "SSWMarket": 24,
        "WisdomofCrowd": 25,
        "CognitiveLimitInvestment": 26,
        "CognitiveLimitBox": 27,
        "CognitiveLimitInsurance": 28,
    }

    CATEGORIES = {
            "Instruction": 1,
            "Question": len(PAGES_TO_QUESTIONS.keys()),
            "CognitiveLimitInvestment": 4,
            "CognitiveLimitBox": 1,
            "CognitiveLimitInsurance": 1,
            "Survey": 7,
        }
    
    OTHER_PAGES_TO_QUESTIONS = {
        "CognitiveLimitInvestment": [f"cognitiveLimitInvestment_{i}" for i in range(1, CATEGORIES["CognitiveLimitInvestment"] + 1)] + [f"cognitiveLimitInvestmentOpinion_{i}" for i in range(1,CATEGORIES["CognitiveLimitInvestment"] + 1)],
        "CognitiveLimitBox": [f"cognitiveLimitBox_{i}" for i in range(1,22)],
        "CognitiveLimitInsurance": ["cognitiveLimitInsurance"]
    }
    
    CATEGORY_START_INDEX = {
        category: idx
        for category, idx in zip(
            CATEGORIES.keys(),
            accumulate([0] + list(CATEGORIES.values())[:-1])
        )
    }
            
    SHEET2 = pd.read_excel(
        'design_exp/rCum_distributions_new.xlsx', engine='openpyxl'
    )
    RETA = SHEET2.iloc[0:, :10]
    RETB = SHEET2.iloc[0:, 10:20]
    CUMRETA = (1+ RETA).cumprod(axis=1) - 1
    CUMRETB = (1+ RETB).cumprod(axis=1) - 1
    
    NUM_ROUNDS = sum(CATEGORIES.values())
    

    survey_pages = {
        0: {
            'form_fields': [
                'Demographics_Age',
                'Demographics_Sex',
                'Demographics_FinInterest',
                'Demographics_Investor',
                'Demographics_InvestorHistory',
                'Demographics_InvestorExperience',
                'Demographics_FinanceProf',
                'Demographics_RiskAffinity',
            ],
        },
        1: {
            'form_fields': [
                'Demographics_Percentages',
                'Demographics_Intuition',
                'Demographics_IdeasVsFacts',
                'Demographics_AnalysisVsInsights',
            ],

        },
        2: {
            'form_fields': [
                'interest_rate_inflation',
                'bonds_riskier',
                'highest_return_asset',
                'highest_fluctuations_asset',
                'risk_spreading_money',
                'stock_mutual_fund',
            ],
        },
        3: {
            'form_fields': [
                'invest_mutual_fund',
                'mortgage_payment',
                'savings_interest',
                'mutual_fund_statement',
                'bond_purchase',
                'credit_card_debt',
            ],
        },
        4: {
            'form_fields': [
                'faith1',
                'faith2',
                'faith3',
                'faith4',
                'faith5',
                'faith6',
            ],
        },
        5: {
            'form_fields': [
                'faith7',
                'faith8',
                'faith9',
                'faith10',
                'faith11',
                'faith12',
            ],
        },
        6: {
            'form_fields': [
                'overconfidence1',
                'overconfidence2',
                'overconfidence3',
            ],
        },
    }

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass 
"""
def pos_integerfield(label):
    return models.PositiveIntegerField(label=label,
                                       widget=widgets.RadioSelect,
                                       choices=C.STANDARDCHOICES)


def floatfield(label, max):
    return models.FloatField(label=label,
                             min=0,
                             max=max)
"""

class Player(BasePlayer):

    datarows = models.LongStringField()
    #page_groups = models.LongStringField()
    #question_groups = models.LongStringField()
    #question_pages_order = models.LongStringField()
    experiment_group = models.StringField()
    question = models.IntegerField()
    isLeaving = models.BooleanField(choices=((True, 'leaving'), (False, 'notleaving')),
                                    initial=0)
    browser_first = models.StringField()
    last_name = models.StringField(
        blank=True,
        label='Last name')
    first_name = models.StringField(
        blank=True,
        label='First name')
    student_number = models.StringField(
        blank=True,
        label='Student number')

    # 1. Conjunction fallacy
    conjunction_bank_teller_A = models.FloatField(
        min=0,
        max=100,
        label="Linda is a woman who cares about social problems. What do you think is the probability that Linda is a bank teller (in %, e.g., 10 for 10%)?"
    )
    conjunction_bank_teller_feminist_A = models.FloatField(
        min=0,
        max=100,
        label="What do you think is the probability that Linda is a bank teller who is also active in the feminist movement (in %, e.g., 10 for 10%)?"
    )
    conjunction_bank_teller_B = models.FloatField(
        min=0,
        max=1000,
        label="Linda is a woman who cares about social problems. Out of 1000 Lindas, how many do you think are bank tellers?"
    )
    conjunction_bank_teller_feminist_B = models.FloatField(
        min=0,
        max=1000,
        label="How many do you think are bank tellers who are also active in the feminist movement?"
    )

    # 2. Gambler's Fallacy
    gambler_heads_A = models.FloatField(
        min=0,
        max=100,
        label="A fair coin is flipped 6 times and lands: H, H, H, H, H, H. What is the probability that the next flip will be Heads (in %, e.g., 10 for 10%)?"
    )
    gambler_tails_A = models.FloatField(
        min=0,
        max=100,
        label="What is the probability that the next flip will be Tails (in %, e.g., 10 for 10%)?"
    )

    gambler_heads_B = models.FloatField(
        min=0,
        max=100,
        label="A fair coin is flipped 6 times and lands: H, T, H, T, H, T. What is the probability that the next flip will be Heads (in %, e.g., 10 for 10%)? "
    )
    gambler_tails_B = models.FloatField(
        min=0,
        max=100,
        label="What is the probability that the next flip will be Tails (in %, e.g., 10 for 10%)?"
    )

    # 3. Hot Hand Fallacy
    hotHand_A = models.FloatField(
        min=0,
        max=100,
        label="A basketball player has made 5 shots in a row. What is the probability that they will make the next shot (in %, e.g., 10 for 10%)?"
    )
    hotHand_B = models.FloatField(
        min=0,
        max=100,
        label="Out of 100 basketball players who made 5 shots in a row, how many do you think made the next shot?"
    )

    # 5. Base Rate Fallacy
    baseRate_A = models.FloatField(
        min=0,
        max=100,
        label="In a city, 85% of the cabs are green and 15% are blue. A witness identifies a cab involved in a hit-and-run as blue. The witness is 80% accurate at distinguishing blue from green cabs.<br><br>What is the probability the cab was actually blue (in %, e.g., 10 for 10%)?"
    )
    baseRate_B = models.FloatField(
        min=0,
        max=1000,
        label="In a city, 850 out of 1000 cabs are green and 150 are blue. A witness identifies a cab involved in a hit-and-run as blue. The witness correctly identifies a cab’s color 8 times out of 10.<br><br>Out of 1000 incidents with an identified color, how many times would the cab actually be blue when the witness says “blue”?"
    )

    # 6. Illusion of Control
    illusionControl_A = models.StringField(
        label="You're in a lottery where you can pick your own numbers or let the system choose. Which option do you prefer to maximize your chances?",
        choices=["Pick my own numbers", "Let the system choose", "Either"],
        widget=widgets.RadioSelect
    )
    illusionControl_B = models.StringField(
        label="100 people bought lottery tickets. 50 of them pick their own numbers, the other 50 let the system choose automatically. The winner is more likely to be in:",
        choices=["Number picking group", "Random number group", "Either"],
        widget=widgets.RadioSelect
    )

    # 7. Anchoring Effect
    anchoring_A = models.FloatField(
        min=0,
        max=500,
        label="What do you guess is the median height of a 30-year old Swiss spruce tree (in meters, e.g., 100 meters is the median height if the probabilities of such a tree being higher and lower are both 50%)?"
    )
    anchoring_B = models.FloatField(
        min=0,
        max=500,
        label="What do you guess is the median height of a 30-year old Swiss spruce tree (in meters, e.g., 10 meters is the median height if the probabilities of such a tree being higher and lower are both 50%)?"
    )

    # 8. Hindsight Bias
    hindsight_A = models.FloatField(
        min=0,
        max=100,
        label="A start-up company is developing a new wearable health device. Market analysts say it has a 50/50 chance of success based on the competitive landscape.<br><br>How likely do you think it is that this company will succeed (in %, e.g., 10 for 10%)?"
    )
    hindsight_B = models.FloatField(
        min=0,
        max=100,
        label="A start-up company developed a new wearable health device. It succeeded and is now widely used. Market analysts had originally said it had a 50/50 chance of success.<br><br>How likely do you think it was that this company would succeed (in %, e.g., 10 for 10%)?"
    )

    # 9. Present Bias / Hyperbolic Discounting
    presentBias_A = models.StringField(
        label="You can get a $20 gift card right now or a $25 gift card next month. Which would you choose?",
        choices=["$20 now", "$25 in 1 month"],
        widget=widgets.RadioSelect
    )
    presentBias_B = models.StringField(
        label="You can get a $20 gift card in 12 months, or a $25 gift card in 13 months. Which would you choose?",
        choices=["$20 in 12 months", "$25 in 13 months"],
        widget=widgets.RadioSelect
    )

    # 10. Loss Aversion
    lossAversion_A = models.StringField(
        label="You are given a wallet with €1000. Would you prefer:",
        choices=["A sure gain of €500", "A 50% chance to gain another €1000, a 50% chance to gain €0"],
        widget=widgets.RadioSelect
    )
    lossAversion_B = models.StringField(
        label="You are given a wallet with €2000. Would you prefer:",
        choices=["A sure loss of €500", "A 50% chance to lose €0, a 50% chance to lose €1000"],
        widget=widgets.RadioSelect
    )

    # 11. Endowment Effect
    endowment_A = models.FloatField(
        min=0,
        label="You receive this mug as a gift. How much would you be willing to sell it for? (€)"
    )
    endowment_B = models.FloatField(
        min=0,
        label="You get the offer to buy this mug. How much would you pay for it? (€)"
    )

    # 12. Decoy Effect (Asymmetric Dominance)
    decoy_A = models.StringField(
        label="Which do you prefer as a mobile data plan on a trip abroad?",
        choices=["Option A: €10 for 1GB data", "Option B: €14 for 1.5GB data", "Option C: €15 for 2GB data"],
        widget=widgets.RadioSelect
    )
    decoy_B = models.StringField(
        label="Which do you prefer as a mobile data plan on a trip abroad?",
        choices=["Option A: €10 for 1GB data", "Option B: €15 for 2GB data"],
        widget=widgets.RadioSelect
    )

    # 13. Framing Effect
    framing_A = models.StringField(
        label="A community is facing a health challenge expected to affect 600 people. Choose a program:<br><strong>Program A:</strong> 200 people will be helped<br><strong>Program B:</strong> 1/3 chance that all 600 will be helped, 2/3 chance that no one will be helped",
        choices=["Program A", "Program B"],
        widget=widgets.RadioSelect
    )
    framing_B = models.StringField(
        label="A community is facing a health challenge expected to affect 600 people. Choose a program:<br><strong>Program A:</strong> 400 people will not be helped<br><strong>Program B:</strong> 2/3 chance that all 600 will not be helped, 1/3 chance that everyone will be helped",
        choices=["Program A", "Program B"],
        widget=widgets.RadioSelect
    )

    # 14. Status Quo Bias
    statusQuo_A = models.StringField(
        label="You’re enrolled in Health Plan A. You’re offered Plan B with slightly higher coverage and higher cost. Do you:",
        choices=["Stay", "Switch"],
        widget=widgets.RadioSelect
    )
    statusQuo_B = models.StringField(
        label="You’re enrolled in Health Plan B. You’re offered Plan A with cheaper cost and slightly lower coverage. Do you:",
        choices=["Stay", "Switch"],
        widget=widgets.RadioSelect
    )

    # 15. Sunk Cost Fallacy
    sunkCost_A = models.StringField(
        label="You paid €15 to eat at a sushi buffet. After 20 minutes, you're full. Do you:",
        choices=["Stay and eat more", "Leave"],
        widget=widgets.RadioSelect
    )
    sunkCost_B = models.StringField(
        label="You get a free voucher to eat at sushi buffet. After 20 minutes, you're full. Do you:",
        choices=["Stay and eat more", "Leave"],
        widget=widgets.RadioSelect
    )

    # 16. Mental Accounting
    mentalAccounting_A = models.StringField(
        label="You intend to watch a movie with a €10 movie ticket. You bought the ticket in advance but then you lost it.<br>Do you buy another?",
        choices=["Yes", "No"],
        widget=widgets.RadioSelect
    )
    mentalAccounting_B = models.StringField(
        label="You intend to buy a movie ticket for €10. You put aside a €10 bill for the movie in advance but then you lost it. Do you still buy the ticket?",
        choices=["Yes", "No"],
        widget=widgets.RadioSelect
    )

    # Ultimatum Game
    ultimatum_offer_A = models.FloatField(
        min=0,
        max=10,
        label="You are Player 1. You have €10 to split with another participant (a total stranger). You can offer any amount from €0 to €10. If the other player accepts, the money is split as proposed. If they reject, you both get nothing.<br>What amount would you offer?"
    )
    ultimatum_accept_A = models.FloatField(
        min=0,
        max=10,
        label="You are Player 2. Suppose Player 1 offers you €X.<br>For which values of €X (from €0 to €10) would you accept the offer?"
    )
    ultimatum_offer_B = models.FloatField(
        min=0,
        max=10,
        label="You are Player 1. You have €10 to split with a close friend. You can offer any amount from €0 to €10. If the other player accepts, the money is split as proposed. If they reject, you both get nothing.<br>What amount would you offer?"
    )
    ultimatum_accept_B = models.FloatField(
        min=0,
        max=10,
        label="You are Player 2. Suppose Player 1 offers you €X.<br>For which values of €X (from €0 to €10) would you accept the offer?"
    )

    # Dictator Game
    dictator_amount_A = models.FloatField(
        min=0,
        max=10,
        label="You are the only decision-maker. You have €10. You can give any amount (0-10) to another participant, a total stranger. How much would you give?"
    )
    dictator_amount_B = models.FloatField(
        min=0,
        max=10,
        label="You are the only decision-maker. You have €10. You can give any amount (0-10) to a family member. How much would you give?"
    )

    # Trust (Investment) Game
    trust_send_A = models.FloatField(
        min=0,
        max=10,
        label="You are Player 1. You have €10. You can send any amount (€0–€10) to another participant, a stranger. Whatever you send will be tripled. The other participant will then choose how much to return to you. How much would you send?"
    )
    ## Trust return fields are created dynamically below the Player class
    trust_send_B = models.FloatField(
        min=0,
        max=10,
        label="You are Player 1. You have €10. You can send any amount (€0–€10) to a family member. Whatever you send will be tripled. The other participant will then choose how much to return to you. How much would you send?"
    )
    

    # Public Goods Game
    public_goods_contrib_A = models.FloatField(
        min=0,
        max=10,
        label="There are 4 players (including you) who are complete strangers. Everyone starts with €10 and decides how much to put into a shared pot. The total amount in the shared pot is doubled and then evenly divided among the 4 players.<br><br>How much would you contribute (0-10)?"
    )
    public_goods_contrib_B = models.FloatField(
        min=0,
        max=10,
        label="There are 4 players (including you and your close friends). Everyone starts with €10 and decides how much to put into a shared pot. The total amount in the shared pot is doubled and then evenly divided among the 4 players.<br><br>How much would you contribute (0-10)?"
    )

    # Prisoner's Dilemma
    prisoner_choice_A = models.StringField(
        choices=['Cooperate', 'Defect'],
        label=(
            "You and a stranger each choose <strong>cooperate</strong> or <strong>defect</strong>.<br>"
            "- If both <strong>cooperate</strong>: each gets €5.<br>"
            "- If one <strong>defects</strong> and the other <strong>cooperates</strong>: the defector gets €8, the cooperator gets €0.<br>"
            "- If both <strong>defect</strong>: each gets €2.<br>"
            "What would you choose?"
        ),
        widget=widgets.RadioSelect
    )

    prisoner_choice_B = models.StringField(
        choices=['Cooperate', 'Defect'],
        label=(
            "You and a family member each choose <strong>cooperate</strong> or <strong>defect</strong>.<br>"
            "- If both <strong>cooperate</strong>: each gets €5.<br>"
            "- If one <strong>defects</strong> and the other <strong>cooperates</strong>: the defector gets €8, the cooperator gets €0.<br>"
            "- If both <strong>defect</strong>: each gets €2.<br>"
            "What would you choose?"
        ),
        widget=widgets.RadioSelect
    )

    # Coordination Game
    coord_restaurant_choice_A = models.StringField(
        choices=['Täffä', 'Nanapo Sushi'],
        label=(
            "You and a stranger both choose one of two restaurants to meet at: <strong>Täffä</strong> or <strong>Nanapo Sushi</strong>.<br>"
            "- If you choose the same one, you each get €5.<br>"
            "- If you choose different ones, you each get €0.<br>"
            "Which restaurant do you choose?"
        ),
        widget=widgets.RadioSelect
    )
    coord_other_likelihood_A = models.FloatField(
        min=0,
        max=100,
        label="How likely do you think it is that the other player chooses the same restaurant as you (in %, eg. 10 forr 10%)?"
    )
    coord_restaurant_choice_B = models.StringField(
        choices=['Täffä', 'Nanapo Sushi'],
        label=(
            "You and a close friend both choose one of two restaurants to meet at: <strong>Täffä</strong> or <strong>Nanapo Sushi</strong>.<br>"
            "- If you choose the same one, you each get €5.<br>"
            "- If you choose different ones, you each get €0.<br>"
            "Which restaurant do you choose?"
        ),
        widget=widgets.RadioSelect
    )
    coord_other_likelihood_B = models.FloatField(
        min=0,
        max=100,
        label="How likely do you think it is that the other player chooses the same restaurant as you (in %, eg. 10 forr 10%)?"
    )

    # Bertrand Competition
    bertrand_price_A = models.FloatField(
        min=1,
        max=10,
        label="You and another participant (a stranger) are competing firms. You both sell the same product. You each set a price (between €1 and €10). Whoever sets the lower price sells the product and earns that price as profit. If both choose the same price, you split the market.<br><br>What price do you set (1-10)?"
    )
    bertrand_price_B = models.FloatField(
        min=1,
        max=10,
        label="You and a close friend are competing firms. You both sell the same product. You each set a price (between €1 and €10). Whoever sets the lower price sells the product and earns that price as profit. If both choose the same price, you split the market.<br><br>What price do you set (1-10)?"
    )

    # Cournot Competition
    cournot_quantity_A = models.FloatField(
        min=0,
        max=10,
        label=(
            "You and another player (a stranger) are firms deciding how many units to produce (0–10).<br>"
            "- The market price is <strong>€10 minus the total quantity produced by both firms</strong>.<br>"
            "- Your profit = quantity you produce × market price.<br>"
            "How many units would you produce?"
        )
    )

    cournot_quantity_B = models.FloatField(
        min=0,
        max=10,
        label=(
            "You and a close friend are firms deciding how many units to produce (0–10).<br>"
            "- The market price is <strong>€10 minus the total quantity produced by both firms</strong>.<br>"
            "- Your profit = quantity you produce × market price.<br>"
            "How many units would you produce?"
        )
    )


    # SSW Market - questions from periods 1 to 11 are defined dynamically under the Player class.
    ssw_wtp_0_A = models.FloatField(
        min=0,
        max=11*1.85,
        label=(
            "WTP:"
        )
    )
    ssw_wta_0_A = models.FloatField(
        min=0,
        max=11*1.85,
        label="WTA:"
    )
    ssw_wtp_0_B = models.FloatField(
        min=0,
        max=11*1.85,
        label=(
            "WTP:"
        )
)
    ssw_wta_0_B = models.FloatField(
        min=0,
        max=11*1.85,
        label="WTA:"
    )

    # Wisdom of the crowd
    wisdom_michael_A = models.FloatField(
        min=130,
        max=220,
        label="Estimate the height of Michael, Daniel, and Christoph. Please provide your best guess.<br><br>How tall do you think <strong>Michael</strong> is (in centimeters)?"
    )
    wisdom_daniel_A = models.FloatField(
        min=130,
        max=220,
        label="How tall do you think <strong>Daniel</strong> is (in centimeters)?"
    )
    wisdom_christoph_A = models.FloatField(
        min=130,
        max=220,
        label="How tall do you think <strong>Christoph</strong> is (in centimeters)?"
    )
    wisdom_michael_B = models.FloatField(
        min=130,
        max=220,
        label="Estimate the height of Michael, Daniel, and Christoph. Please provide your best guess. <strong>Suggestion</strong>: You could use Google to quickly research likely heights based on the information (like demographics) you have about each of these persons.<br><br>How tall do you think <strong>Michael</strong> is (in centimeters)?"
    )
    wisdom_daniel_B = models.FloatField(
        min=130,
        max=220,
        label="How tall do you think <strong>Daniel</strong> is (in centimeters)?"
    )
    wisdom_christoph_B = models.FloatField(
        min=130,
        max=220,
        label="How tall do you think <strong>Christoph</strong> is (in centimeters)?"
    )


##### Cognitive Limit Box

    cognitiveLimitBox_1_A = models.StringField(
        choices=['A', 'B'],
        widget=widgets.RadioSelect,
        label = (
                    f"For each of the scenarios, please choose between alternative <strong>A</strong> and <strong>B</strong>.<br>"
                    f"For your payment, the computer will select one of the 21 scenarios at random.<br>"
                    f"If you chose <strong>A</strong> in that scenario, you will get whatever is in <strong>A</strong>’s box.<br>"
                    f"If you chose <strong>B</strong> in that scenario, the computer will randomly choose one of <strong>B</strong>’s boxes and you will get whatever is in that box.<br><br>"
                    f"<strong>Scenario 1:</strong><br>"
                    f"<strong>A</strong>. One box containing €0<br>"
                    f"<strong>B</strong>. 87 boxes: 85 boxes €0, 2 boxes €2175"
                )
    )

    cognitiveLimitBox_1_B = models.StringField(
        choices=['A', 'B'],
        widget=widgets.RadioSelect,
        label = (
                    f"For each of the scenarios, please choose between alternative <strong>A</strong> and <strong>B</strong>.<br>"
                    f"For your payment, the computer will select one of the 21 scenarios at random.<br>"
                    f"If you chose <strong>A</strong> in that scenario, you will get whatever is in <strong>A</strong>’s box.<br>"
                    f"If you chose <strong>B</strong> in that scenario, the computer will calculate the average amount in <strong>B</strong>’s boxes<br>"
                    f"and you will get paid that amount.<br><br>"
                    f"<strong>Scenario 1:</strong><br>"
                    f"<strong>A</strong>. One box containing €0<br>"
                    f"<strong>B</strong>. 87 boxes: 85 boxes €0, 2 boxes €2175"
                )
    )


### Cognitive Limit Insurance


    cognitiveLimitInsurance = models.StringField(
        choices=['plan A', 'plan B'],
        widget=widgets.RadioSelect,
        label="Which plan would you choose?"
    )

    Demographics_Age = models.PositiveIntegerField(blank=True, label='What is your age?', min=1, max=130, )
    Demographics_Sex = models.IntegerField(
        blank=True,
        initial=None,
        choices=[
            [1, 'Male'],
            [2, 'Female'],
            [3, 'Other'],
            [4, 'Prefer not to say'],
        ],
        verbose_name='What is your gender?',
        widget=widgets.RadioSelectHorizontal(),
    )
    Demographics_FinInterest = models.PositiveIntegerField(
        blank=True,
        label='Are you interested in financial markets? Please select a category between 1 ("not at all") and 7 ("very much").',
        choices=range(1, 8),
        initial=None,
        widget=widgets.RadioSelectHorizontal(),
    )
    Demographics_Investor = models.IntegerField(
        blank=True,
        initial=None,
        verbose_name='Do you own stocks or mutual funds?',
        choices=[
            [0, 'No'],
            [1, 'Yes'],
        ],
    )
    Demographics_InvestorHistory = models.IntegerField(
        blank=True,
        initial=None,
        verbose_name='Have you ever owned stocks or mutual funds?',
        choices=[
            [0, 'No'],
            [1, 'Yes'],
        ],
    )
    Demographics_InvestorExperience = models.LongStringField(
        blank=True,
        initial=None,
        label='Please briefly describe your experience with stock or fund investing. If you do not invest (anymore), please describe why.',
    )
    Demographics_FinanceProf = models.IntegerField(
        blank=True,
        initial=None,
        verbose_name='Have you ever had a job in the financial industry?',
        choices=[
            [0, 'No'],
            [1, 'Yes'],
        ],
    )
    Demographics_RiskAffinity = models.PositiveIntegerField(
        blank=True,
        verbose_name='Please assess your willingness to take financial risks. Select a category between 1 ("Not willing to take financial risks") and 5 ("Willing to take large risks to achieve a significant gain").',
        choices=range(1, 6),
        initial=None,
        widget=widgets.RadioSelectHorizontal(),
    )
    Demographics_Percentages = models.PositiveIntegerField(
        blank=True,
        verbose_name='Please assess the following statement: “I am good at working with percentages.”',
        initial=None,
        widget=widgets.RadioSelectHorizontal(),
        choices=[
            [1, "1 - Strongly disagree"],
            [2, "2"],
            [3, "3"],
            [4, "4"],
            [5, "5 - Strongly agree"],
        ],
    )
    Demographics_Intuition = models.PositiveIntegerField(
        blank=True,
        verbose_name='Please assess the following statement: “I make many of my decisions on the basis of intuition.”',
        initial=None,
        widget=widgets.RadioSelectHorizontal(),
        choices=[
            [1, "1 - Strongly disagree"],
            [2, "2"],
            [3, "3"],
            [4, "4"],
            [5, "5 - Strongly agree"],
        ],
    )
    Demographics_IdeasVsFacts = models.PositiveIntegerField(
        blank=True,
        verbose_name='Please assess the following statement: “I am more at home with ideas rather than facts and figures.”',
        initial=None,
        widget=widgets.RadioSelectHorizontal(),
        choices=[
            [1, "1 - Strongly disagree"],
            [2, "2"],
            [3, "3"],
            [4, "4"],
            [5, "5 - Strongly agree"],
        ],
    )
    Demographics_AnalysisVsInsights = models.PositiveIntegerField(
        blank=True,
        verbose_name='Please assess the following statement: “My understanding of a problem tends to come more from thorough analysis than flashes of insight.”',
        initial=None,
        widget=widgets.RadioSelectHorizontal(),
        choices=[
            [1, "1 - Strongly disagree"],
            [2, "2"],
            [3, "3"],
            [4, "4"],
            [5, "5 - Strongly agree"],
        ],
    )
    # -----------------------------------------
    # Understanding of diversification benefits
    # -----------------------------------------
    ######## Financial litercy test ###############
    interest_rate_inflation = models.PositiveIntegerField(
        blank=True,
        initial=None,
        label='Imagine that the interest rate on your savings account was 1% per year and inflation was 2% per year. After 1 year, would you be able to buy:',
        widget=widgets.RadioSelect,
        choices=[
            [1, f"More than today with the money in this account (£1,000)"],
            [2, f"Exactly the same as today with the money in this account (£1,000)"],
            [3, f"Less than today with the money in this account (£1,000)"],
            [4, "Don’t know"],
            [5, "Refuse to answer"],
        ],
    )
    bonds_riskier = models.PositiveIntegerField(
        blank=True,
        initial=None,
        label='Do you think that the following statement is true or false? “Bonds are normally riskier than stocks.”',
        widget=widgets.RadioSelect,
        choices=[[1, "True"], [2, "False"], [3, "Don’t know"], [4, "Refuse to answer"]],
    )
    highest_return_asset = models.PositiveIntegerField(
        blank=True,
        initial=None,
        label='Considering a long time period (for example, 10 or 20 years), which asset class described below would normally give the highest return?',
        widget=widgets.RadioSelect,
        choices=[
            [1, "Savings accounts"],
            [2, "Stocks"],
            [3, "Bonds"],
            [4, "Don’t know"],
            [5, "Refuse to answer"],
        ],
    )
    highest_fluctuations_asset = models.PositiveIntegerField(
        blank=True,
        initial=None,
        label='Normally, which asset class described below displays the highest fluctuations over time?',
        widget=widgets.RadioSelect,
        choices=[
            [1, "Savings accounts"],
            [2, "Stocks"],
            [3, "Bonds"],
            [4, "Don’t know"],
            [5, "Refuse to answer"],
        ],
    )
    risk_spreading_money = models.PositiveIntegerField(
        blank=True,
        initial=None,
        label='When an investor spreads their money among different assets, the risk of losing a lot of money:',
        widget=widgets.RadioSelect,
        choices=[
            [1, "Increases"],
            [2, "Decreases"],
            [3, "Stays the same"],
            [4, "Don’t know"],
            [5, "Refuse to answer"],
        ],
    )
    stock_mutual_fund = models.PositiveIntegerField(
        blank=True,
        initial=None,
        label='Do you think that the following statement is true or false? “A stock mutual fund combines the money of many investors to buy a variety of stocks.”',
        widget=widgets.RadioSelect,
        choices=[[1, "True"], [2, "False"], [3, "Don’t know"], [4, "Refuse to answer"]],
    )
    invest_mutual_fund = models.PositiveIntegerField(
        blank=True,
        initial=None,
        label=f'Do you think that the following statement is true or false? “If you were to invest £1,000 in a stock mutual fund, it would be possible to have less than £1,000 when you withdraw your money.”',
        widget=widgets.RadioSelect,
        choices=[[1, "True"], [2, "False"], [3, "Don’t know"], [4, "Refuse to answer"]],
    )

    mortgage_payment = models.PositiveIntegerField(
        blank=True,
        initial=None,
        label='Do you think that the following statement is true or false? “A 15-year mortgage typically requires higher monthly payments than a 30-year mortgage, but the total interest paid over the life of the loan will be less.”',
        widget=widgets.RadioSelect,
        choices=[[1, "True"], [2, "False"], [3, "Don’t know"], [4, "Refuse to answer"]],
    )
    savings_interest = models.PositiveIntegerField(
        blank=True,
        initial=None,
        label=f'Suppose you have £100 in a savings account and the interest rate is 20% per year and you never withdraw money or interest payments. After 5 years, how much would you have in this account in total?',
        widget=widgets.RadioSelect,
        choices=[
            [1, f"More than £200"],
            [2, f"Exactly £200"],
            [3, f"Less than £200"],
            [4, "Don’t know"],
            [5, "Refuse to answer"],
        ],
    )
    mutual_fund_statement = models.PositiveIntegerField(
        blank=True,
        initial=None,
        label='Which of the following statements is correct?',
        widget=widgets.RadioSelect,
        choices=[
            [
                1,
                "Once one invests in a mutual fund, one cannot withdraw the money in the first year",
            ],
            [
                2,
                "Mutual funds can invest in several assets, for example invest in both stocks and bonds",
            ],
            [
                3,
                "Mutual funds pay a guaranteed rate of return which depends on their past performance",
            ],
            [4, "None of the above"],
            [5, "Don’t know"],
            [6, "Refuse to answer"],
        ],
    )
    bond_purchase = models.PositiveIntegerField(
        blank=True,
        initial=None,
        label='Which of the following statements is correct? If somebody buys a bond of firm B:',
        widget=widgets.RadioSelect,
        choices=[
            [1, "They own a part of firm B"],
            [2, "They have lent money to firm B"],
            [3, "They are liable for firm B’s debts"],
            [4, "None of the above"],
            [5, "Don’t know"],
            [6, "Refuse to answer"],
        ],
    )
    credit_card_debt = models.PositiveIntegerField(
        blank=True,
        initial=None,
        label=f'Suppose you owe £3,000 on your credit card. You pay a minimum payment of £30 each month. At an annual percentage rate of 12% (or 1% per month), how many years would it take to eliminate your credit card debt if you made no additional new charges?',
        widget=widgets.RadioSelect,
        choices=[
            [1, "Less than 5 years"],
            [2, "Between 5 and 10 years"],
            [3, "Between 10 and 15 years"],
            [4, "Never"],
            [5, "Don’t know"],
            [6, "Refuse to answer"],
        ],
    )
    # -----------------------------------------
    # Faith-in-Intuition Score (Epstein et al., 1996)
    # -----------------------------------------
    faith1 = models.PositiveIntegerField(
        blank=True,
        initial=None,
        label='My initial impressions of people are almost always right.',
        widget=widgets.RadioSelectHorizontal(),
        choices=[
            [1, "1 - Completely False"],
            [2, "2"],
            [3, "3"],
            [4, "4"],
            [5, "5 - Completely True"],
        ],
    )
    faith2 = models.PositiveIntegerField(
        blank=True,
        initial=None,
        label='I trust my initial feelings about people.',
        widget=widgets.RadioSelectHorizontal(),
        choices=[
            [1, "1 - Completely False"],
            [2, "2"],
            [3, "3"],
            [4, "4"],
            [5, "5 - Completely True"],
        ],
    )
    faith3 = models.PositiveIntegerField(
        blank=True,
        initial=None,
        label='When it comes to trusting people, I can usually rely on my "gut feelings."',
        widget=widgets.RadioSelectHorizontal(),
        choices=[
            [1, "1 - Completely False"],
            [2, "2"],
            [3, "3"],
            [4, "4"],
            [5, "5 - Completely True"],
        ],
    )
    faith4 = models.PositiveIntegerField(
        blank=True,
        initial=None,
        label='I believe in trusting my hunches.',
        widget=widgets.RadioSelectHorizontal(),
        choices=[
            [1, "1 - Completely False"],
            [2, "2"],
            [3, "3"],
            [4, "4"],
            [5, "5 - Completely True"],
        ],
    )
    faith5 = models.PositiveIntegerField(
        blank=True,
        initial=None,
        label='I can usually feel when a person is right or wrong even if I cannot explain how I know.',
        widget=widgets.RadioSelectHorizontal(),
        choices=[
            [1, "1 - Completely False"],
            [2, "2"],
            [3, "3"],
            [4, "4"],
            [5, "5 - Completely True"],
        ],
    )
    faith6 = models.PositiveIntegerField(
        blank=True,
        initial=None,
        label='I am a very intuitive person.',
        widget=widgets.RadioSelectHorizontal(),
        choices=[
            [1, "1 - Completely False"],
            [2, "2"],
            [3, "3"],
            [4, "4"],
            [5, "5 - Completely True"],
        ],
    )
    faith7 = models.PositiveIntegerField(
        blank=True,
        initial=None,
        label='I can typically sense right away when a person is lying.',
        widget=widgets.RadioSelectHorizontal(),
        choices=[
            [1, "1 - Completely False"],
            [2, "2"],
            [3, "3"],
            [4, "4"],
            [5, "5 - Completely True"],
        ],
    )
    faith8 = models.PositiveIntegerField(
        blank=True,
        initial=None,
        label='I am quick to form impressions about people.',
        widget=widgets.RadioSelectHorizontal(),
        choices=[
            [1, "1 - Completely False"],
            [2, "2"],
            [3, "3"],
            [4, "4"],
            [5, "5 - Completely True"],
        ],
    )
    faith9 = models.PositiveIntegerField(
        blank=True,
        initial=None,
        label='I believe I can judge character pretty well from a person`s appearance.',
        widget=widgets.RadioSelectHorizontal(),
        choices=[
            [1, "1 - Completely False"],
            [2, "2"],
            [3, "3"],
            [4, "4"],
            [5, "5 - Completely True"],
        ],
    )
    faith10 = models.PositiveIntegerField(
        blank=True,
        initial=None,
        label='I often have clear visual images of things.',
        widget=widgets.RadioSelectHorizontal(),
        choices=[
            [1, "1 - Completely False"],
            [2, "2"],
            [3, "3"],
            [4, "4"],
            [5, "5 - Completely True"],
        ],
    )
    faith11 = models.PositiveIntegerField(
        blank=True,
        initial=None,
        label='I have a very good sense of rhythm.',
        widget=widgets.RadioSelectHorizontal(),
        choices=[
            [1, "1 - Completely False"],
            [2, "2"],
            [3, "3"],
            [4, "4"],
            [5, "5 - Completely True"],
        ],
    )
    faith12 = models.PositiveIntegerField(
        blank=True,
        initial=None,
        label='I am good at visualizing things.',
        widget=widgets.RadioSelectHorizontal(),
        choices=[
            [1, "1 - Completely False"],
            [2, "2"],
            [3, "3"],
            [4, "4"],
            [5, "5 - Completely True"],
        ],
    )

    overconfidence1 = models.FloatField(
        blank=True,
        initial=None,
        min=0,
        max=100,
        label="You're in a large group of people playing a new game. You don't know how your ability compares to other people's. You play one game against a randomly selected person and win. What percentage of people do you think you're better than (in %, eg. 10 for 10%)?",
    )
    overconfidence2 = models.FloatField(
        blank=True,
        initial=None,
        min=0,
        max=100,
        label="Imagine you're on a committee deciding between 5 different project options. There are 10 members of the committee. You propose Option A. The next three committee members propose Option B. The six other committee members will propose their choice next. When the meeting is finished, what percentage of the choices do you think will be Option A (in %, eg. 10 for 10%)?",
    )
    overconfidence3 = models.FloatField(
        blank=True,
        initial=None,
        min=0,
        max=100,
        label="One hundred people are guessing the number of jellybeans in a jar. The closest 10 guesses win $100. How likely are you to be one of the winners (in %, eg. 10 for 10%)?",
    )

## Define cognitive limit investments fields dynamically    
for i in range(1, C.CATEGORIES["CognitiveLimitInvestment"] + 1):
    field_name = f'CognitiveLimitInvestment_{i}'
    field = models.StringField(
        label="Which asset do you choose to invest in?",
        choices=["Asset A", "Asset B"],
        widget=widgets.RadioSelect
    )
    setattr(Player, field_name, field)
    field_opinion_name = f'CognitiveLimitInvestmentOpinion_{i}'
    field_opinion = models.StringField(
        label="Which asset do you expect to have higher expected return?",
        choices=["Asset A", "Asset B", "Same Expected Return"],
        widget=widgets.RadioSelect
    )
    setattr(Player, field_opinion_name, field_opinion)

## Define boxes questions dynamically
for i in range(2, 22):
    field_name = f'cognitiveLimitBox_{i}'
    field = models.StringField(
        choices=['A', 'B'],
        widget=widgets.RadioSelect,
        label = (
                    f"<strong>Scenario {i}:</strong><br>"
                    f"<strong>A</strong>. One box containing €{(i-1)*45}<br>"
                    f"<strong>B</strong>. 87 boxes: 85 boxes €0, 2 boxes €2175"
                )
    )
    setattr(Player, field_name, field)

## Define Investment Trust questions dynamically
for amount in range(3, 31, 3):
    setattr(
        Player,
        f"trust_return_{amount}_A",
        models.FloatField(
            min=0,
            max=amount,
            label=f"You are Player 2. Suppose you receive €{amount}. How much would you return?"
        ),
    )
    setattr(
        Player,
        f"trust_return_{amount}_B",
        models.FloatField(
            min=0,
            max=amount,
            label=f"You are Player 2. Suppose you receive €{amount}. How much would you return?"
        ),
    )

## Define WTP/WTA dynamically
for period in range(1, 12):
    setattr(
        Player,
        f"ssw_wtp_{period}_A",
        models.FloatField(
            min=0,
            max=11*1.85,
            label= (
                "WTP:"
            )
            
        ),
    )
    setattr(
        Player,
        f"ssw_wtp_{period}_B",
        models.FloatField(
            min=0,
            max=11*1.85,
            label=(
                    "WTP:"
                )
        ),
    )
    setattr(
        Player,
        f"ssw_wta_{period}_A",
        models.FloatField(
            min=0,
            max=11*1.85,
            label=f"WTA:"
        ),
    )
    setattr(
        Player,
        f"ssw_wta_{period}_B",
        models.FloatField(
            min=0,
            max=11*1.85,
            label=f"WTA:"
        ),
    )
def creating_session(subsession: Subsession):
    if subsession.round_number == 1:
        players = subsession.get_players()
        num_players = len(players)

        # Generate a balanced assignment for each question
        # This is done once per question
        question_to_assignments = {}
        for question_name in C.PAGES:
            half = num_players // 2
            assignments = ["A"] * half + ["B"] * half
            if num_players % 2 != 0:
                # If odd number of players, assign last randomly
                assignments.append(random.choice(["A", "B"]))
            random.shuffle(assignments)
            question_to_assignments[question_name] = assignments


        for p in subsession.get_players():
            i=1
            index = p.participant.id_in_session - 1
            ## Assign group A or B
            nof_groups = len(C.GROUPS)
            player_assignment = {}
            for question_name, assignment_list in question_to_assignments.items():
                player_assignment[question_name] = assignment_list[index]

            p.participant.vars["question_groups"] = player_assignment
            ## Creating the dict from page to question names with groups for easier access by the teachers
            question_group_assignments = {}
            for page, questions in C.PAGES_TO_QUESTIONS.items():
                question_group_assignments[page] = [f"{q}_{player_assignment[page]}" for q in questions]
            question_group_assignments["CognitiveLimitInvestment"] = C.OTHER_PAGES_TO_QUESTIONS["CognitiveLimitInvestment"]
            question_group_assignments["CognitiveLimitBox"] = [C.OTHER_PAGES_TO_QUESTIONS["CognitiveLimitBox"][0] + "_" +  player_assignment["CognitiveLimitBox"]] + C.OTHER_PAGES_TO_QUESTIONS["CognitiveLimitBox"][1:]
            question_group_assignments["CognitiveLimitInsurance"] = C.OTHER_PAGES_TO_QUESTIONS["CognitiveLimitInsurance"]

            #save_data(p, json.dumps(player_assignment), 'page_groups', i)
            #save_data(p, json.dumps(question_group_assignments), 'question_groups', i)

            ## Get corresponding rows in the data for CognitiveLimitInvestmentPage
            nof_rows = C.CATEGORIES["CognitiveLimitInvestment"]
            start_row_idx = (index // nof_groups) * nof_rows
            end_row_idx = start_row_idx + nof_rows
            p.participant.vars["datarows"] =  list(range(start_row_idx,end_row_idx))

            save_data(p, json.dumps(p.participant.vars["datarows"] ), 'datarows', i)

            ## Randomize question pages orders (only experiments switched on)
            question_pages = list(C.PAGES_TO_QUESTIONS.keys())
            indices = [i for i, page in enumerate(question_pages) if experiment_enabled(subsession.session, page)]
            random.shuffle(indices)
            shuffled_pages = [question_pages[i] for i in indices]
            p.participant.vars["question_pages"] = shuffled_pages
            p.participant.vars["question_pages_indices"] = indices
            #save_data(p, json.dumps(p.participant.vars["question_pages_indices"] ), 'question_pages_order', i)

def save_data(player: Player, data, page_name, round_number_to_save):
    desired_round_player = player.in_round(round_number_to_save)
    setattr(desired_round_player, page_name, data)

def experiment_enabled(session, page_name):
    return bool(session.config.get(C.PAGE_TO_TOGGLE[page_name], True))

def category_rounds(category):
    start = C.CATEGORY_START_INDEX[category]
    return list(range(start + 1, start + C.CATEGORIES[category] + 1))

def page_progress(player: Player):
    ## "Page X of Y" counting only the rounds this participant actually sees
    rounds = category_rounds("Instruction")
    rounds += category_rounds("Question")[:len(player.participant.vars["question_pages"])]
    for category in ["CognitiveLimitInvestment", "CognitiveLimitBox", "CognitiveLimitInsurance"]:
        if experiment_enabled(player.session, category):
            rounds += category_rounds(category)
    rounds += category_rounds("Survey")
    return {'page_num': rounds.index(player.round_number) + 1,
            'total_pages': len(rounds)}


## PAGES 




class Base1(Page):
    form_model = "player"


class Instructions_WelcomeScreen(Base1):
    form_fields = ['browser_first','first_name', 'last_name', 'student_number', 'isLeaving']
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1
    """
    @staticmethod
    def vars_for_template(player: Player):
        return {
                'testing': player.session.config["testing"], }
    """
    
    @staticmethod
    def error_message(player: Player, values):
        if values['isLeaving'] == False:
            student_number = values.get('student_number')
            last_name = values.get('last_name')
            first_name = values.get('first_name')
            err_string = ""
            if last_name == "":
                err_string += 'Please enter your last name.\n'
                return err_string
            if first_name == "":
                err_string += 'Please enter your first name.\n'
                return err_string
            if student_number == "":
                err_string += 'Please enter your student number.\n'
                return err_string

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        i = 1
        save_data(player, player.browser_first, 'browser_first', i)
        save_data(player, player.student_number, 'student_number', i)
        save_data(player, player.first_name, 'first_name', i)
        save_data(player, player.last_name, 'last_name', i)

    @staticmethod
    def vars_for_template(player: Player):
        return page_progress(player)

class LeavePage(Page):
    template_name = 'design_exp/LeavePage.html'
    @staticmethod
    def is_displayed(player: Player):
        return player.isLeaving
    
class CognitiveLimitInvestmentPage(Base1):
    @staticmethod
    def is_displayed(player: Player):
        # Show only after instructions round 1
        return player.round_number in category_rounds("CognitiveLimitInvestment") and experiment_enabled(player.session, "CognitiveLimitInvestment")

    @staticmethod
    def get_form_fields(player):
        index = player.round_number - C.CATEGORY_START_INDEX["CognitiveLimitInvestment"] - 1
        field = f"CognitiveLimitInvestment_{index+1}"
        field_opinion = f"CognitiveLimitInvestmentOpinion_{index+1}"
        return [field, field_opinion]
    
    @staticmethod
    def vars_for_template(player: Player):
        index = player.round_number - C.CATEGORY_START_INDEX["CognitiveLimitInvestment"] - 1
        group = player.participant.vars["question_groups"]["CognitiveLimitInvestment"]
        datarows = player.participant.vars["datarows"]
        if group == 'A':
            retA = C.RETA.iloc[datarows[index]].tolist()
            retAToShow = [retA[i] * 100 for i in (range(len(retA)))]
            retB = C.RETB.iloc[datarows[index]].tolist()
            retBToShow = [retB[i] * 100 for i in (range(len(retB)))]

            axisLabel = str("Annual Return      (since start of this year)") 
        else:
            retA = C.CUMRETA.iloc[datarows[index]].tolist()
            retAToShow = [retA[i] * 100 for i in (range(len(retA)))]
            retB = C.CUMRETB.iloc[datarows[index]].tolist()
            retBToShow = [retB[i] * 100 for i in (range(len(retB)))]
            axisLabel = str("Cumulative Return (since start of Year 1)")
        return {
            'testing': player.session.config["testing"],
            'group': group,
            **page_progress(player),
            'array1': retAToShow, # Returns used for display
            'array2': retBToShow, # Returns used for display
            'ar1name': 'AssetA',
            'ar2name': 'AssetB',
            'animation_time': 0,
            'yAxisLabel': axisLabel,
            'max_value': max(retAToShow + retBToShow)
        }
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        i = player.round_number
        index = player.round_number - C.CATEGORY_START_INDEX["CognitiveLimitInvestment"] - 1
        field = f"CognitiveLimitInvestment_{index+1}"
        field_opinion = f"CognitiveLimitInvestmentOpinion_{index+1}"
        group = player.participant.vars["question_groups"]["CognitiveLimitInvestment"]
        save_data(player, group, "experiment_group", i)
        save_data(player, C.QUESTION_IDS["CognitiveLimitInvestment"], "question", i)
        save_data(player, getattr(player, field),
                  field, i)
        save_data(player, getattr(player, field_opinion),
                  field_opinion, i)
    
class QuestionPage(Base1):
    @staticmethod
    def is_displayed(player: Player):
        # Show only after instructions round 1; question_pages holds only the experiments switched on
        index = player.round_number - C.CATEGORY_START_INDEX["Question"] - 1
        return 0 <= index < len(player.participant.vars["question_pages"])

    
    @staticmethod
    def get_form_fields(player):
        
        index = player.round_number - C.CATEGORY_START_INDEX["Question"] - 1
        page_name = player.participant.vars["question_pages"][index]

        group = player.participant.vars["question_groups"][page_name]

        fields = C.PAGES_TO_QUESTIONS[page_name]
        fields_with_group = [field + "_" + group for field in fields]
        return fields_with_group
    
    @staticmethod
    def vars_for_template(player: Player):
        index = player.round_number - C.CATEGORY_START_INDEX["Question"] - 1
        page_name = player.participant.vars["question_pages"][index]
        group = player.participant.vars["question_groups"][page_name]
            
        if page_name in C.PAGES_wITH_IMAGES.keys():
            has_image = True
            image = C.PAGES_wITH_IMAGES[page_name]
        else:
            has_image = False
            image = ""
        
        return {
                'has_image' : has_image,
                'image' : image,
                **page_progress(player),
                'page_name': page_name,
                'group': group,
            }
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        index = player.round_number - C.CATEGORY_START_INDEX["Question"] - 1
        page_name = player.participant.vars["question_pages"][index]

        group = player.participant.vars["question_groups"][page_name]

        fields = C.PAGES_TO_QUESTIONS[page_name]
        fields_with_group = [field + "_" + group for field in fields]
        i=player.round_number
        save_data(player, group, "experiment_group", i)
        save_data(player, C.QUESTION_IDS[page_name], "question", i)

        for field in fields_with_group:
            save_data(player, getattr(player, field),
                  field, i)
    
class CognitiveLimitBoxPage(Base1):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number in category_rounds("CognitiveLimitBox") and experiment_enabled(player.session, "CognitiveLimitBox")

    @staticmethod
    def get_form_fields(player):
        group = player.participant.vars["question_groups"]["CognitiveLimitBox"]

        fields = [f'cognitiveLimitBox_1_{group}']
        fields = fields + [f"cognitiveLimitBox_{i}" for i in range(2,22)]
        return fields


    def vars_for_template(player: Player):
        return page_progress(player)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        group = player.participant.vars["question_groups"]["CognitiveLimitBox"]

        fields = [f'cognitiveLimitBox_1_{group}']
        fields = fields + [f"cognitiveLimitBox_{i}" for i in range(2,22)]
        i= player.round_number
        save_data(player, group, "experiment_group", i)
        save_data(player, C.QUESTION_IDS["CognitiveLimitBox"], "question", i)
        for field in fields:
            save_data(player, getattr(player, field),
                  field, i)
    

class CognitiveLimitInsurancePage(Base1):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number in category_rounds("CognitiveLimitInsurance") and experiment_enabled(player.session, "CognitiveLimitInsurance")

    form_fields = ['cognitiveLimitInsurance']

    def vars_for_template(player: Player):
        return {'experimentGroup': player.participant.vars["question_groups"]["CognitiveLimitInsurance"],
                **page_progress(player)}
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        i= player.round_number
        group = player.participant.vars["question_groups"]["CognitiveLimitInsurance"]
        save_data(player, group, "experiment_group", i)
        save_data(player, C.QUESTION_IDS["CognitiveLimitInsurance"], "question", i)
        save_data(player, getattr(player, "cognitiveLimitInsurance"),
                "cognitiveLimitInsurance", i)
    
class SurveyPage(Base1):
    template_name = 'design_exp/SurveyPage.html'

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number >= C.CATEGORY_START_INDEX["Survey"] + 1 and player.round_number < C.CATEGORY_START_INDEX["Survey"] + C.CATEGORIES["Survey"] + 1

    @staticmethod
    def get_form_fields(player: Player):
        index = player.round_number - C.CATEGORY_START_INDEX["Survey"] - 1
        return C.survey_pages[index]['form_fields']

    @staticmethod
    def vars_for_template(player: Player):
        return page_progress(player)
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        index = player.round_number - C.CATEGORY_START_INDEX["Survey"] - 1

        fields = C.survey_pages[index]['form_fields']
        i=1
        for field in fields:
            value = player.field_maybe_none(field)
            if value is not None:
                save_data(player, value, field, i)
            i += 1
    
class ThanksPage(Base1):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

page_sequence = [Instructions_WelcomeScreen,
                 LeavePage,
                 QuestionPage,
                 CognitiveLimitInvestmentPage,
                 CognitiveLimitBoxPage,
                 CognitiveLimitInsurancePage,
                 SurveyPage,
                 ThanksPage
                 ]