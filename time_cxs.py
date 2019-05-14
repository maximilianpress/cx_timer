#!/usr/bin/env python
'''
Contraction timer. will see if it works.

Added utilities to preserve records of contraction measurement episodes for cross-comparison.

Added CxRecord object as an organizing principle.
'''

from __future__ import print_function
from datetime import datetime
import pickle
import argparse

class CxRecord:
	'''To hold data for specific episodes of measurement, timestamped.
	'''
	def __init__(self, cx_lengths, cx_begins, pickle_stub=None, logfile="cx_log.txt"):
		self.begins = []
		self.ends = []
		self.lengths = None
		self.diffs = None
		#self._median_length = median_length
		#self._median_interval = median_interval
		self.date_and_time = datetime.now().replace(" ", "_")
		if pickle_stub is None:
			self.pickle_path = "cx_{0}.pkl".format(self.date_and_time)
		else:
			self.pickle_path = "cx_{0}.pkl".format(pickle_stub)
	
	@property
	def median_length(self):
		'''compute/return the median cx length for a given episode'''
		return self._median_length
	
	@median_length.setter
	def median_length(self):
		self._median_length = compute_median(self.lengths)
	
	@property
	def median_interval(self):
		'''compute/return the median interval between cxs for a given episode'''
		return self._median_interval
		
	@median_interval.setter	
	def median_interval(self):
		self.diffs = diff_time_series(self.begins)
		self._median_interval = compute_median(self.diffs)
	
	def pickle_record(self):
		pickle.dump(self, file=self.pickle_path)
		
	def load_record(self, begin, end):
		self.begins.append(begin)
		self.lengths.append(end - begin)
	
	def record_cx_episode():
		cx_lengths = []
		cx_begins = []
		it = 0
		while True:
			cx_begin, cx_end = time_cx()
			if str(cx_end).lower() == "done":
				break
			cx_delta = cx_end - cx_begin
			elif str(cx_end).lower() is None:
				continue
			else:
				cx_lengths.append(cx_delta)
			cx_begins.append(cx_begin)
			it+=1
			print("{0} contractions measured".format(it))
		self.cx_lengths = cx_lengths
		self.cx_begins = cx_begins
		self.cx_ends = cx_ends
	

# to become methods of the CxRecord class (at some point!!!)
def time_cx():
	'''Actually collect the data (user-input) on a specific contraction time.
	'''
	input = raw_input("press enter to indicate beginning of Cx, or 'done' to finish and compute from collected data.\n")
	begin = datetime.now()
	if input == "done":
		return "done", "done"
	input = raw_input("press enter to indicate end of Cx, or 'next' to skip to next Cx beginning.\n")
	end = datetime.now()
	if input == "next":
		return None, None
	return begin, end

	
def run_cx_loop():
	'''Iterate on contractions within an episode until done with episode.
	'''
	cx_lengths = []
	cx_begins = []
	it = 0
	while True:
		cx_begin, cx_end = time_cx()
		if str(cx_end).lower() == "done":
			break
		cx_delta = cx_end - cx_begin
		elif str(cx_end).lower() is None:
			continue
		else:
			cx_lengths.append(cx_delta)
		cx_begins.append(cx_begin)
		it+=1
		print("{0} contractions measured".format(it))
	return cx_lengths, cx_begins
	
def diff_time_series(cx_begins):
	'''Diff the beginning times of an episode's beginning time measurements.
	'''
	last_time = None
	diffs = []
	for cx in cx_begins:
		if last_time is None:
			last_time = cx
		else:
			diff = cx - last_time
			diffs.append(diff.total_seconds())
	return diffs
	
def compute_median(list):
	'''Compute the median of a list of numbers.
	
		Args:
			list ([int] or [float]): numbers to compute a median of
	'''
	list.sort()
	midpoint = len(list) / 2.0
	if len(list) % 2 == 0:
		mid1 = int(midpoint-.5)
		mid2 = int(midpoint+.6)
		median = (list[mid1] + list[mid2]) / 2.
	else:
		median = list[int(midpoint)]
	return median
	
def compute_cx_stats(cx_lengths, cx_begins):
	'''Given expected contraction time measurements, compute stats of interest.
	'''
	cx_sec_lens = [cx.total_seconds() for cx in cx_lengths]
	median_cx = compute_median(cx_sec_lens)
	diffs = diff_time_series(cx_begins)
	median_diffs = compute_median(diffs)
	print("median interval between cx", median_diffs)
	print("median length of cx", median_cx)
	return median_cx, median_diffs, diffs

def write_cx_data_to_log(cx_begins, cx_lengths, logfile = "cx_log.txt"):
	'''Write raw contraction data to human-readable log.
	'''
	with open(logfile, "a") as out:
		for i in range(len(cx_lengths)):
			log_str = "{0}\t{1}\t{2}\n".format(i, 
											   str(cx_begins[i]).replace(" ", "_"),
											   cx_lengths[i])
			out.write(log_str)
	
def make_cx_record():
	'''Run the procedures to get info on a contraction episode.
	'''
	cx_lengths, cx_begins = run_cx_loop()
	median_cx, median_diffs, diffs = compute_cx_stats(cx_lengths, cx_begins)
	write_cx_data_to_log(cx_begins=cx_begins, cx_lengths=cx_lengths)
	

	
	
	
if __name__ == "__main__":
	make_cx_record()