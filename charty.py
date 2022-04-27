#!/usr/bin/env python3
# Author: Michael T. Duffy II

from optparse import OptionParser
import os.path
import yaml
import re
import textwrap
from random import randint

#===============================================================================
class ChartCollection:

  #-----------------------------------------------------------------------------
  def __init__ (self):
    self.charts = {}

  #-----------------------------------------------------------------------------
  def register_chart (self, chart):
    """ Add a chart to the collection.  The passed 'chart' object should
        have a string 'name' field and a list 'entries' field.
    """
    name = chart['name']
    entries = chart['entries']

    if (not name or not entries):
      return
    rex_weight_and_text = re.compile(r"\s*(\((\d+)\))?\s*(.+)$")

    new_chart = []
    for entry in entries:
      match_result = rex_weight_and_text.match (entry)
      if match_result:

        num_matches = len(match_result.groups())

        if match_result.group(1) == None:
          # Evenly weighted
          new_chart.append ((1, match_result.group(3)))
        else:
          # Specifically weighted
          new_chart.append ((int(match_result.group(2)), match_result.group(3)))

    self.charts[name] = new_chart

  #-----------------------------------------------------------------------------
  def expand_charts (self, string_in):
    """ Expand any chart definition within the string with a roll on that chart """
    string_out = string_in
    rex_chart_tag = re.compile (r"\<\s*chart\s*\|\s*([^\>]+)\s*>")

    # While there are still charts to expand, expand them.
    while 1:
      result = rex_chart_tag.search (string_out)

      if not result:
        break;

      chart_name = result.group(1)
      if not chart_name:
        break;

      lookup_result = self.__roll_chart (chart_name)
      string_out = rex_chart_tag.sub (lookup_result, string_out, 1)

    return string_out

  #-----------------------------------------------------------------------------
  def __roll_chart (self, chart_name):
    """ Look up the named chart and return a roll of its contents """
    if not chart_name in self.charts:
      return ""
    # calculate the weighted sum, then roll the dice
    max = 0
    for entry in self.charts[chart_name]:
      max += entry[0]

    if max == 0:
      return ""

    sum = 0
    roll = randint(0,max-1)
    for entry in self.charts[chart_name]:
      sum += entry[0]
      if sum > roll:
        return entry[1]
    # we ran past the end of the chart.  We shouldn't get here unless the chart is empty.
    return ""

#===============================================================================
class Charty:
  """
  Charty takes chart (table) definitions stored in YAML format as input, composes the
   charts according to their defined rules, and writes the results to stdout.

  Charts file YAML has the following schema.  Note that "charts" is a list and may
    have multiple charts defined under it.

    include:
      - other_chart_filename_to_include

    charts:
      - name: chart_name_one
        entries:
        - entry text A with default weight of 1
        - (2) entry text B with optional defined weight of 2
        - entry text N
      - name: chart_name_two
        entries:
        - entry text A with default weight of 1

    output: |
      Text output line 1
      Text output line 2
      <chart|chart_name_one> Result from the chart named "chart_name_one"
  """

  #-----------------------------------------------------------------------------
  def __init__ (self):
    self.chart_collection = ChartCollection ()

    self.wrap_width = 80
    self.indent = ""
    self.input_files = []
    self.included_files = []
    self.output = ""
    self.output_override = None
    self.filename = None

  #-----------------------------------------------------------------------------
  def read_command_params (self):
    """ Read command line parameters and initialize the default state """
    parser = OptionParser()
    parser.add_option ("-f", "--file", dest="filename",
                       help="write results to FILE instead of stdout", metavar="FILE")
    parser.add_option ("-c", "--chart", dest="chart",
                       help="roll results on specific CHART instead of using the output section", metavar="CHART")
    parser.add_option ("-i", "--indent", dest="indent", type="int", default=0,
                       help="indent the first line by INDENT spaces", metavar="INDENT")
    parser.add_option ("-w", "--width", dest="width", type="int", default=80,
                       help="wrap the results at WIDTH characters", metavar="WIDTH")

    (options, args) = parser.parse_args()

    if options.chart:
      self.output_override = "<chart|{name}>".format (name=options.chart)

    self.filename    = options.filename
    self.indent      = " "*options.indent
    self.wrap_width  = options.width
    self.input_files = args

  #-----------------------------------------------------------------------------
  def load_chart_file (self, file_in, ignore_output = False):
    """ Load the charts, included files, and output spec from a YAML file """
    if (os.path.exists(file_in) and os.path.isfile(file_in)):
      with open(file_in, 'r') as yamlfile:
        cfg = yaml.load(yamlfile, Loader=yaml.SafeLoader)
        for section in cfg:
          if section == "charts":
            if isinstance (cfg[section], list):
               for curr in cfg[section]:
                 self.chart_collection.register_chart (curr)
          if section == "include":
            if isinstance (cfg[section], list):
               for curr in cfg[section]:
                 self.included_files.append (curr)
          if section == "output":
            if not ignore_output:
              self.output += cfg[section]

  #-----------------------------------------------------------------------------
  def read_input_files (self):
    """ load all YAML format input files """
    for curr_file in self.input_files:
      self.load_chart_file (curr_file)
    for curr_file in self.included_files:
      self.load_chart_file (curr_file, ignore_output=True)

  #-----------------------------------------------------------------------------
  def expand_charts (self, string_in):
    """ Expand any chart definition within the string with a roll on that chart """
    result = self.chart_collection.expand_charts (string_in)
    wrapped_result = textwrap.fill (result, width = self.wrap_width, initial_indent = self.indent)
    return (wrapped_result)

  #-----------------------------------------------------------------------------
  def write_results (self, results):
    """ Write the given results to stdout or the output file if specified """
    if app.filename:
      with open (app.filename, "w") as file_out:
        file_out.write (results)
        file_out.write ("\n")
    else:
      print (results)

#===============================================================================
if __name__ == '__main__':
  app = Charty()
  app.read_command_params ()
  app.read_input_files ()
  app.write_results (app.expand_charts (app.output_override if app.output_override else app.output))
