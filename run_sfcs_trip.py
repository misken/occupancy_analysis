import pandas as pd

import hillmaker as hm

scenario_stub = 'sfcs_trip'

# Read cycleshare data
stopdata = './data/sfcs_trip.csv'
stops_df = pd.read_csv(stopdata, parse_dates=['start_date', 'end_date'])
# Make datetime columns timezone naive
stops_df['start_date'] = stops_df['start_date'].dt.tz_localize(None)
stops_df['end_date'] = stops_df['end_date'].dt.tz_localize(None)

# Create empty dicts to hold the scenario dicts and scenario objects
scenario_dicts = {}

# Define experimental input levels
bin_size_mins_levels = [60, 30, 15]
highres_bin_size_mins_levels = [30, 15, 5, 3, 1]
edge_bins_levels = [1, 2]

# Run hillmaker for each combination of input levels
for bsm in bin_size_mins_levels:
    for eb in edge_bins_levels:
        for hr in [h for h in highres_bin_size_mins_levels if h <= bsm]:
            scenario_name = f'{scenario_stub}_edge{eb}_bin{bsm}_res{hr}'
            print(f'Starting {scenario_name}')
            scenario_dicts[scenario_name] = {'scenario_name': scenario_name,
                                             'stops_df': stops_df,
                                             'in_field': 'start_date',
                                             'out_field': 'end_date',
                                             'start_analysis_dt': '2014-05-01',
                                             'end_analysis_dt': '2014-09-30',
                                             'output_path': f'output/{scenario_stub}',
                                             'bin_size_minutes': bsm,
                                             'highres_bin_size_minutes': hr,
                                             'edge_bins': eb,
                                             'keep_highres_bydatetime': True,
                                             'export_bydatetime_csv': True,
                                             'export_summaries_csv': True,
                                             'make_all_dow_plots': False,
                                             'make_all_week_plots': True,
                                             'export_all_dow_plots': False,
                                             'export_all_week_plots': True,
                                             'verbosity': 1,
                                             }

            scenario = hm.Scenario(**scenario_dicts[scenario_name])
            scenario.make_hills()
            print(f'Scenario {scenario_name} complete\n')

            with open(f'output/{scenario_stub}/{scenario_name}_runtime.txt', 'w') as fout:
                fout.write(f'{scenario.hills["runtime"]:.2f}')
