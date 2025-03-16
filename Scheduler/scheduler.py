from datetime import datetime
import pytz
import json
from route import Route
from ETA import get_eta
from supabase import create_client, Client

SUPABASE_URL = "https://uhpsdfszsevzcvoyzarn.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVocHNkZnN6c2V2emN2b3l6YXJuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDIwMDg0NjQsImV4cCI6MjA1NzU4NDQ2NH0.3WKlnCQ571BT8_sY6I5gSv_SyE6b2rK0cHCWzT6lt1w"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def schedular():
    gmt_hour = datetime.now(pytz.timezone('GMT')).hour

    with open(f"jobs_JSON/jobs{gmt_hour:02d}.json", "r") as f:
        routes = [Route.from_dict(route) for route in json.load(f)]

    for r in routes:
        eta = get_eta(r.route[0], r.route_id[1]) #origin and destination
        route_id = r.route_id

        now = datetime.now(pytz.timezone('GMT'))
        current_time = now.strftime('%H:%M:%S')
        current_date = now.strftime('%Y-%m-%d')

        data = {
            "route_id": route_id,
            "time": current_time,
            "date": current_date,
            "eta": eta
        }

        #send the entry to the database
        supabase.table("routeentries").insert(data).execute()
