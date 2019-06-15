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

class CxRecord(object):
	'''To hold data for specific episodes of measurement, timestamped.
	'''
	def __init__(self, pickle_stub=None, logfile="cx_log.txt"):
		self.begins = []
		self.ends = []
		self.lengths = []
		self.diffs = None
		self.median_length = None
		self.median_interval = None
		self.date_and_time = str(datetime.now()).replace(" ", "_")
		if pickle_stub is None:
			self.pickle_path = "cx_{0}.pkl".format(self.date_and_time)
		else:
			self.pickle_path = "cx_{0}.pkl".format(pickle_stub)
	
	def pickle_record(self):
		pkl_file = open(self.pickle_path, "w")
		pickle.dump(self, file=pkl_file)
		
	def compute_stats(self):
		self.median_length = compute_median(self.lengths)
		self.diffs = diff_time_series(self.begins)
		self.median_interval = compute_median(self.diffs)
	
	def record_cx_episode(self):
		cx_lengths = []
		cx_begins = []
		cx_ends = []
		it = 0
		while True:
			cx_begin, cx_end = time_cx()
			if str(cx_end).lower() == "done":
				break
			elif cx_end is None:
				continue
			else:
				cx_delta = cx_end - cx_begin
				cx_lengths.append(cx_delta)
			
			cx_begins.append(cx_begin)
			cx_ends.append(cx_end)
			it+=1
			print("{0} contractions measured".format(it))
		
		self.lengths = [cx_length.total_seconds() for cx_length in cx_lengths]
		self.begins = cx_begins
		self.ends = cx_ends
		self.compute_stats()
	
	def report_stats(self):
		stat_report = "{0} Cx beginning at {1}\n".format(len(self.begins), self.begins[0])
		stat_report += "Median cx length {}\n".format(self.median_length)
		stat_report += "Median cx interval {}\n".format(self.median_interval)
		print(stat_report)
	

# to become methods of the CxRecord class (at some point!!!)
def time_cx():
	'''Actually collect the data (user-input) on a specific contraction time.
	'''
	input = raw_input("press enter to indicate beginning of Cx, or type 'done' (+enter) to finish and compute from collected data.\n")
	begin = datetime.now()
	if input == "done":
		return "done", "done"
	input = raw_input("press enter to indicate end of Cx, or type 'next' (+enter) to skip to next Cx beginning.\n")
	end = datetime.now()
	if input == "next":
		return None, None
	return begin, end
	
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
	if len(list) == 1:
		return list[0]
	elif len(list) == 0:
		return None
	list.sort()
	midpoint = len(list) / 2.0
	if len(list) % 2 == 0:
		mid1 = int(midpoint-.5)
		mid2 = int(midpoint+.6)
		median = (list[mid1] + list[mid2]) / 2.
	else:
		median = list[int(midpoint)]
	return median
	
def write_cx_data_to_log(cx_begins, cx_lengths, logfile = "cx_log.txt"):
	'''Write raw contraction data to human-readable log.
	'''
	with open(logfile, "a") as out:
		for i in range(len(cx_lengths)):
			log_str = "{0}\t{1}\t{2}\n".format(i, 
											   str(cx_begins[i]).replace(" ", "_"),
											   cx_lengths[i])
			out.write(log_str)
	
def parse_args():
	parser = argparse.ArgumentParser(description='contraction timer.')
	parser.add_argument('--out_archive', '-o', type=str, required=False, default=None,
						help='prefix to use in pickle of record. Default is timestamp.')
	parser.add_argument('--out_log', '-l', type=str, required=False, default="cx_log.txt",
						help='human-readable log file to append to. Default is' 			
						'cx_log.txt.')
	args = parser.parse_args()
	return vars(args)
    
    
def main():
	args = parse_args()
	CXR = CxRecord(pickle_stub=args["out_archive"], logfile=args["out_log"])
	CXR.record_cx_episode()
	CXR.report_stats()
	write_cx_data_to_log(cx_begins=CXR.begins, cx_lengths=CXR.lengths, logfile=args["out_log"])
	CXR.pickle_record()
	
if __name__ == "__main__":
	#make_cx_record()
	main()