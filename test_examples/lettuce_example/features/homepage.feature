Feature: Visit homepage
	In order to check whether the site actually works
	As a visitor
	I want to visit the website

	Scenario Outline: Homepage working
		Given a web application based on <framework> located at <path>
		When I launch that application wit the subcommand <subcommand> with <ssl>
		When I go to the app's url
		Then I see "<text>"
	
	Examples:
		| framework				| path				| subcommand				| text			    | ssl   |
		| Flask					| flask/main.py		| 							| Home Flask	    | no    |
		| Flask 				| flask/main.py		| 							| Home Flask SSL	| yes	|
		| GAE					| gae				| venv/bin/dev_appserver	| Home GAE		    | no	|
		| Django				| django/example	| 							| Home Django	    | no	|
		| WsgirefSimpleServer	| pyramid/main.py	| 							| Home Pyramid	    | no	|