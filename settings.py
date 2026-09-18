from os import environ

# On/off switch per experiment (True = shown, False = skipped).
# Keys must match C.EXPERIMENT_TOGGLES in design_exp/__init__.py.
# Also editable per session under "Configure session" in the admin.
EXPERIMENT_SWITCHES = dict(
    E01_ConjunctionFallacy=False,
    E02_GamblersFallacy=False,
    E03_HotHandFallacy=False,
    E05_BaseRateFallacy=False,
    E06_IllusionofControl=False,
    E07_AnchoringEffect=False,
    E08_HindsightBias=False,
    E09_PresentBias=False,
    E10_LossAversion=False,
    E11_EndowmentEffect=False,
    E12_DecoyEffect=False,
    E13_FramingEffect=False,
    E14_StatusQuoBias=False,
    E15_SunkCostFallacy=False,
    E16_MentalAccounting=False,
    E17_UltimatumGame=False,
    E18_DictatorGame=False,
    E19_TrustInvestmentGame=False,
    E20_PublicGoodsGame=False,
    E21_PrisonersDilemma=False,
    E22_CoordinationGame=False,
    E23_BertrandCompetition=False,
    E24_CournotCompetition=False,
    E25_SSWMarket=False,
    E26_WisdomofCrowd=False,
    E27_30_CountingHeuristic=False,
    E31_DeterministicMirror=True,
    E32_InsurancePlan=False,
)

SESSION_CONFIGS = [
    dict(
        name='design_exp',
         app_sequence=['design_exp'],
         num_demo_participants=2,
         testing = True,
         **EXPERIMENT_SWITCHES,
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = []
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '9804803664040'
