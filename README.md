# Challenge
Tests to check several endpoint of the test service (API docs https://reqres.in/)

<b>Endpoints to verify:</b>
https://reqres.in/api/users
https://reqres.in/api/users/{id}

<b>Checklist is here</b> 
https://docs.google.com/spreadsheets/d/1G0GwfdGZFxHw7pk2FUmShdH91QXZsEse65-bbTDL0GQ/edit?usp=sharing

<b>How to run tests</b>
<p>python -m pytest --alluredir=test_results/ tests/</p>


<b>How to generate allure report</b>
<p>allure serve test_results</p>
