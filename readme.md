ValTracker is a small Valorant esports backend that

talks to a third party Valorant stats API
talks to your Supabase database
exposes a simple web API so a front end or Swagger UI can use those features


It focuses on three main things

Look up recent matches for a team
Save and list favorite teams in the cloud
Generate a recap report for a team

Plus a small bonus route that returns a Google Maps embed for an event location.


How to Run this project:

in Command Prompt(Microsoft Windows), cd to Valtracker Folder:
pip install -r requirements.txt
cp .env.example .env
python -m uvicorn app.main:api --reload

Application Will start. After startup completion, open a web browser and go to http://127.0.0.1:8000/docs.



1. GET /health

Very simple check

Returns {"ok": true} when the app is alive

Use it as a heartbeat to show the server and config are fine.


2. GET /team

Purpose

Fetch recent matches for a Valorant team

What happens inside

The API calls StatsService
StatsService uses EsportsAdapter
EsportsAdapter calls the Pandascore Valorant endpoint
It normalizes the JSON into a clean list with
team names
match name
event or tournament
status
start time

3. POST /favorites

Purpose

Save a favorite team to your Supabase database

What happens inside

On startup bootstrap() creates a favorites table if it does not exist
When you call this route
it inserts a new row into favorites with
user id (default demo_user)
team name


4. GET /favorites

Purpose

List the most recent favorites from the database

What happens
Reads the last 10 rows from the favorites table
Returns them as JSON


5. GET /report.csv

Purpose
Generate a text report for a team that you can download or open in Excel

What happens

Calls the same esports adapter used by /team
Pulls the last N matches
Writes them into CSV format with columns
begin_at
status
event
name
teams

6. GET /event/map?q=Toronto esports arena

Purpose

Return a simple HTML snippet with a Google Maps embed for a location string

What happens

The maps adapter stub builds an <iframe> URL using the query text
The route returns HTML
If you paste the returned HTML into a simple front end page, you see a map




LIMITATIONS
PandascoreAPI is free of access but the record and key are mostly showing regional tournaments. Full detailed results cant be shown here.
Online Database will shut off when the inactivity period is reached.