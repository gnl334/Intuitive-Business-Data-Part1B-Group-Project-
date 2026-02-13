from flask import Flask, request
from flask_cors import CORS
from enum import Enum
import database
import pandas as pd

app = Flask(__name__)
CORS(app, resources = {
    r"/*": { # restrict origins of all routes
        "origins": [
            "http://localhost:5173",
            "http://127.0.0.1:5173"
        ]
    }
})

@app.route("/")
def index():
    return "Flask API"


class TIMESPAN(str, Enum):
    HOURLY = 'hourly'
    DAILY = 'daily'
    WEEKLY = 'weekly'
    MONTHLY = 'monthly'

class AGGREGATE_TABLE(str, Enum):
    HOURLY = 'focus_usage_cost_hourly'
    DAILY = 'focus_usage_cost_daily'
    WEEKLY = 'focus_usage_cost_weekly'
    MONTHLY = 'focus_usage_cost_monthly'

class USAGE_FIELD(str, Enum):
    HOURLY = 'usage_hour'
    DAILY = 'usage_date'
    WEEKLY = 'usage_week'
    MONTHLY = 'usage_month'

AGGREGATE_TABLE_LOOKUP = {
    TIMESPAN.HOURLY.value: [AGGREGATE_TABLE.HOURLY.value,USAGE_FIELD.HOURLY.value],
    TIMESPAN.DAILY.value: [AGGREGATE_TABLE.DAILY.value,USAGE_FIELD.DAILY.value],
    TIMESPAN.WEEKLY.value: [AGGREGATE_TABLE.WEEKLY.value,USAGE_FIELD.WEEKLY.value],
    TIMESPAN.MONTHLY.value: [AGGREGATE_TABLE.MONTHLY.value,USAGE_FIELD.MONTHLY.value]
}

#############################################
#                Data Routes                #
#############################################

@app.route("/api/overview")
def overview():
    return "TODO"

@app.route("/api/overview/<provider>")
def overview_provider(provider):
    return "TODO"

@app.route("/api/providers")
def get_providers():
    return list(map(lambda x: x[0], database.query("SELECT DISTINCT provider_name FROM cost_entity;")))

@app.route("/api/usage/<provider>/<timestep>")
def usage(provider, timestep):
    # check parameters
    if timestep not in TIMESPAN:
        return f'Bad Request: ${timestep} not in acceptible timesteps: ${AGGREGATE_TABLE_LOOKUP.keys()}', 400

    if provider not in get_providers():
        return f'Bad Request: ${provider} not in acceptible providers: ${get_providers()}', 400
    
    selected_table, selected_usage_field = AGGREGATE_TABLE_LOOKUP[timestep]

    query = f"""
    SELECT    
        {selected_usage_field},
        SUM(total_usage_cost) AS usage_cost
    FROM {selected_table}
    WHERE provider_name = "{provider}"
    GROUP BY {selected_usage_field}
    ORDER BY {selected_usage_field};
    """
    
    return database.query(query)

@app.route("/api/top_services/<provider>/<timestep>")
def top_services(provider,timestep):
    # check parameters
    if timestep not in TIMESPAN:
        return f'Bad Request: ${timestep} not in acceptible timesteps: ${AGGREGATE_TABLE_LOOKUP.keys()}', 400

    if provider not in get_providers():
        return f'Bad Request: ${provider} not in acceptible providers: ${get_providers()}', 400

    selected_table, selected_usage_field = AGGREGATE_TABLE_LOOKUP[timestep]

    # How many services to give information for and how many to
    N_top_services = int(request.args.get("N", 5))

    query = f"""
    SELECT    
        {selected_usage_field}, service_name,
        SUM(total_usage_cost) AS usage_cost
    FROM {selected_table}
    WHERE provider_name = "{provider}"
    GROUP BY {selected_usage_field}, service_name
    ORDER BY {selected_usage_field};
    """
    # read the query directly into a pandas dataframe
    df = pd.read_sql_query(query, database.get_db())

    # find the
    top_services = df.groupby("service_name")["usage_cost"].sum().nlargest(N_top_services).index
    df["service_group"] = df["service_name"].where(df["service_name"].isin(top_services), "Other")
    plot_df = df.groupby(["usage_hour", "service_group"])["usage_cost"].sum().reset_index()
    pivot_df = plot_df.pivot(index="usage_hour", columns="service_group", values="usage_cost").fillna(0)
    return pivot_df.to_json()


############################################
#                VPL Routes                #
############################################

@app.route("/api/getVPL=<vplID>")
def home_page(vplID):
    return vplID # get vpl file

@app.teardown_appcontext
def on_close(exception):
    database.close_connection(exception)

# make sure no caching while testing
@app.after_request
def add_headers(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response