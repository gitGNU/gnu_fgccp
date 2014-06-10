""" Free GURPS Character Creation Program
    Copyright © 2014  Mateus Rodrigues <mprodrigues@openmailbox.org>

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

#!/usr/bin/python
'''This is the python classes for character definition
'''

import string
from advantages import *
from skills import *

class Attribute:
  def __init__(self, val):
    self.MAX=25
    self.MIN=1
    self.value=10
    self.points=0
    self.point_table = [ -100,   #  0  <- Not Valid 
                          -80,   #  1
                          -70,   #  2
                          -60,   #  3
                          -50,   #  4
                          -40,   #  5
                          -30,   #  6
                          -20,   #  7
                          -15,   #  8
                          -10,   #  9
                            0,   # 10
                           10,   # 11
                           20,   # 12
                           30,   # 13
                           45,   # 14
                           60,   # 15
                           80,   # 16
                          100,   # 17
                          125,   # 18
                          150,   # 19
                          175,   # 20
                          200,   # 21
                          225,   # 22
                          250,   # 23
                          275,   # 24
                          300]   # 25
    self.set_value(val)
  def set_value(self, value):
    if((value < self.MIN) | (value > self.MAX)):
      return -1
    self.value  = value
    self.points = self.point_table[self.value]
    
class Character_data:
  def __init__(self):
    self.name = ''
    self.player = ''

    self.skills={}
    self.advantages={}
    self.modifiers={}

    self.quirks={}

    self.thrust = [       '0',   #  0  <- Not Valid 
                          '0',   #  1
                          '0',   #  2
                          '0',   #  3
                          '0',   #  4
                       '1d-5',   #  5
                       '1d-4',   #  6
                       '1d-3',   #  7
                       '1d-3',   #  8
                       '1d-2',   #  9
                       '1d-2',   # 10
                       '1d-1',   # 11
                       '1d-1',   # 12
                         '1d',   # 13
                         '1d',   # 14
                       '1d+1',   # 15
                       '1d+1',   # 16
                       '1d+2',   # 17
                       '1d+2',   # 18
                       '2d-1',   # 19
                       '2d-1',   # 20
                         '2d',   # 21
                         '2d',   # 22
                       '2d+1',   # 23
                       '2d+1',   # 24
                       '2d+2']   # 25

    self.swing =  [       '0',   #  0  <- Not Valid 
                          '0',   #  1
                          '0',   #  2
                          '0',   #  3
                          '0',   #  4
                       '1d-5',   #  5
                       '1d-4',   #  6
                       '1d-3',   #  7
                       '1d-2',   #  8
                       '1d-1',   #  9
                         '1d',   # 10
                       '1d+1',   # 11
                       '1d+2',   # 12
                       '2d-1',   # 13
                         '2d',   # 14
                       '2d+1',   # 15
                       '2d+2',   # 16
                       '3d-1',   # 17
                         '3d',   # 18
                       '3d+1',   # 19
                       '3d+2',   # 20
                       '4d-1',   # 21
                         '4d',   # 22
                       '4d+1',   # 23
                       '4d+2',   # 24
                       '5d-1']   # 25 
 

class Character:
  def __init__(self, *args):
    self.ST = Attribute(10)
    self.DX = Attribute(10)
    self.IQ = Attribute(10)
    self.HT = Attribute(10)

    self.d = Character_data()

    self.available_points = 100

  def set_character_name(self,name):
    '''Sets the character name'''
    self.d.name = name

  def get_character_name(self):
    return self.d.name

  def set_player_name(self,name):
    '''Sets the player name'''
    self.d.player = name

  def get_player_name(self):
    return self.d.player

  def pre_save(self):
    # Store some values before we pickle
    self.d.st_val = self.ST.value
    self.d.dx_val = self.DX.value
    self.d.iq_val = self.IQ.value
    self.d.ht_val = self.HT.value

  def post_load(self):
    # Restore attribute values
    self.ST = Attribute(self.d.st_val)
    self.DX = Attribute(self.d.dx_val)
    self.IQ = Attribute(self.d.iq_val)
    self.HT = Attribute(self.d.ht_val)

  def get_attr(self, attribute):
    if attribute == 'ST':
      return self.ST.value 
    elif attribute == 'DX':
      return self.DX.value
    elif attribute == 'IQ':
      return self.IQ.value
    elif attribute == 'HT':
      return self.HT.value
    else:
      return -1 

  def sorted_skill_keys(self):
    '''Returns a sorted list of the skill keys'''
    # XXX Todo
    # Important, this sorts the keys, not the names, we should fix this
    # eventually
    keys = self.d.skills.keys()
    keys.sort()
    return keys

  def has_skill(self,skill_id):
    return self.d.skills.has_key(skill_id)
 
  def sorted_advantage_keys(self):
    '''Returns a sorted list of the advantage keys'''
    # XXX Todo
    # Important, this sorts the keys, not the names, we should fix this
    # eventually
    keys = self.d.advantages.keys()
    keys.sort()
    return keys

  def sorted_quirk_keys(self):
    '''Returns a sorted list of the advantage keys'''
    keys = self.d.quirks.keys()
    keys.sort()
    return keys

  def has_advantage(self,skill_id):
    return self.d.advantages.has_key(skill_id)
 
  def attr_points(self):
    '''Returns the points used in attributes'''
    return self.ST.points + self.HT.points + self.IQ.points + self.DX.points

  def advantage_points(self):
    '''Returns the points used in advantages'''
    total_points = 0
    for a in self.d.advantages.keys():
      if self.d.advantages[a]['points'] > -1:
        total_points = total_points + self.d.advantages[a]['points']
    return total_points

  def disadvantage_points(self):
    '''Returns the points gained in disadvantages (probably a negative value)'''
    total_points = 0
    for a in self.d.advantages.keys():
      if self.d.advantages[a]['points'] < 0:
        total_points = total_points + self.d.advantages[a]['points']
    return total_points

  def quirk_points(self):
    '''Returns the points gained in quirks'''
    total_points = 0
    for q in self.d.quirks.keys():
      total_points = total_points - 1
    return total_points

  def skill_points(self):
    '''Returns the points used in skills'''
    total_points = 0
    for s in self.d.skills.keys():
      total_points = total_points + self.d.skills[s]['points']
    return total_points

  def total_points(self):
    '''Returns the totol character points'''
    return self.attr_points() + self.advantage_points() + \
      self.disadvantage_points() + self.quirk_points() + self.skill_points()

  def unused_points(self):
    '''Returns the unused points for this character'''
    return self.available_points - self.total_points()


  def set_available_points(self, points):
    '''Sets the available points for this character'''
    self.available_points = points

  def set_skill_db(self, skill_db):
    self.skill_db = skill_db

  def set_advantage_db(self, adv_db):
    self.advantage_db = adv_db

  def get_skill(self,skill):
    """Returns the skill level of a certain skill"""
    if self.d.skills.has_key(skill):
      return self.d.skills[skill]['level'] + self.d.skills[skill]['mod']
    return 0

  def remove_skill(self, skill_id):
    if self.d.skills.has_key(skill_id):
      skill_type_list = string.split(skill_id,'/')
      skill = skill_type_list[0]
      if self.skill_db.gives_modifiers(skill):
        # XXX TODO check for modifiers by this skill and remove
        print "Removing skill that gives modifiers, modif not removed"
      del(self.d.skills[skill_id])

  def remove_quirk(self, quirk):
    '''Removes a quirk'''
    if self.d.quirks.has_key(quirk):
      del(self.d.quirks[quirk])

  def remove_advantage(self, adv_id):
    '''Removes an advantage'''
    if self.d.advantages.has_key(adv_id):
      # Check for modifiers by this advantage
      if self.advantage_db.gives_modifiers(adv_id):
        for mod in string.split(self.advantage_db.db[adv_id][ABON],','):
          if mod == "":
            continue
          name,type,val = string.split(mod,'/')
          del(self.d.modifiers[name][adv_id])        
      del(self.d.advantages[adv_id])

  def add_skill(self,skill_id,points):
    """Adds a skill to a character"""
    skill_type_list = string.split(skill_id,'/')
    skill = skill_type_list[0]
    if not self.skill_db.db.has_key(skill):
      return -1
    if not self.d.skills.has_key(skill_id):
      self.d.skills[skill_id]={}
      self.d.skills[skill_id]['mod']=0
    self.d.skills[skill_id]['points']=points
    self.d.skills[skill_id]['level'] = self.skill_db.calculate_skill(self,
                                       skill, points)
    for mod in string.split(self.skill_db.db[skill][SBON],','):
      if mod == "":
        continue
      name,type,val = string.split(mod,'/')
      if not self.d.modifiers.has_key(name):
        self.d.modifiers[name]={}
      if self.d.modifiers[name].has_key(skill_id):
        print "Modifier", name, "already has key", skill_id,"  How come?"
      self.d.modifiers[name][skill_id]={}
      self.d.modifiers[name][skill_id]['type']=type
      self.d.modifiers[name][skill_id]['val']=val

    #print 'Adding skill ' + skills[skill_id][SNAME] + ' ',
    #print char['skills'][skill_id]['level']
    self.apply_skill_modifiers()
    return 0
 
  def add_skill_with_type(self,skill_id,points,type):
    """Adds a skill to a character"""
    if not self.skill_db.db.has_key(skill_id):
      return -1
    skill_type = skill_id + '/' + type
    if not self.d.skills.has_key(skill_type):
      self.d.skills[skill_type]={}
      self.d.skills[skill_type]['mod']=0
    self.d.skills[skill_type]['points']=points
    self.d.skills[skill_type]['level'] = self.skill_db.calculate_skill(self,
                                       skill_id, points)
    for mod in string.split(self.skill_db.db[skill_id][SBON],','):
      if mod == "":
        continue
      name,type,val = string.split(mod,'/')
      if not self.d.modifiers.has_key(name):
        self.d.modifiers[name]={}
      if self.d.modifiers[name].has_key(skill_id):
        print "Modifier", name, "already has key", skill_type,"  How come?"
      self.d.modifiers[name][skill_type]={}
      self.d.modifiers[name][skill_type]['type']=type
      self.d.modifiers[name][skill_type]['val']=val

    #print 'Adding skill ' + skills[skill_id][SNAME] + ' ',
    #print char['skills'][skill_id]['level']
    self.apply_skill_modifiers()
    return 0
   
  def add_quirk(self,quirk):
    """Adds a quirk to the character"""
    self.d.quirks[quirk] = {}
    self.d.quirks[quirk]['name'] = quirk
  
  def change_adv_lvl(self,adv_id,level):
    self.add_advantage(adv_id,level)

  def add_advantage(self,adv_id,level):
    """Adds an advantage to a character"""
    if not self.advantage_db.db.has_key(adv_id):
      # Skill does not exist in database, we can't add it
      return -1
    if level < 1 or level > int(self.advantage_db.db[adv_id][AMAXL]):
      # can't add skill at this level
      return -1
    self.d.advantages[adv_id]={}
    self.d.advantages[adv_id]['level']=level
    self.d.advantages[adv_id]['points']=self.advantage_db.calculate_advantage_cost(adv_id, level)
    for mod in string.split(self.advantage_db.db[adv_id][ABON],','):
      if mod == "":
        continue
      name,type,val = string.split(mod,'/')
      if not self.d.modifiers.has_key(name):
        self.d.modifiers[name]={}
      if self.d.modifiers[name].has_key(adv_id):
        # We are re-adding this skill, we should update the values.
        pass
      self.d.modifiers[name][adv_id]={}
      self.d.modifiers[name][adv_id]['type']=type
      self.d.modifiers[name][adv_id]['val']=val * level
    return 0
    
  def apply_attribute_modifiers(self):
    """Applies the modifeirs to attribute"""

  def apply_advantage_modifiers(self):
    """Applies the modifeirs to advantages"""

  def apply_skill_modifiers(self):
    """Applies the modifeirs to skills"""
    for sid in self.d.skills.keys():
      #print self.skill_db.db[sid][SNAME]
      self.d.skills[sid]['mod'] = 0
      skill_type_list = string.split(sid,'/')
      skill = skill_type_list[0]
      for mod in string.split(self.skill_db.db[skill][SMOD],','):
        #print mod
        if self.d.modifiers.has_key(mod):
          for mkey in self.d.modifiers[mod].keys():
            if self.d.modifiers[mod][mkey]['type'] == '+':
              self.d.skills[sid]['mod'] += int(self.d.modifiers[mod][mkey]['val'])
            elif self.d.modifiers[mod][mkey]['type'] == '-':
              self.d.skills[sid]['mod'] -= int(self.d.modifiers[mod][mkey]['val'])

  def apply_modifiers(self):
    """Applies the modifiers to skills, abilities, advantages, etc"""
    self.apply_attribute_modifiers()
    self.apply_advantage_modifiers()
    self.apply_skill_modifiers() 
   
  def update_skills(self):
    for s in self.d.skills.keys():
      self.add_skill(s,self.d.skills[s]['points'])

  def print_modifiers(self):
    for mod in self.d.modifiers.keys():
      print mod, self.d.modifiers[mod]['type'], self.d.modifiers[mod]['val']

  def get_move(self):
    # We need modifiers for this
    return (self.DX.value + self.HT.value) / 4.0
    
  def get_hits(self):
    # We need modifiers for this
    return self.HT.value

  def get_vision(self):
    # We need modifiers for this
    return self.IQ.value

  def get_will(self):
    # We need modifiers for this
    return self.IQ.value

  def get_hearing(self):
    # We need modifiers for this
    return self.IQ.value

  def get_taste_smell(self):
    # We need modifiers for this
    return self.IQ.value

  def get_fatigue(self):
    # We need modifiers for this
    return self.ST.value

  def get_thrust(self):
    return self.d.thrust[self.ST.value]

  def get_swing(self):
    return self.d.swing[self.ST.value]

  def get_punch(self):
    return self.d.thrust[self.ST.value]

  def get_kick(self):
    return self.d.thrust[self.ST.value]

  def get_bite(self):
    return self.d.thrust[self.ST.value/2]

  def apply_damage_modifer(self):
    ''' Applies the damage modifer '''
    # XXX TODO read the rules and calculate this
    pass

  def print_character(self):
    for line in self.tprint_character():
      print line,

  def print_to_file(self, filename):
    text_char = self.tprint_character()
    self.print_character()
    text_file=open(filename,'w')
    text_file.writelines(text_char)
    text_file.close()

  def tprint_character(self):
    text_char = []
    text_char = text_char + self.tprint_meta_info() 
    text_char.append('\n')
    text_char = text_char + self.tprint_attributes() 
    text_char.append('\n')
    text_char = text_char + self.tprint_stats()
    text_char.append('\n')
    text_char = text_char + self.tprint_advantages()
    text_char.append('\n')
    text_char = text_char + self.tprint_quirks()
    text_char.append('\n')
    text_char = text_char + self.tprint_skills()
    text_char.append('\n')
    text_char = text_char + self.tprint_overview()
    text_char.append('\n Generated with GCCP\n')
    return text_char

  def tprint_overview(self):
    """Prints a point overview of the character to a list"""
    overview = []
    overview.append('Overview:\n')
    overview.append(' Attributes:    '+ str(self.attr_points()) + '\n')
    overview.append(' Advantages:    '+ str(self.advantage_points()) + '\n')
    overview.append(' Disadvantages: '+ str(self.disadvantage_points()) + '\n')
    overview.append(' Quirks:        '+ str(self.quirk_points()) + '\n')
    overview.append(' Skills:        '+ str(self.skill_points()) + '\n')
    overview.append('\n')
    overview.append(' Total:         '+ str(self.total_points()) + '\n')
    return overview

  def tprint_quirks(self):
    """Prints the character quirks"""
    qtext = []
    qtext.append('Quirks\n')
    for q in self.d.quirks.keys():
      qtext.append(' -1 ' + self.d.quirks[q]['name'] + '\n')
    return qtext

  def tprint_meta_info(self):
    mtext = []
    mtext.append('Character Name: '+ self.d.name + '\n')
    mtext.append('Player Name:    '+ self.d.player + '\n')
    return mtext 

  def tprint_attributes(self):
    atext = []
    atext.append('Attributes\n')
    atext.append('  ST %3d (%3dp) \n' % (self.ST.value, self.ST.points))
    atext.append('  DX %3d (%3dp) \n' % (self.DX.value, self.DX.points))
    atext.append('  IQ %3d (%3dp) \n' % (self.IQ.value, self.IQ.points))
    atext.append('  HT %3d (%3dp) \n' % (self.HT.value, self.HT.points))
    return atext

  def tprint_stats(self):
    stext = []
    stext.append('Stats\n')
    stext.append('  Fatigue:     '+ str(self.get_fatigue()) + '\n')
    stext.append('  Will:        '+ str(self.get_will()) + '\n')
    stext.append('  Vision:      '+ str(self.get_vision()) + '\n')
    stext.append('  Hearing:     '+ str(self.get_hearing()) + '\n')
    stext.append('  Taste/Smell: '+ str(self.get_taste_smell()) + '\n')
    stext.append('  Hits:        '+ str(self.get_hits()) + '\n')
    stext.append('  Move:        '+ str(self.get_move()) + '\n')
    stext.append('  Thrust:      '+ self.get_thrust() + '\n')
    stext.append('  Swing:       '+ self.get_swing() + '\n')
    return stext

  def tprint_advantages(self):
    atext = []
    atext.append('Advantages\n')
    atext.append('  %3s' % 'pts' + '  Advantage Name\n')
    for aid in self.sorted_advantage_keys():
      if self.advantage_db.db[aid][AMAXL] != '1':
        atext.append('  %3s' % self.d.advantages[aid]['points'] + ' ' +
                     self.advantage_db.db[aid][ANAME] +
	  	     ' (lvl %s)' % self.d.advantages[aid]['level'] + '\n')
      else:
        atext.append('  %3s' % self.d.advantages[aid]['points'] + ' ' +
                     self.advantage_db.db[aid][ANAME] + '\n')
    return atext
        

  def tprint_skills(self):
    stext = []
    stext.append('Skills\n')
    stext.append(string.ljust('Skill Name',40) + 
                 '  %4s   %3s\n' % ('pts','lvl'))
    for sid in self.sorted_skill_keys():
      skill_type_list = string.split(sid,'/')
      skill = skill_type_list[0]
      sname  = self.skill_db.db[skill][SNAME]
      if len(skill_type_list) > 1:
        sname = sname + '(' + skill_type_list[1] + ')'
      stext.append(string.ljust(sname,40) +
                   '  %4.1f ' % self.d.skills[sid]['points'] +
                   '  %3s\n' % self.d.skills[sid]['level'])
    return stext
 
