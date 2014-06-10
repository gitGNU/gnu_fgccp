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


"""FGCCP

Free GURPS Character Creation Program"""

from character import *
from skills import *
from advantages import *
import pygtk
#pygtk.require('2.0')
import gtk 
import gobject
import pickle

WINDOW_NAME = 'FGCCP: Free GURPS Character Creation Program'

ALIGN_CENTER = 0.5

FGCCP_VERSION = '0.1 (alpha)'


#########################################################################
# Helper functions
def show_message(message):
  print message

#########################################################################
#
class Quirk_Window:
  def __init__(self, app):
    self.app_window = app
    self.COLUMN_QUIRK = 0
    self.window = gtk.Window()
    self.window.connect('destroy',self.cancel)
    self.window.set_title('Select Quirks')
    self.window.set_default_size(400,400)

    self.quirk_db = app.quirk_db

    vbox = gtk.VBox()
    self.window.add(vbox)
    
    self.quirk_table = gtk.TreeView(self.quirk_list_model())
    self.quirk_table.set_rules_hint(True)
    self.quirk_table.set_headers_visible(True)
    selection = self.quirk_table.get_selection()
    selection.set_mode(gtk.SELECTION_SINGLE)
    self.add_columns(self.quirk_table)

    sw = gtk.ScrolledWindow()
    sw.add(self.quirk_table)
    vbox.pack_start(sw)
    
    hbox = gtk.HBox()
    button = gtk.Button('Add Selected Quirk')
    button.connect('clicked', self.add_quirk)
    hbox.pack_start(button)
    button = gtk.Button('Done')
    button.connect('clicked', self.close_window)
    hbox.pack_start(button)
    button = gtk.Button('Cancel')
    button.connect('clicked', self.cancel)
    hbox.pack_start(button)

    vbox.pack_start(hbox, expand=False) 

  def show(self, arg):
    self.window.show_all()
 
  def cancel(self, args):
    self.window.hide()
 
  def quirk_list_model(self):
    model = gtk.ListStore(gobject.TYPE_STRING)
    for q in self.quirk_db.sorted_keys():
      iter = model.append()
      model.set(iter,
               self.COLUMN_QUIRK   , q)

    return model

  def close_window(self, arg):
    self.window.hide()

  def add_columns(self,quirk_table):
    model = quirk_table.get_model()

    renderer = gtk.CellRendererText()
    column = gtk.TreeViewColumn('Quirk', renderer,text=self.COLUMN_QUIRK)
    column.set_resizable(True)
    column.set_min_width(250)
    quirk_table.append_column(column)

  def add_quirk(self, arg):
    selection = self.quirk_table.get_selection()
    selected  = selection.get_selected()
    if selected:
      model, iter = selected
      i = model.get_value(iter,self.COLUMN_QUIRK)
      self.app_window.add_quirk(i)
 
#########################################################################
#
class Skill_Window:
  def __init__( self, app ):
    self.COLUMN_NAME       = 0
    self.COLUMN_DIFF       = 1
    self.COLUMN_DEFAULT    = 2
    self.COLUMN_ID         = 3
    self.window = gtk.Window()
    self.window.connect('destroy', self.cancel)
    self.window.set_title('Select Skills')
    self.window.set_default_size(400,400)

    self.app_window= app
    
    self.skill_db = app.skill_db

    vbox = gtk.VBox()
    self.window.add(vbox)
    
    self.skill_table = gtk.TreeView(self.skill_list_model())
    self.skill_table.set_rules_hint(True)
    self.skill_table.set_headers_visible(True)
    selection = self.skill_table.get_selection()
    selection.set_mode(gtk.SELECTION_SINGLE)
    self.add_columns(self.skill_table)

    sw = gtk.ScrolledWindow()
    sw.add(self.skill_table)
    vbox.pack_start(sw)
    
    hbox = gtk.HBox()
    button = gtk.Button('Add Selected Skills')
    button.connect('clicked', self.add_skill)
    hbox.pack_start(button)
    button = gtk.Button('Done')
    button.connect('clicked', self.close_window)
    hbox.pack_start(button)
    button = gtk.Button('Cancel')
    button.connect('clicked', self.cancel)
    hbox.pack_start(button)

    vbox.pack_start(hbox, expand=False) 

  def add_skill(self, arg):
    selection = self.skill_table.get_selection()
    selected  = selection.get_selected()
    if selected:
      model, iter = selected
      i = model.get_value(iter,self.COLUMN_ID)
      self.app_window.add_skill(i)
      
  
  def cancel(self, args):
    self.window.hide()

  def show(self, args):
    self.window.show_all()
 
  def skill_list_model(self):
    model = gtk.ListStore(gobject.TYPE_STRING,
                          gobject.TYPE_STRING,
                          gobject.TYPE_STRING,
        		  gobject.TYPE_STRING)
    for sid in self.skill_db.sorted_keys():
      iter = model.append()
      skill = self.skill_db.db[sid]
      model.set(iter,
               self.COLUMN_NAME   , skill[SNAME],
               self.COLUMN_DIFF   , skill[SDIFF],
               self.COLUMN_DEFAULT, skill[SDEF],
               self.COLUMN_ID     , skill[SID])
    return model

  def close_window(self, arg):
    self.window.hide()

  def add_columns(self,skill_table):
    model = skill_table.get_model()

    renderer = gtk.CellRendererText()
    column = gtk.TreeViewColumn('Skill', renderer,text=self.COLUMN_NAME)
    column.set_resizable(True)
    column.set_min_width(250)
    skill_table.append_column(column)

    renderer = gtk.CellRendererText()
    column = gtk.TreeViewColumn('Diff', renderer, text=self.COLUMN_DIFF)
    column.set_resizable(True)
    skill_table.append_column(column)

    #renderer = gtk.CellRendererText()
    #column = gtk.TreeViewColumn('Default', renderer,text=COLUMN_LEVEL)
    #column.set_resizable(True)
    #skill_table.append_column(column)

#########################################################################
#

class Advantage_Window:
  def __init__( self, app ):
    self.COLUMN_POINTS = 0
    self.COLUMN_NAME   = 1
    self.COLUMN_ID     = 2
    self.window = gtk.Window()
    self.window.connect('destroy', self.cancel)
    self.window.set_title('Select Advantage/Disadvantages')
    self.window.set_default_size(400,400)

    self.app_window= app
    self.adv_db = app.advantage_db

    vbox = gtk.VBox()
    self.window.add(vbox)
    
    self.adv_table = gtk.TreeView(self.adv_list_model())
    self.adv_table.set_rules_hint(True)
    self.adv_table.set_headers_visible(True)
    selection = self.adv_table.get_selection()
    selection.set_mode(gtk.SELECTION_SINGLE)
    self.add_columns(self.adv_table)

    sw = gtk.ScrolledWindow()
    sw.add(self.adv_table)
    vbox.pack_start(sw)
    
    hbox = gtk.HBox()
    button = gtk.Button('Add Selected Advantage')
    button.connect('clicked', self.add_adv)
    hbox.pack_start(button)
    button = gtk.Button('Done')
    button.connect('clicked', self.close_window)
    hbox.pack_start(button)
    button = gtk.Button('Cancel')
    button.connect('clicked', self.cancel)
    hbox.pack_start(button)

    vbox.pack_start(hbox, expand=False) 
  
  def cancel(self, args):
    self.window.hide()

  def show(self, args):
    self.window.show_all()
 
  def adv_list_model(self):
    model = gtk.ListStore(gobject.TYPE_STRING,
                          gobject.TYPE_STRING,
        		  gobject.TYPE_STRING)
    for adv in self.adv_db.sorted_keys():
      iter = model.append()
      a = self.adv_db.db[adv]
      model.set(iter,
               self.COLUMN_POINTS, a[AINIT],
               self.COLUMN_NAME, a[ANAME],
               self.COLUMN_ID, a[AID])
    return model

  def add_adv(self, arg):
    selection = self.adv_table.get_selection()
    selected  = selection.get_selected()
    if selected:
      model, iter = selected
      i = model.get_value(iter,self.COLUMN_ID)
      self.app_window.add_adv(i)
 

  def close_window(self, arg):
    self.window.hide()

  def add_columns(self,adv_table):
    model = adv_table.get_model()

    renderer = gtk.CellRendererText()
    column = gtk.TreeViewColumn('Points', renderer,text=self.COLUMN_POINTS)
    column.set_resizable(True)
    adv_table.append_column(column)

    renderer = gtk.CellRendererText()
    column = gtk.TreeViewColumn('Advantage/Disadvantage', 
                                renderer, text=self.COLUMN_NAME)
    column.set_resizable(True)
    column.set_min_width(250)
    adv_table.append_column(column)



#########################################################################
#

class Fgccp_App:
  def __init__( self, *args ):
    self.SCOLUMN_NAME     = 0
    self.SCOLUMN_DIFF     = 1
    self.SCOLUMN_POINTS   = 2
    self.SCOLUMN_LEVEL    = 3
    self.SCOLUMN_ID       = 4
    self.SCOLUMN_EDITABLE = 5

    self.ACOLUMN_POINTS   = 0
    self.ACOLUMN_NAME     = 1
    self.ACOLUMN_LVL      = 2
    self.ACOLUMN_ID       = 3
    self.ACOLUMN_EDITABLE = 4

    # Set up the main window
    self.window = gtk.Window()
    self.window.connect('destroy', self.exit_gccp)
    self.window.set_title(WINDOW_NAME)
    self.window.set_default_size(400,400)

    # Set up acceleration..
    self.accel_group = gtk.AccelGroup()
    self.window.add_accel_group(self.accel_group)

    # Create a character
    self.char         = Character()
    self.filename     = ''
    self.skill_db     = Skill_db()
    self.skill_db.add_skill_file('skills.dat')
    self.advantage_db = Advantage_db()
    self.advantage_db.add_advantage_file('advantages.dat')
    self.quirk_db = Quirk_db()
    self.quirk_db.add_quirk_file('quirks.dat')
    self.char.set_skill_db(self.skill_db)
    self.char.set_advantage_db(self.advantage_db)

    # Create the other windows and have them ready
    self.skill_list_window = Skill_Window(self)
    self.adv_list_window   = Advantage_Window(self)
    self.quirk_list_window = Quirk_Window(self)

    # Let's pack everthing into a VBox
    vbox = gtk.VBox()
    self.window.add(vbox)

    # Start with a menubar
    self.menubar = self.create_menubar()
    vbox.pack_start(self.menubar, expand=False)

    # Then a notebook
    #self.notebook = self.create_notebook()
    #vbox.pack_start(self.notebook)
    self.panes = self.create_panes()
    vbox.pack_start(self.panes)
    

    # Then the statusbar
    self.statusbar = self.create_statusbar()
    vbox.pack_start(self.statusbar, expand=False)

    # Clear the character
    self.redraw_character()
    
  def exit_gccp(self,arg):
    gtk.main_quit()

  def create_statusbar(self):
    statusbar = gtk.Statusbar()
    return statusbar
    
  # old definition of notebook
  def create_notebook(self):
    notebook = gtk.Notebook()

    self.create_stats_page(notebook)
    self.create_advantage_page(notebook)
    self.create_skill_page(notebook)
    return notebook

  def create_panes(self):
    stats_pane    = self.create_stats_pane()
    adv_pane      = self.create_adv_pane()
    skill_pane    = self.create_skill_pane()
    overview_pane = self.create_overview_pane()
    
    pane = gtk.HPaned()
    lpane = gtk.VPaned()
    rpane = gtk.VPaned()

    stats_pane.set_size_request(400, 300)
    adv_pane.set_size_request(400, 300)
    skill_pane.set_size_request(400, 450)
    overview_pane.set_size_request(400, 150)

    lpane.add(stats_pane)
    lpane.add2(adv_pane)
    rpane.add(skill_pane)
    rpane.add2(overview_pane)
    
    pane.add(lpane)
    pane.add2(rpane)

    return pane

  def create_stats_pane(self):
    table = gtk.Table(2,3)
    table.set_border_width(4)
    table.set_col_spacings(4)
    table.set_row_spacings(4)

    frame = gtk.Frame('Character')
    chartable=gtk.Table(2,2)
    frame.add(chartable)
    table.attach(frame,0,2,0,1)

    label = gtk.Label('Character Name:')
    self.cnamelabel = gtk.Label('')
    hbox = gtk.HBox()
    hbox.pack_start(label, False, False,5)
    hbox.pack_start(self.cnamelabel, False, False)
    chartable.attach(hbox,0,1,0,1)

    label = gtk.Label('Player Name:')
    self.pnamelabel = gtk.Label('')
    hbox = gtk.HBox()
    hbox.pack_start(label, False, False,5)
    hbox.pack_start(self.pnamelabel, False, False)
    chartable.attach(hbox,0,1,1,2)

    label = gtk.Label('Points:')
    self.tpointslabel = gtk.Label('0')
    hbox = gtk.HBox()
    hbox.pack_start(label, False, False,5)
    hbox.pack_start(self.tpointslabel, False, False)
    chartable.attach(hbox,1,2,0,1)

    label = gtk.Label('Unspent:')
    self.upointslabel = gtk.Label('0')
    hbox = gtk.HBox()
    hbox.pack_start(label, False, False,5)
    hbox.pack_start(self.upointslabel, False, False)
    chartable.attach(hbox,1,2,1,2)


    

    frame = gtk.Frame("Attributes")
    attr_table = gtk.Table(3,4)
    frame.add(attr_table)
    table.attach(frame,0,1,1,2)

    label = gtk.Label('ST')
    adj = gtk.Adjustment(10,1,25,1)
    self.attr_st   = gtk.SpinButton(adj)
    self.points_st = gtk.Label('0')
    attr_table.attach(label,0,1,0,1)
    attr_table.attach(self.attr_st,1,2,0,1)
    attr_table.attach(self.points_st,2,3,0,1)
    self.attr_st.connect('changed',self.change_attr_st)
    self.attr_st.connect('value-changed',self.change_attr_st)
 
    label = gtk.Label('DX')
    adj = gtk.Adjustment(10,1,25,1)
    self.attr_dx   = gtk.SpinButton(adj)
    self.points_dx = gtk.Label('0')
    attr_table.attach(label,0,1,1,2)
    attr_table.attach(self.attr_dx,1,2,1,2)
    attr_table.attach(self.points_dx,2,3,1,2)
    self.attr_dx.connect('changed',self.change_attr_dx)
    self.attr_dx.connect('value-changed',self.change_attr_dx)
  
    label = gtk.Label('IQ')
    adj = gtk.Adjustment(10,1,25,1)
    self.attr_iq   = gtk.SpinButton(adj)
    self.points_iq = gtk.Label('0')
    attr_table.attach(label,0,1,2,3)
    attr_table.attach(self.attr_iq,1,2,2,3)
    attr_table.attach(self.points_iq,2,3,2,3)
    self.attr_iq.connect('changed',self.change_attr_iq)
    self.attr_iq.connect('value-changed',self.change_attr_iq)
   
    label = gtk.Label('HT')
    adj = gtk.Adjustment(10,1,25,1)
    self.attr_ht   = gtk.SpinButton(adj)
    self.points_ht = gtk.Label('0')
    attr_table.attach(label,0,1,3,4)
    attr_table.attach(self.attr_ht,1,2,3,4)
    attr_table.attach(self.points_ht,2,3,3,4) 
    self.attr_ht.connect('changed',self.change_attr_ht)
    self.attr_ht.connect('value-changed',self.change_attr_ht)

    frame = gtk.Frame('Movement')
    table.attach(frame,0,1,2,3)
    hbox = gtk.HBox()
    frame.add(hbox)
    label = gtk.Label('Move:')
    hbox.pack_start(label,False, False,5)
    self.movelabel = gtk.Label('5')
    hbox.pack_start(self.movelabel,False, False)
    
    frame = gtk.Frame('Stats')
    table.attach(frame,1,2,1,3)
    vbox = gtk.VBox()
    frame.add(vbox)

    hbox = gtk.HBox()
    label = gtk.Label('Fatigue:')
    self.fatiguelabel = gtk.Label('10')
    hbox.pack_start(label, False, False,5)
    hbox.pack_start(self.fatiguelabel,False, False)
    vbox.pack_start(hbox, True, True)

    hbox = gtk.HBox()
    label = gtk.Label('Will:')
    self.willlabel = gtk.Label('10')
    hbox.pack_start(label, False, False,5)
    hbox.pack_start(self.willlabel,False, False)
    vbox.pack_start(hbox, True, True)

    hbox = gtk.HBox()
    label = gtk.Label('Vision:')
    self.visionlabel = gtk.Label('10')
    hbox.pack_start(label, False, False,5)
    hbox.pack_start(self.visionlabel,False, False)
    vbox.pack_start(hbox, True, True)

    hbox = gtk.HBox()
    label = gtk.Label('Hearing:')
    self.hearinglabel = gtk.Label('10')
    hbox.pack_start(label, False, False,5)
    hbox.pack_start(self.hearinglabel,False, False)
    vbox.pack_start(hbox, True, True)

    hbox = gtk.HBox()
    label = gtk.Label('Taste/Smell:')
    self.tastesmelllabel = gtk.Label('10')
    hbox.pack_start(label, False, False,5)
    hbox.pack_start(self.tastesmelllabel,False, False)
    vbox.pack_start(hbox, True, True)

    hbox = gtk.HBox()
    label = gtk.Label('Hits:')
    self.hitslabel = gtk.Label('10')
    hbox.pack_start(label, False, False,5)
    hbox.pack_start(self.hitslabel,False, False)
    vbox.pack_start(hbox, True, True)

    hbox = gtk.HBox()
    label = gtk.Label('Thurst:')
    self.thrustlabel = gtk.Label('1d-1')
    hbox.pack_start(label, False, False,5)
    hbox.pack_start(self.thrustlabel,False, False)
    vbox.pack_start(hbox, True, True)

    hbox = gtk.HBox()
    label = gtk.Label('Swing:')
    self.swinglabel = gtk.Label('1d-2')
    hbox.pack_start(label, False, False,5)
    hbox.pack_start(self.swinglabel,False, False)
    vbox.pack_start(hbox, True, True)

    # This hasn't been correctly implemented yet
    if 0:
      hbox = gtk.HBox()
      label = gtk.Label('Punch:')
      self.punchlabel = gtk.Label('1d-1')
      hbox.pack_start(label, False, False,5)
      hbox.pack_start(self.punchlabel,False, False)
      vbox.pack_start(hbox, True, True)

      hbox = gtk.HBox()
      label = gtk.Label('Kick:')
      self.kicklabel = gtk.Label('1d-2')
      hbox.pack_start(label, False, False,5)
      hbox.pack_start(self.kicklabel,False, False)
      vbox.pack_start(hbox, True, True)

      hbox = gtk.HBox()
      label = gtk.Label('Bite:')
      self.bitelabel = gtk.Label('1d-2')
      hbox.pack_start(label, False, False,5)
      hbox.pack_start(self.bitelabel,False, False)
      vbox.pack_start(hbox, True, True)

    return table

  def create_overview_pane(self):
    vbox = gtk.VBox()

    label = gtk.Label('Stats:')
    label.set_justify(gtk.JUSTIFY_RIGHT)
    self.totals_stats_label = gtk.Label('0')
    label.set_justify(gtk.JUSTIFY_RIGHT)
    hbox = gtk.HBox()
    hbox.pack_start(label, False, False,5)
    hbox.pack_start(self.totals_stats_label, False, False)
    vbox.pack_start(hbox, True, True)
    
    label = gtk.Label('Skills:')
    label.set_justify(gtk.JUSTIFY_RIGHT)
    self.totals_skills_label = gtk.Label('0')
    label.set_justify(gtk.JUSTIFY_RIGHT)
    hbox = gtk.HBox()
    hbox.pack_start(label, False, False,5)
    hbox.pack_start(self.totals_skills_label, False, False)
    vbox.pack_start(hbox, True, True)

    label = gtk.Label('Adv:')
    label.set_justify(gtk.JUSTIFY_RIGHT)
    self.totals_adv_label = gtk.Label('0')
    label.set_justify(gtk.JUSTIFY_RIGHT)
    hbox = gtk.HBox()
    hbox.pack_start(label, False, False,5)
    hbox.pack_start(self.totals_adv_label, False, False)
    vbox.pack_start(hbox, True, True)

    label = gtk.Label('Dis:')
    label.set_justify(gtk.JUSTIFY_RIGHT)
    self.totals_dis_label = gtk.Label('0')
    label.set_justify(gtk.JUSTIFY_RIGHT)
    hbox = gtk.HBox()
    hbox.pack_start(label, False, False,5)
    hbox.pack_start(self.totals_dis_label, False, False)
    vbox.pack_start(hbox, True, True)
    
    label = gtk.Label('Quirks:')
    label.set_justify(gtk.JUSTIFY_RIGHT)
    self.totals_quirks_label = gtk.Label('0')
    label.set_justify(gtk.JUSTIFY_RIGHT)
    hbox = gtk.HBox()
    hbox.pack_start(label, False, False,5)
    hbox.pack_start(self.totals_quirks_label, False, False)
    vbox.pack_start(hbox, True, True)

    label = gtk.Label('Total:')
    label.set_justify(gtk.JUSTIFY_RIGHT)
    self.totals_total_label = gtk.Label('0')
    label.set_justify(gtk.JUSTIFY_RIGHT)
    hbox = gtk.HBox()
    hbox.pack_start(label, False, False,5)
    hbox.pack_start(self.totals_total_label, False, False)
    vbox.pack_start(hbox, True, True)

    frame = gtk.Frame('Overview')
    frame.add(vbox)
    frame.set_border_width(4)

    return frame

  def create_skill_pane(self):
    vbox = gtk.VBox()
    
    self.skill_table = gtk.TreeView(self.skill_model())
    self.skill_table.set_rules_hint(True)
    self.skill_table.set_headers_visible(True)
    selection = self.skill_table.get_selection()
    selection.set_mode(gtk.SELECTION_SINGLE)
    self.add_skill_columns(self.skill_table)

    sw = gtk.ScrolledWindow()
    sw.add(self.skill_table)
    sw.set_border_width(4)
    vbox.pack_start(sw, padding=4)

    hbox = gtk.HBox()
    button = gtk.Button('Add Skill')
    #button.connect('clicked', self.skill_list_window.show, 'None')
    button.connect('clicked', self.skill_list_window.show)
    hbox.pack_start(button, padding=4)
    button = gtk.Button('Add Defaults')
    button.connect('clicked', self.add_default_skills)
    hbox.pack_start(button, padding=4)
    button = gtk.Button('Remove Skill')
    button.connect('clicked', self.remove_skill)
    hbox.pack_start(button, padding=4)

    vbox.pack_start(hbox, False, False, 4) 
    
    frame = gtk.Frame('Skills')
    frame.add(vbox)
    frame.set_border_width(4)

    return(frame)

  def add_default_skills(self, arg):
    self.menubar.show()
    show_message('Add Default Skills not implemented yet')

  def remove_skill(self, arg):
    selection = self.skill_table.get_selection()
    selected  = selection.get_selected()
    if selected:
      model, iter = selected
      if iter:
        i = model.get_value(iter,self.SCOLUMN_ID)
        self.char.remove_skill(i)
        self.recalculate_skills()
        self.update_totals()

  def remove_adv(self, arg):
    selection = self.advantage_table_tv.get_selection()
    selected  = selection.get_selected()
    if selected:
      model, iter = selected
      if iter:
        i = model.get_value(iter,self.ACOLUMN_ID)
	if i == 'quirk':
	  q = model.get_value(iter,self.ACOLUMN_NAME)
	  self.char.remove_quirk(q)
	else:
          self.char.remove_advantage(i)
        self.recalculate_skills()
        self.reprint_advantages()
        self.update_totals()


 
  
  def create_adv_pane(self):
    vbox = gtk.VBox()

    self.advantage_table_tv = gtk.TreeView(self.adv_model())
    self.advantage_table_tv.set_rules_hint(True)
    self.advantage_table_tv.set_headers_visible(True)
    selection = self.advantage_table_tv.get_selection()
    selection.set_mode(gtk.SELECTION_SINGLE)
    self.add_adv_columns(self.advantage_table_tv)
 
    sw = gtk.ScrolledWindow()
    sw.add(self.advantage_table_tv)
    sw.set_border_width(4)
    vbox.pack_start(sw, True, True, 4)
   
    hbox = gtk.HBox(spacing=2)
    button = gtk.Button('Add Adv/Dis')
    #button.connect('clicked', self.skill_list_window.show, 'None')
    button.connect('clicked', self.adv_list_window.show)
    hbox.pack_start(button, padding=4)
    button = gtk.Button('Add Quirk')
    button.connect('clicked', self.quirk_list_window.show)
    hbox.pack_start(button, padding=4)
    button = gtk.Button('Delete Adv/Dis')
    button.connect('clicked', self.remove_adv)
    hbox.pack_start(button, padding=4)
    

    vbox.pack_start(hbox, False, False, 4) 
   
    frame = gtk.Frame('Advantage/Disadvantage/Quirks')
    frame.add(vbox)
    frame.set_border_width(4)

    return(frame)

  def adv_model(self):
    model = gtk.TreeStore(gobject.TYPE_INT,
                          gobject.TYPE_STRING,
                          gobject.TYPE_STRING,
                          gobject.TYPE_STRING,
			  gobject.TYPE_BOOLEAN)
    return model


 
  def add_adv_columns(self, adv_tv):
    model = adv_tv.get_model()

    renderer = gtk.CellRendererText()
    column = gtk.TreeViewColumn('Points', renderer,text=self.ACOLUMN_POINTS)
    column.set_resizable(True)
    column.set_alignment(ALIGN_CENTER)
    adv_tv.append_column(column)

    renderer = gtk.CellRendererText()
    column = gtk.TreeViewColumn('Advantage/Disadvantage/Quirk', 
                                renderer, text=self.ACOLUMN_NAME)
    column.set_resizable(True)
    column.set_min_width(250)
    column.set_alignment(ALIGN_CENTER)
    adv_tv.append_column(column)

    renderer = gtk.CellRendererText()
    renderer.connect('edited', self.change_adv_lvl, model)
    column = gtk.TreeViewColumn('Lvl', renderer, text=self.ACOLUMN_LVL, 
                                editable=self.ACOLUMN_EDITABLE)
    column.set_resizable(True)
    column.set_alignment(ALIGN_CENTER)
    adv_tv.append_column(column)

  def add_skill_columns(self,skill_table):
    model = skill_table.get_model()

    renderer = gtk.CellRendererText()
    column = gtk.TreeViewColumn('Skill', renderer,text=self.SCOLUMN_NAME)
    column.set_resizable(True)
    column.set_min_width(250)
    skill_table.append_column(column)

    renderer = gtk.CellRendererText()
    column = gtk.TreeViewColumn('Diff', renderer, text=self.SCOLUMN_DIFF)
    column.set_resizable(True)
    column.set_alignment(ALIGN_CENTER)
    skill_table.append_column(column)

    renderer = gtk.CellRendererText()
    renderer.connect('edited', self.change_skill_points, model)
    column = gtk.TreeViewColumn('Pts', renderer, text=self.SCOLUMN_POINTS,
                                editable=self.SCOLUMN_EDITABLE)
    column.set_resizable(True)
    column.set_alignment(ALIGN_CENTER)
    skill_table.append_column(column)

    renderer = gtk.CellRendererText()
    column = gtk.TreeViewColumn('Level', renderer,text=self.SCOLUMN_LEVEL)
    column.set_resizable(True)
    column.set_alignment(ALIGN_CENTER)
    skill_table.append_column(column)

  def skill_model(self):
    model = gtk.ListStore(gobject.TYPE_STRING,
                          gobject.TYPE_STRING,
                          gobject.TYPE_STRING,
                          gobject.TYPE_INT,
                          gobject.TYPE_STRING,
                          gobject.TYPE_BOOLEAN)
    return model

  def menu_cb(self, window, action, widget):
    print 'You selected an unimplemented menu option'

  def quit_cb(self, *args):
    self.exit_gccp(0)

  def set_info_cb(self, *args):
    '''Sets the character information'''
    dialog = gtk.Dialog("Enter Character info", self.window, 0 ,
                        (gtk.STOCK_OK, gtk.RESPONSE_OK,
                         gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL))
    hbox = gtk.HBox(False)
    hbox.set_border_width(8)
    label = gtk.Label('Character Name:')
    hbox.pack_start(label)
    char_name_entry = gtk.Entry()
    hbox.pack_start(char_name_entry)
    dialog.vbox.pack_start(hbox)

    hbox = gtk.HBox(False)
    hbox.set_border_width(8)
    label = gtk.Label('Player Name:')
    hbox.pack_start(label)
    player_name_entry = gtk.Entry()
    hbox.pack_start(player_name_entry)
    dialog.vbox.pack_start(hbox)
    dialog.show_all()

    response = dialog.run()

    if response == gtk.RESPONSE_OK:
      self.char.set_character_name(char_name_entry.get_text())
      self.char.set_player_name(player_name_entry.get_text())
      self.cnamelabel.set_text(str(self.char.get_character_name()))
      self.pnamelabel.set_text(str(self.char.get_player_name()))
    dialog.destroy()

  def about_cb(self, *args):
    '''Displays the about box'''
    dialog = gtk.Dialog("About GCCP", self.window, 0,
                        (gtk.STOCK_OK, gtk.RESPONSE_OK))
    label = gtk.Label('GCCP version ' + GCCP_VERSION)
    dialog.vbox.pack_start(label)
    label = gtk.Label('http://www.igso.net/gccp')
    dialog.vbox.pack_start(label)
    label = gtk.Label('Ignacio Solis <isolis@igso.net>')
    dialog.vbox.pack_start(label)
    dialog.show_all()
    dialog.run()
    dialog.destroy()
    

  def create_menubar(self):
    self.menu_items = (
      ('/_File',                   None,         None,         0, '<Branch>'),
      ('/File/_New Character',     '<control>N', self.menu_cb, 0, '<StockItem>', gtk.STOCK_NEW),
      ('/File/_Open Character',    '<control>O', self.load_character_cb, 0, '<StockItem>', gtk.STOCK_OPEN),
      ('/File/_Save Character',    '<control>S', self.save_character_cb, 0, '<StockItem>', gtk.STOCK_SAVE),
      ('/File/Save Character _As', '<control>A', self.save_character_as_cb, 0, '<StockItem>', gtk.STOCK_SAVE),
      ('/File/sep1',               None,         self.menu_cb, 0, '<Separator>'),
      ('/File/_Print Character',   '<control>P', self.print_cb, 0, '<StockItem>', gtk.STOCK_PRINT),
      ('/File/sep1',               None,         self.menu_cb, 0, '<Separator>'),
      ('/File/_Quit',              '<control>Q', self.quit_cb, 0, '<StockItem>', gtk.STOCK_QUIT),

      ('/_Edit',                      None,         None,             0, '<Branch>'),
      ('/_Edit/_Set Character Info',  '<control>I', self.set_info_cb, 0, ''),

      ('/_Prefernces',                        None, None,         0, '<Branch>'),
      ('/_Prefernces/_Load Dat',              None, None,         0, '<Branch>'),
      ('/_Prefernces/Load Dat/_Skills',       None, self.menu_cb, 0, ''),
      ('/_Prefernces/Load Dat/_Advantages',   None, self.menu_cb, 0, ''),
      ('/_Prefernces/Load Dat/_Quirks',       None, self.menu_cb, 0, ''),
      ('/_Prefernces/_Unload Dat',            None, None,         0, '<Branch>'),
      ('/_Prefernces/Unload Dat/_Skills',     None, self.menu_cb, 0, ''),
      ('/_Prefernces/Unload Dat/_Advantages', None, self.menu_cb, 0, ''),
      ('/_Prefernces/Unload Dat/_Quirks',     None, self.menu_cb, 0, ''),
      ('/_Help',        None, None,         0, '<LastBranch>'),
      ('/_Help/_About', None, self.about_cb, 0, ''),
      ('/_Help/_Dat Format', None, self.menu_cb, 0, ''),
      )
    self.item_factory = gtk.ItemFactory(gtk.MenuBar,'<main>',self.accel_group)
    self.item_factory.create_items(self.menu_items,self.window)

    return self.item_factory.get_widget('<main>')




  def run(self):
    self.window.show_all()
    gtk.main()

 
  def change_attr_st(self, arg):
    self.char.ST.set_value(int(self.attr_st.get_value()))
    self.points_st.set_text(str(self.char.ST.points))
    self.recalculate_skills()
    self.update_totals()

  def change_attr_dx(self, arg):
    self.char.DX.set_value(int(self.attr_dx.get_value()))
    self.points_dx.set_text(str(self.char.DX.points))
    self.recalculate_skills()
    self.update_totals()

  def change_attr_iq(self, arg):
    self.char.IQ.set_value(int(self.attr_iq.get_value()))
    self.points_iq.set_text(str(self.char.IQ.points))
    self.recalculate_skills()
    self.update_totals()

  def change_attr_ht(self, arg):
    self.char.HT.set_value(int(self.attr_ht.get_value()))
    self.points_ht.set_text(str(self.char.HT.points))
    self.recalculate_skills()
    self.update_totals()

  def redraw_attr(self):
    self.points_st.set_text(str(self.char.ST.points))
    self.attr_st.set_value(self.char.ST.value)
    self.points_dx.set_text(str(self.char.DX.points))
    self.attr_dx.set_value(self.char.DX.value)
    self.points_iq.set_text(str(self.char.IQ.points))
    self.attr_iq.set_value(self.char.IQ.value)
    self.points_ht.set_text(str(self.char.HT.points))
    self.attr_ht.set_value(self.char.HT.value)

  def update_totals(self):
    self.totals_stats_label.set_text(str(self.char.attr_points()))
    self.totals_adv_label.set_text(str(self.char.advantage_points()))
    self.totals_dis_label.set_text(str(self.char.disadvantage_points()))
    self.totals_quirks_label.set_text(str(self.char.quirk_points()))
    self.totals_skills_label.set_text(str(self.char.skill_points()))
    self.totals_total_label.set_text(str(self.char.total_points()))
    self.tpointslabel.set_text(str(self.char.total_points()))
    self.upointslabel.set_text(str(self.char.unused_points()))
    self.update_stats()

  def update_stats(self):
    self.fatiguelabel.set_text(str(self.char.get_fatigue()))
    self.willlabel.set_text(str(self.char.get_will()))
    self.visionlabel.set_text(str(self.char.get_vision()))
    self.hearinglabel.set_text(str(self.char.get_hearing()))
    self.tastesmelllabel.set_text(str(self.char.get_taste_smell()))
    self.hitslabel.set_text(str(self.char.get_hits()))
    self.movelabel.set_text(str(self.char.get_move()))
    self.thrustlabel.set_text(str(self.char.get_thrust()))
    self.swinglabel.set_text(str(self.char.get_swing()))
    #self.punchlabel.set_text(str(self.char.get_punch()))
    #self.kicklabel.set_text(str(self.char.get_kick()))
    #self.bitelabel.set_text(str(self.char.get_bite()))

  def change_skill_points(self, cell, row, new_text, model):
    iter = model.get_iter_from_string(row)
    sid  = model.get_value(iter,self.SCOLUMN_ID)
    try:
      point = int(new_text)
      new_points = new_text
    except:
      new_points = '0.5'
    model.set(iter, self.SCOLUMN_POINTS, new_points)
    self.char.add_skill(sid,float(new_points))
    self.recalculate_skills()

    self.update_totals()

  def change_adv_lvl(self, cell, row, new_text, model):
    iter    = model.get_iter_from_string(row)
    adv_id  = model.get_value(iter,self.ACOLUMN_ID)
    model.set(iter, self.ACOLUMN_LVL, new_text)
    try:
      new_points = int(new_text)
    except:
      new_points = 1
    self.char.change_adv_lvl(adv_id,new_points)
    self.reprint_advantages()
    self.update_totals()
    

  def add_quirk(self,quirk):
    self.char.add_quirk(quirk)
    self.reprint_advantages()
    self.update_totals()
    
  def add_skill(self,skill_id):
    '''Adds a skill to the character. This should probably ask for type
    if a type is needed'''
    if self.char.has_skill(skill_id):
      # This should check for type ??
      return
    if self.skill_db.takes_type(skill_id):
      self.add_skill_with_type(skill_id)
      return
    self.char.add_skill(skill_id,0)
    self.recalculate_skills()

  def add_skill_with_type(self,skill_id):
    dialog = gtk.Dialog("Enter Type", self.window, 0 ,
                        (gtk.STOCK_OK, gtk.RESPONSE_OK,
                         gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL))
    hbox = gtk.HBox(False)
    hbox.set_border_width(8)
    dialog.vbox.pack_start(hbox)

    label = gtk.Label(self.skill_db.db[skill_id][SNAME] + ' type:')
    hbox.pack_start(label)
    entry = gtk.Entry()
    hbox.pack_start(entry)

    dialog.show_all()

    response = dialog.run()

    if response == gtk.RESPONSE_OK:
      self.char.add_skill_with_type(skill_id,0,entry.get_text())
      self.recalculate_skills()

    dialog.destroy()

  def recalculate_skills(self):
    model = self.skill_table.get_model()
    model.clear()
    self.char.update_skills()
    for s in self.char.sorted_skill_keys():
      skill_type_list = string.split(s,'/')
      sid = skill_type_list[0]
      skill  = self.skill_db.db[sid]      
      sname = skill[SNAME]
      if len(skill_type_list) > 1:
        sname = sname + '(' + skill_type_list[1] + ')'
      cskill = self.char.d.skills[s]
      iter = model.append()
      model.set(iter,
               self.SCOLUMN_NAME,     sname,
               self.SCOLUMN_DIFF,     skill[SDIFF],
               self.SCOLUMN_POINTS,   str(cskill['points']),
               self.SCOLUMN_LEVEL,    self.char.get_skill(s),
               self.SCOLUMN_ID,       s,
               self.SCOLUMN_EDITABLE, TRUE)
 
      
  def add_adv(self,adv_id):
    ''' Adds an Advantage to the character. This should probably ask for
    level, and/or type'''
    if self.char.has_advantage(adv_id):
      return
    self.char.add_advantage(adv_id,1)
    self.recalculate_skills()
    self.reprint_advantages()
    self.update_totals()

  def redraw_character(self):
    self.recalculate_skills()
    self.reprint_advantages()
    self.redraw_attr()
    self.update_totals()
    self.cnamelabel.set_text(str(self.char.get_character_name()))
    self.pnamelabel.set_text(str(self.char.get_player_name()))
    #self.update_stats()  # done by update totals
      
  def reprint_advantages(self):
    model = self.advantage_table_tv.get_model()
    model.clear()
    parent_iter = model.append(None)
    model.set(parent_iter,
             self.ACOLUMN_POINTS,   self.char.advantage_points(),
             self.ACOLUMN_NAME,     "Advantages",
             self.ACOLUMN_LVL,      "",
             self.ACOLUMN_ID,       "",
             self.ACOLUMN_EDITABLE, False)
    for a in self.char.sorted_advantage_keys():
      adv  = self.advantage_db.db[a]
      cadv = self.char.d.advantages[a]
      iter = model.insert_before(parent_iter,None)
      model.set(iter,
               self.ACOLUMN_POINTS,   cadv['points'],
               self.ACOLUMN_NAME,     adv[ANAME],
	       self.ACOLUMN_LVL,      str(cadv['level']),
               self.ACOLUMN_ID,       a,
	       self.ACOLUMN_EDITABLE, TRUE)
    parent_iter = model.append(None)
    model.set(parent_iter,
             self.ACOLUMN_POINTS,   self.char.quirk_points(),
             self.ACOLUMN_NAME,     "Quirks",
             self.ACOLUMN_LVL,      "",
             self.ACOLUMN_ID,       "",
             self.ACOLUMN_EDITABLE, False)
    for q in self.char.sorted_quirk_keys():
      iter = model.insert_before(parent_iter,None)
      model.set(iter,
               self.ACOLUMN_POINTS,   -1,
               self.ACOLUMN_NAME,     q,
	       self.ACOLUMN_LVL,      "",
               self.ACOLUMN_ID,       'quirk',
	       self.ACOLUMN_EDITABLE, FALSE)
    self.advantage_table_tv.expand_all()
 
      
  def save_character_file(self, char_file_name):
    self.filename = char_file_name 
    char_file=open(char_file_name,'w')
    self.char.pre_save()
    pickle.dump(self.char.d,char_file)

  def load_character_file(self, char_file_name):
    self.filename = char_file_name 
    char_file=open(char_file_name,'r')
    self.char.d = pickle.load(char_file)
    self.char.post_load()
    self.redraw_character()

  def load_character(self,w):
    self.filew.hide()
    self.load_character_file(self.filew.get_filename())

  def save_character(self,w):
    self.filew.hide()
    self.save_character_file(self.filew.get_filename())

  def load_character_cb(self, window, action, widget):
    self.filew = gtk.FileSelection("Load Character")
    self.filew.connect("destroy", 
                       lambda w: self.filew.hide())
    self.filew.ok_button.connect("clicked", self.load_character)
    self.filew.cancel_button.connect("clicked",
                                     lambda w: self.filew.destroy())
    self.filew.set_filename("character.gc")
    self.filew.show()

  def save_character_cb(self, window, action, widget):
    if self.filename == '':
      self.save_character_as_cb(window, action, widget)
    else:
      self.save_character_file(self.filename)

  def save_character_as_cb(self, window, action, widget):
    self.filew = gtk.FileSelection("Save Character")
    self.filew.connect("destroy", 
                       lambda w: self.filew.hide())
    self.filew.ok_button.connect("clicked", self.save_character)
    self.filew.cancel_button.connect("clicked",
                                     lambda w: self.filew.destroy())
    self.filew.set_filename("character.gc")
    self.filew.show()

  def print_cb(self, window, action, widget):
    self.filew = gtk.FileSelection("Print character to file")
    self.filew.connect("destroy", 
                       lambda w: self.filew.hide())
    self.filew.ok_button.connect("clicked", self.print_character_to_file)
    self.filew.cancel_button.connect("clicked",
                                     lambda w: self.filew.destroy())
    self.filew.set_filename("character")
    self.filew.show()
  
  def print_character_to_file(self,w):
    self.filew.hide()
    self.char.print_to_file(self.filew.get_filename())


if __name__ == '__main__':
  fgccp_App = Fgccp_App()
  fgccp_App.run()
