import probe_power_spectrum_pipeline.probe_location as probe_location
from pathlib import Path
import os


calculate_power = True
re_calculate_power = False
build_whole_probe = True

mode = 'four_shanks'


mouselist = ['AP5R', 'AP5L', 'AP5lr','SEQ006','SEQ007','SEQ008']

base_ephys_path = r'/ceph/sjones/projects/sequence_squad/revision_data/lars_recordings/ephys/'


OUTPUT = Path(r'/ceph/sjones/projects/sequence_squad/revision_data/organised_data/probe_power_spectra//') 

if calculate_power:
    
    for mouse in mouselist:
        
        recording_paths  = []
        for sub_folder in os.listdir(base_ephys_path):
            os.listdir(os.path.join(base_ephys_path,sub_folder))
            for file_ in os.listdir(os.path.join(base_ephys_path,sub_folder)):
                if mouse in file_:
                    print(file_)
                    recording_paths += [os.path.join(base_ephys_path,sub_folder + r'/' + file_)]
                    
        for raw_data_directory in recording_paths:

            # List the directories directly under raw_data_directory
            for directory in next(os.walk(raw_data_directory))[1]:  # [1] gives the list of directories at the top level

                dir_path = os.path.join(raw_data_directory, directory)

                result = probe_location.get_record_node_path_list(dir_path)
                print(f'RESULT: {result}')

                if len(result)>0:

                    for segment, i in enumerate(result):

                        print(f'SEGMENT:{segment}')
                        
                        if segment == 0:
                            output_probemap = Path(OUTPUT) /  f'{directory}_{mode}' / 'probemap.csv'
                        else:
                            output_probemap = Path(OUTPUT) / f'{directory}_{mode}_segment{segment}' / 'probemap.csv'


                        if output_probemap.is_file() and not re_calculate_power:
                            print(f'{directory} is already processed. SKIPPING!')
                            continue

                        print('\n \n #################################')
                        print(f'Processing {mouse} session {directory}')
                        print('#################################\n \n ')

                        probe_mapper = probe_location.probe_mapper(mouse, directory,dir_path,OUTPUT, mode=mode, segment = segment)

                        #Diagnostics plots

                        probe_mapper.fourier()
                        probe_mapper.plot_10s_traces()

                        #Calculate delta power

                        probe_mapper.probe_spectrum()
                        probe_mapper.calculate_delta_power()

                        #Output plots

                        probe_mapper.build_probemap()


if build_whole_probe:
    
    for mouse in mouselist:
    
        probe = probe_location.whole_probe(mouse)

        probe.build_whole_probemap()

        probe.process_probemap()

        probe.plot_probemap()