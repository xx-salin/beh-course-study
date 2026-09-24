from os import environ

# On/off switch per experiment (True = shown, False = skipped).
# Keys must match C.EXPERIMENT_TOGGLES in design_exp/__init__.py.
# Also editable per session under "Configure session" in the admin.
EXPERIMENT_SWITCHES = dict(
    E01_ConjunctionFallacy=True,
    E02_GamblersFallacy=True,
    E03_HotHandFallacy=True,
    E05_BaseRateFallacy=True,
    E06_IllusionofControl=True,
    E07_AnchoringEffect=True,
    E08_HindsightBias=True,
    E09_PresentBias=True,
    E10_LossAversion=True,
    E11_EndowmentEffect=True,
    E12_DecoyEffect=True,
    E13_FramingEffect=True,
    E14_StatusQuoBias=True,
    E15_SunkCostFallacy=True,
    E16_MentalAccounting=True,
    E17_UltimatumGame=True,
    E18_DictatorGame=True,
    E19_TrustInvestmentGame=True,
    E20_PublicGoodsGame=True,
    E21_PrisonersDilemma=True,
    E22_CoordinationGame=True,
    E23_BertrandCompetition=True,
    E24_CournotCompetition=True,
    E25_SSWMarket=True,
    E26_WisdomofCrowd=True,
    E27_30_CountingHeuristic=True,
    E31_DeterministicMirror=True,
    E32_InsurancePlan=True,
)

# Order of the experiment pages.
# True  = random order per participant (default).
# False = fixed order, exactly as listed in C.PAGES_TO_QUESTIONS
RANDOMIZE_EXPERIMENT_ORDER = False

SESSION_CONFIGS = [
    dict(
        name='design_exp',
         app_sequence=['design_exp'],
         num_demo_participants=2,
         testing = True,
         randomize_experiment_order=RANDOMIZE_EXPERIMENT_ORDER,
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
