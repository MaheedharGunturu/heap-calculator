#!/usr/bin/env python

import sys

if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    sys.stderr.write('Usage: <histogram-output>\n')
    sys.exit(0)

with open(filename) as f:
    histogram = f.read().strip().split('\n')

# Store the column indexes
offset_index = 0
row_size_index = 0

# Store the totals
total_estimated_row_size = 0
total_rows = 0

for i, line in enumerate(histogram):
    split_line = line.split()
    try:
        # Calculate the median size of this range
        size_range = int(split_line[offset_index])
        if i + 1 < len(histogram):
            next_range = int(histogram[i + 1].split()[offset_index])
            size_range = (size_range + next_range) / 2

        # Grab the number of rows in this range
        sized_rows = int(split_line[row_size_index])

        # Keep track of the totals
        total_rows += sized_rows
        total_estimated_row_size += size_range * sized_rows
    except:
        # Catch the first and all non-data rows
        if not offset_index and split_line[0] == 'Offset':
            # Allow a split for phrases with spaces, i.e. 'Row Size'
            line = filter(None, line.split('  '))

            # Get the column index of Offsets and Row Sizes
            offset_index = line.index('Offset')
            row_size_index = line.index('Row Size')

# Print the average estimated row size
print total_estimated_row_size / total_rows
