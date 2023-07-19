from os import environ
SESSION_CONFIG_DEFAULTS = dict(real_world_currency_per_point=0.5, participation_fee=5)
#app_sequence- change to 'pg_T2', 'pg_T3' and 'pg_T4' if you want to run those treatments.
SESSION_CONFIGS = [
                dict(name='my_sessionT2', num_demo_participants=4, app_sequence=['pg_T2',
                                                                                'survey']),
                dict(name='my_sessionT3', num_demo_participants=4, app_sequence=['pg_T3',
                                                                                'survey']),
                dict(name='my_sessionT4', num_demo_participants=4, app_sequence=['pg_T4',
                                                                                'survey'])]


                
LANGUAGE_CODE = 'en'
REAL_WORLD_CURRENCY_CODE = 'GBP'
USE_POINTS = True
POINTS_CUSTOM_NAME='tokens'
DEMO_PAGE_INTRO_HTML = ''
PARTICIPANT_FIELDS = ['selected_round']
SESSION_FIELDS = ['my_round']
ROOMS = [
    dict(
        name='test',
        display_name='test',
        participant_label_file='_rooms/Lexel_labels.txt',
        use_secure_urls=False
    ),
    dict(
        name='LEXEL',
        display_name='LEXEL',
        participant_label_file='_rooms/Lexel_labels.txt',
        use_secure_urls=False
    ),
]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

SECRET_KEY = 'blahblah'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']


