# Challenge
Tests to check several endpoint of the test service (API docs https://reqres.in/)

<b>Endpoints to verify:</b>
https://reqres.in/api/users
https://reqres.in/api/users/{id}

<b>Checklist is here</b> 
https://docs.google.com/spreadsheets/d/1G0GwfdGZFxHw7pk2FUmShdH91QXZsEse65-bbTDL0GQ/edit?usp=sharing

How to run tests
python -m pytest --alluredir=test_results/ tests/


How to generate allure report
allure serve test_results
