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
 
SID    = 0
SNAME  = 1
SDIFF  = 2
SATTR  = 3
SDEF   = 4
SMOD   = 5
SBON   = 6
SPRE   = 7
SFLAGS = 8
SREF   = 9

 
def find_flag(flag,flags):
  """Finds a flag in a comma separated list"""
  for i in string.split(flags,','):
    if i == flag:
      return True
  return False


class Skill_db:
  def __init__(self, *args):
    self.db = {}  

  def takes_type(self,skill_id):
    return find_flag('type',self.db[skill_id][SFLAGS])

  def list_skills(self):
    """Lists the skills in the database"""
    for sid in self.all.keys():
      sname = skills[sid][SNAME]
      if find_flag('TL',skills[sid][SFLAGS]):
	sname = sname + '/TL'
      print string.ljust(sname,30),
      print '%5s' % skills[sid][SDIFF]
   
  def sorted_keys(self):
    '''Returns a sorted list of the keys'''
    # XXX Todo
    # Important, this sorts the keys, not the names, we should fix this
    # eventually
    keys = self.db.keys()
    keys.sort()
    return keys
 
  def gives_modifiers(self, skill_id):
    if not self.db.has_key(skill_id):
      print "gives modifiers received wrong skill id", skill_id
      return -1
    if self.db[skill_id][SBON] != "":
      return 1
    return 0
    
  def add_skill_file(self, file):
    try:
      skill_file=open(file,'r')
    except:
      print 'Error opening skill file ', file
      return -1
    for skill_line in skill_file.readlines():
      string.strip(skill_line)
      if skill_line[0] == '#': 
        continue
      skill = string.split(skill_line,';')
      for i in range(len(skill)):
        skill[i] = string.strip(skill[i])
      self.db[skill[0]] = skill

  def sdiff_adjustment(self,diff,points):
    """Calculates the adjustment based on the points assgined"""
    type, hardness = string.split(diff,'/')
    if points == 0:
      return -20
    if type == 'P':
      #print "Physical skill"
      if points >= 0.5 and points < 1:
	adj = -1
      elif points >= 1 and points < 2:
	adj = 0
      elif points >= 2 and points < 4:
	adj = 1
      elif points >= 4 and points < 8:
	adj = 2
      else:
	adj = points/8 + 2
      if hardness == 'H':
	adj = adj - 2
      elif hardness == 'A':
	adj = adj - 1
      elif hardness != 'E':
	print 'Unknown hardness'
    elif type == 'M':
      if hardness == 'VH':
	if points >= 0.5 and points < 1:
	  adj = -4
	elif points >= 1 and points < 2:
	  adj = -3
	elif points >= 2 and points < 4:
	  adj = -2
	elif points >= 4 and points < 8:
	  adj = -1
	else:
	  adj = points/4 - 2
      else:
	if points >= 0.5 and points < 1:
	  adj = -1
	elif points >= 1 and points < 2:
	  adj = 0
	elif points >= 2 and points < 4:
	  adj = 1
	elif points >= 4 and points < 6:
	  adj = 2
	else:
	  adj = points/2 
	if hardness == 'H':
	  adj = adj - 2
	elif hardness == 'A':
	  adj = adj - 1
	elif hardness != 'E':
	  print 'Unknown hardness'
    else:
      print "Unkown type"
    return adj


  def calculate_default(self,character,skill):
    """Returns the skill level of a default skill"""
    sdefaults = string.split(self.db[skill][SDEF],',')
    high_default = 0
    if sdefaults[0] == "":
      return 0
    for sdefault in sdefaults:
      sbase, sadj = string.split(sdefault,'/')
      if sbase == 'ST':
	sdef = character.get_attr('ST')
      elif sbase == 'DX':
	sdef = character.get_attr('DX')
      elif sbase == 'IQ':
	sdef = character.get_attr('IQ')
      elif sbase == 'HT':
	sdef = character.get_attr('HT')
      else:
	#print "Based on skill ", sdefault
	sdef = character.get_skill(sbase) 
      #print "Based on attr ", sbase, " ", sdef, " ", sadj,
      sdef = sdef + int(sadj)
      #print " >> ", sdef
      if sdef > high_default:
	high_default = sdef
    return high_default

  def calculate_by_points(self,character,skill,points):
    """Calculates the skill level of a skill based on points"""
    sbase = character.get_attr(self.db[skill][SATTR])
    sadj  = self.sdiff_adjustment(self.db[skill][SDIFF],points)
    return sbase + sadj
    
  def calculate_skill(self,character,skill,points):
    """Calculates the skill level of a skill for a certain character"""
    sdefault = self.calculate_default(character,skill) 
    slevel = self.calculate_by_points(character,skill,points)
    if sdefault > slevel:
      return sdefault
    else:
      return slevel



