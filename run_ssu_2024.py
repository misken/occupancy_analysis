import pandas as pd

import hillmaker as hm

scenario_stub = 'ssu_2024'

# Read ssu_2024 data
stopdata = f'./data/{scenario_stub}.csv'
stops_df = pd.read_csv(stopdata, parse_dates=['InRoomTS', 'OutRoomTS'])

# Create empty dicts to hold the scenario dicts and scenario objects
scenario_dicts = {}

# Define experimental input levels
bin_size_mins_levels = [120, 60, 30, 15]
highres_bin_size_mins_levels = [120, 60, 30, 15, 5, 3, 1]
edge_bins_levels = [1, 2]

# Run hillmaker for each combination of input levels
for bsm in bin_size_mins_levels:
    for eb in edge_bins_levels:
        for hr in [h for h in highres_bin_size_mins_levels if h <= bsm]:
            scenario_name = f'{scenario_stub}_edge{eb}_bin{bsm}_res{hr}'
            print(f'Starting {scenario_name}')
            scenario_dicts[scenario_name] = {'scenario_name': scenario_name,
                                             'stops_df': stops_df,
                                             'in_field': 'InRoomTS',
                                             'out_field': 'OutRoomTS',
                                             'start_analysis_dt': '2024-01-01',
                                             'end_analysis_dt': '2024-09-30',
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
