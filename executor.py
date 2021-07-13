import os

stream = os.popen('coverage run -m unittest unit_tests.py -v')
output = stream.read()
stream = os.popen('coverage html app.py ./models/*.py ./resources/*.py ./schemas/*.py sql_alchemy.py blacklist.py ma.py unit_tests.py')
output = stream.read()