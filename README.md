# Dynatrace Problems as Metrics extension

## Requirements

### Basic:

1. Python 3.6+. Please see [Download Python](https://www.python.org/downloads/)
2. Python `requests` module. Install after completing step 1 by running `pip3 install requests`

### Configuration:

For `problems.config`

1. Tenancy URL
    - SaaS : `{your-environment-id}.live.dynatrace.com`
    - Managed : `{your-domain}/e/{your-environment-id}`    
    - If running from ActiveGate: `{your-activegate-address}:9999/{your-environment-id}`

2. API Token with below permissions:
   - Read Configuration (v1)
   - Write Configuration (v1)
   - Read Problems (v2)
   - Ingest Metrics (v2)

<br/>

## Usage

Step 1: Clone this github repo to a suitable location on your computer/server 

    `git clone https://github.com/arunkrishnan-dt/dynatrace-problems-as-metrics.git`

Step 2: Update `problems.config` with `tenancy_url` and `api_token` string

```
[TENANCY_INFO]
tenancy_url = xxxxx.live.dynatrace.com
api_token = dt0c01.xxxxxxx.xxxxxx
```
Step 3: Setup Cron/Windows Task Scheduler to run the script every minute

In Linux:

    a. Open Crontab: `crontab -e`

    b. Enter line: `* * * * * python3 {dir_path}/dynatrace-problems-as-metrics/main.py` 

    c. Save and exit

Step 4: Confirm script sending data to Dynatrace tenancy

    a. Metrics show in Dynatrace. Search for `dtapi.problem` in Dynatrace 'Metrics' view

    b. 'Operations centre' is available as a 'preset' dashboard in Dashboards

<br/>

## Troubleshooting

Logs are available at `log/problems.log`

Logging is set to 'INFO' level by default. Update to 'DEBUG' in `problems.config` (as shown below) to get more details.

```
[LOGGING]
log_mode = DEBUG
```

Please raise an issue in github repo if required. 

<br/>

## Configuration File

Configuration file has below parameters

```
[TENANCY_INFO]
tenancy_url =           # Your tenancy url. Please see under 'Requirements' section above
api_token =             # Your API TOKEN. Please see under 'Requirements' section above

[METRICS]
problems_open = true    # Set'true' to send total problems open Global & Management Zone
problems_ttr = true     # Set 'true' to send problem Time to Repair (TTR) values -  Global & Management Zone
problems_new = true     # Set 'true' to send new problem metric -  Global & Management Zone
problems_age = true     # Set 'true' to age of open problems -  Global & Management Zone

[LOGGING]
log_mode = INFO         # Set 'DEBUG' for more detailed logging

[INITIALIZE]
metric_metadata = true  # Intitalizes metric metadata. Value changes to 'false' after first run 
dashboard = true        # POST example dashboard 'Operations Centre'. Value changes to 'false' after first run
```

<br/>

## License Calculation

Sum of all below:

### Problems_Open
- Global = 4 x 60 min x 24 h x 365 days x 0.001 metric weight = 2106.4 DDUs/year
- Management Zones = {Number of management zones} * 4 x 60 min x 24 h x 365 days x 0.001 metric weight DDUs/year

### Problems_MTTR
- Global = {Avg. number of daily problems - Global} x 365 days x 0.001 metric weight DDUs/year
- Management Zones = {Avg. number of daily problems - Management Zone} x 365 days x 0.001 metric weight DDUs/year

### Problems_New
- Global = {Avg. number of daily problems - Global} x 365 days x 0.001 metric weight DDUs/year
- Management Zones = {Avg. number of daily problems - Management Zone} x 365 days x 0.001 metric weight DDUs/year

### Problems_Age
- Global = 4 x 60 min x 24 h x 365 days x 0.001 metric weight = 2106.4 DDUs/year
- Management Zones = {Number of management zones} * 4 x 60 min x 24 h x 365 days x 0.001 metric weight DDUs/year

