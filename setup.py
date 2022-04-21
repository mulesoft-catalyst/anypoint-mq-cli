from setuptools import setup

setup(
    name='mq',
    version='0.1',
    py_modules=['mq'],
    include_package_data=True,
    install_requires=[
        'Click', 'Requests', 'jsonlib-python3', 'pymemcache', 'python-memcached'
    ],
    entry_points='''
        [console_scripts]
        mq=mq:cli
    ''',
)
