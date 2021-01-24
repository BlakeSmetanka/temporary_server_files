import json

landing_page = {}
with open("Pages/landingPage.json") as json_file:
        landing_page = json.load(json_file)

contact_page = {}
with open("Pages/contactPage.json") as json_file:
        contact_page = json.load(json_file)

about_page = {}
with open("Pages/aboutPage.json") as json_file:
        about_page = json.load(json_file)

reservation_page = {}
with open("Pages/Student/reservationsPage.json") as json_file:
        reservation_page = json.load(json_file)
