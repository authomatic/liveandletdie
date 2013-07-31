Feature: Visit homepage
	In order to check whether the site actually works
	As a visitor
	I want to visit the website

	Scenario: Homepage showing "Home"
		Given a website running at "http://localhost:8001"
		When I go to that location
		Then I see "Home"