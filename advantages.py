#!/usr/bin/python

""" Free GURPS Character Creation Program
    Copyright (C) 2014  Mateus Rodrigues <mprodrigues@openmailbox.org>

    This file is part of fgccp.

    fgccp is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Fgccp is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with fgccp.  If not, see <http://www.gnu.org/licenses/>."""

import string

AID    = 0
ANAME  = 1
AINIT  = 2
APPL   = 3
AMAXL  = 4
ABON   = 5
AREF   = 6

class Quirk_db:
  def __init__(self, *args):
    self.db = {}

  def add_quirk_file(self, file):
    quirk_file=open(file,'r')
    for q_line in quirk_file.readlines():
      if q_line[0] == '#':
        continue
      quirk = string.split(q_line,';')
      string.strip(quirk[0])
      #print '>', quirk[0], '<'
      self.db[quirk[0]] = 1

       
  def sorted_keys(self):
    keys = self.db.keys()
    keys.sort()
    return keys

class Advantage_db:
  def __init__(self, *args):
    self.db = {}

  def add_advantage_file(self, file):
    advantage_file=open(file,'r')
    for advantage_line in advantage_file.readlines():
      string.strip(advantage_line)
      if advantage_line[0] == '#':
	continue
      advantage = string.split(advantage_line,';')
      for i in range(len(advantage)):
	advantage[i] = string.strip(advantage[i])
        #print '>', advantage[i], '<'
      self.db[advantage[0]] = advantage
      

  def sorted_keys(self):
    '''Returns a sorted list of the keys'''
    # XXX Todo
    # Important, this sorts the keys, not the names, we should fix this
    # eventually
    keys = self.db.keys()
    keys.sort()
    return keys
 
  def calculate_advantage_cost(self,adv,lvl):
    """Calculate the cost of having this advantage"""
    if lvl == 0:
      return 0
    initial_costs = string.split(self.db[adv][AINIT],'/')
    level = 1
    cost = 0
    while level <= lvl:
      if len(initial_costs) >= level:
	cost = cost + int(initial_costs[level-1])
      else:
	cost = cost + int(self.db[adv][APPL])
      level = level + 1
    return cost
    
  def gives_modifiers(self, adv_id):
    if not self.db.has_key(adv_id):
      print "gives modifiers received wrong skill id", adv_id
      return -1
    if self.db[adv_id][ABON] != 0:
      return 1
    return 0
    

