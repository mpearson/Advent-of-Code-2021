import sys
import numpy as np

data_path = "data/problem_8.txt"
# data_path = "data/problem_8_test.txt"


with open(data_path, "r") as f:
    file_lines = f.read().splitlines()

row_count = len(file_lines)

output_patterns = np.zeros((row_count, 10, 7), dtype=bool)
query_patterns = np.zeros((row_count, 4, 7), dtype=bool)

a_offset = ord("a")
for row_index, line in enumerate(file_lines):
    left_words, right_words = line.split(" | ")
    for pattern_index, word in enumerate(left_words.split(" ")):
        segment_indices = np.frombuffer(word.encode(), dtype=np.uint8) - a_offset
        output_patterns[row_index, pattern_index, segment_indices] = True

    for pattern_index, word in enumerate(right_words.split(" ")):
        segment_indices = np.frombuffer(word.encode(), dtype=np.uint8) - a_offset
        query_patterns[row_index, pattern_index, segment_indices] = True

# part 1
segment_definitions = np.array([
#    a  b  c  d  e  f  g
    [1, 1, 1, 0, 1, 1, 1],  # 0 = abc efg
    [0, 0, 1, 0, 0, 1, 0],  # 1 =   c  f
    [1, 0, 1, 1, 1, 0, 1],  # 2 = a cde g
    [1, 0, 1, 1, 0, 1, 1],  # 3 = a cd fg
    [0, 1, 1, 1, 0, 1, 0],  # 4 =  bcd f
    [1, 1, 0, 1, 0, 1, 1],  # 5 = ab d fg
    [1, 1, 0, 1, 1, 1, 1],  # 6 = ab defg
    [1, 0, 1, 0, 0, 1, 0],  # 7 = a c  f
    [1, 1, 1, 1, 1, 1, 1],  # 8 = abcdefg
    [1, 1, 1, 1, 0, 1, 1],  # 9 = abcd fg
], dtype=int)

# determine which numbers have a unique number of segments
segment_counts = segment_definitions.sum(axis=1)
print(f"segment_counts: {segment_counts}")

_, unique_count_indices, unique_count_counts = np.unique(segment_counts, return_index=True, return_counts=True)
numbers_with_unique_segment_counts = unique_count_indices[unique_count_counts == 1]
print(f"values {numbers_with_unique_segment_counts} have unique segment counts {segment_counts[numbers_with_unique_segment_counts]}")

query_segment_counts = query_patterns.sum(axis=2)
easy_digit_count = 0
for segment_count in segment_counts[numbers_with_unique_segment_counts]:
    easy_digit_count += np.sum(query_segment_counts == segment_count)

print(f"Part 1 solution: {easy_digit_count}")


# part 2

# candidate matrix for each row.
# Axis 0 is row index, axis 1 is the nominal segment, axis 2 is all displayed segments that haven't been eliminated.
# initially, all segments are possible candidates.
translation_map = np.ones((row_count, 7, 7), dtype=int)

# for each number with a unique segment count, eliminate all candidates with the wrong count
for number in numbers_with_unique_segment_counts:
    patterns_with_matching_counts = output_patterns.sum(axis=2) == segment_counts[number]
    candidate_segments = output_patterns[patterns_with_matching_counts]
    translation_map[:, segment_definitions[number].astype(bool)] &= candidate_segments[:, None, :]
    # note the [:, None, :] is broadcast (N, 7) to (N, M, 7) where N is the number lines
    # and M is the number of segments in the number

# let's see how many numbers each segment appears in
segment_frequencies = segment_definitions.sum(axis=0)
print(f"segment_frequencies: {segment_frequencies}")

_, unique_seg_freq_indices, unique_seg_freq_counts = np.unique(segment_frequencies, return_index=True, return_counts=True)
segments_with_unique_seg_freq = unique_seg_freq_indices[unique_seg_freq_counts == 1]
print(f"segments {segments_with_unique_seg_freq} have unique segment frequencies {segment_frequencies[segments_with_unique_seg_freq]}")


# for each segment with a unique frequency, eliminate all candidates with the wrong frequency
for segment_index in segments_with_unique_seg_freq:
    output_segment = np.argmax(output_patterns.sum(axis=1) == segment_frequencies[segment_index], axis=1)
    # print(f"mapping: {segment_index} -> {output_segment}")
    translation_map[:, segment_index] = False
    translation_map[range(row_count), :, output_segment] = False # eliminate this segment as a candidate everywhere else
    translation_map[range(row_count), segment_index, output_segment] = True # eliminate this segment as a candidate everywhere else


# do this whole shit twice, which is an amount of times that seems to do the ol' trick
for i in range(2):
    # for each fully constrained segment, remove it as a candidate everywhere else
    locked_segments = np.nonzero(translation_map[0].sum(axis=1) == 1)[0]
    print(f"locked_segments: {locked_segments}")
    locked_segment_values = np.argmax(translation_map[:, locked_segments], axis=2)
    for index, segment in enumerate(locked_segments):
        translation_map[range(row_count), :, locked_segment_values[:, index]] = 0
        translation_map[range(row_count), segment, locked_segment_values[:, index]] = 1

    fully_constrained = np.all(translation_map.sum(axis=2) == 1)
    if fully_constrained:
        print(f"All segments fully constrained")
        break

assert fully_constrained, "dangit"

# print(f"translation_map[0]:\n{translation_map[0]}")

# convert translation matrix to integer indices
decoder_map = np.argmax(translation_map, axis=1)
# print(decoder_map)


# convert bool segment patterns to numeric indices
row_indices, number_indices, segment_indices = np.nonzero(query_patterns)

translated_segments = np.zeros_like(query_patterns)
# use magical fancy indexing to look up translations for every segment in every query row
translated_segments[row_indices, number_indices, decoder_map[row_indices, segment_indices]] = True

# indexing like this ain't natural, I tell you what
digit_translation = np.argmax(np.all(translated_segments[:, :, :] == segment_definitions[:, None, None, :], axis=3), axis=0)
# print(digit_translation)

exponents = 10 ** np.arange(digit_translation.shape[1])[::-1]
row_values = np.sum(digit_translation * exponents, axis=1)
# print(row_values)

print(f"Part 2 solution: {row_values.sum()}")
