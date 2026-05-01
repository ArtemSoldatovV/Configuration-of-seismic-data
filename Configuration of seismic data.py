import numpy as np
import matplotlib.pyplot as plt

#1) часть кода segpy устарел, эта часть кода нужна для решения этой проблемы
# , если вышло обновление которое решает эту проблему код можно удалить
import sys
if sys.version_info >= (3, 10):
    import collections.abc as collections_abc
    sys.modules['collections'].Mapping = collections_abc.Mapping
    sys.modules['collections'].Iterable = collections_abc.Iterable
    sys.modules['collections'].Sequence = collections_abc.Sequence

#1) конец
from segpy.reader import create_reader

class Configuration_of_seismic_data:
    def processing(Path):
        with open(Path, 'rb') as file:
            segy_parser = create_reader(file)
            data = np.zeros(
                (segy_parser.num_inlines(), segy_parser.num_trace_samples(1),
                segy_parser.num_xlines())
                )
            
            for inline, xline in segy_parser.inline_xline_numbers():
                trace_id = segy_parser.trace_index((inline, xline))
                inline_start = segy_parser.inline_numbers()[0]
                xline_start = segy_parser.xline_numbers()[0]
                data[inline - inline_start, :, xline - xline_start] = segy_parser.trace_samples(trace_id)
        
        #Нормализует сейсмические данные
        data = (data - np.min(data)) / (np.max(data) - np.min(data))
        return data
    
    def Image_output_seismic_section(depth_array, figsize_1, figsize_2, data):
        number_of_columns = 3
        number_of_rows = len(depth_array)


        fig, axes = plt.subplots(nrows=number_of_rows, ncols=number_of_columns, figsize=(figsize_1, figsize_2),
                                tight_layout=True, sharex=True, sharey=True)
        
        if number_of_rows == 1:
            for i, _ in enumerate(axes.flat):
                inline = depth_array[i // number_of_columns ]
                axes[0].imshow(data[:, :, inline], cmap='seismic', origin='lower')
                axes[1].imshow(data[:, inline, :], cmap='seismic', origin='lower')
                axes[2].imshow(data[inline, :, :], cmap='seismic', origin='lower')

                #Заголовки
                axes[0].set_title(f"XY slice for {inline}m")
                axes[1].set_title(f"XZ slice for {inline}m")
                axes[2].set_title(f"YZ slice for {inline}m")
        else:
            for i, _ in enumerate(axes.flat):
                row = i//number_of_columns
                inline = depth_array[i // number_of_columns ]
                axes[row, 0].imshow(data[:, :, inline], cmap='seismic', origin='lower')
                axes[row, 1].imshow(data[:, inline, :], cmap='seismic', origin='lower')
                axes[row, 2].imshow(data[inline, :, :], cmap='seismic', origin='lower')

                #Заголовки
                axes[row, 0].set_title(f"XY slice for {inline}m")
                axes[row, 1].set_title(f"XZ slice for {inline}m")
                axes[row, 2].set_title(f"YZ slice for {inline}m")

        plt.show()