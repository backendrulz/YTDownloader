#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ¬¬
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Importamos los modulos necesarios
try:
	import pygtk
	pygtk.require('2.0')
except:
	pass

try:
	import gtk
	import gtk.glade
except:
	print 'You need to install pyGTK or GTKv2 or set your PYTHONPATH correctly'
	print 'debian: sudo apt-get install python-gtk2 python-glade2'
	sys.exit(1)

import dialogs
import threading
import gobject
import pexpect
import re, sys

PROGRAM_NAME = 'YTDownloader'
PROGRAM_VERSION = '0.1'

gtk.gdk.threads_init()

class MainGui:
	def __init__(self):
		b = gtk.Builder()
		b.add_from_file('gui.glade')

		self.ventanaprincipal = b.get_object('window_main')
		self.ventanaprincipal.connect('destroy', gtk.main_quit, None)

		self.f_save_directory = b.get_object('f_save_directory')
		self.f_save_directory.set_current_folder(os.path.expanduser('~/')) # os.path.expandvars('$HOME')
		self.b_download = b.get_object('b_download')
		self.e_youtube_url = b.get_object('e_youtube_url')
		self.p_bar = b.get_object('progressbar')
		self.p_bar.set_fraction(0.0)
		self.p_bar.set_text('0%, en espera.')

		self.format_ids = ['', '38', '37', '22', '45', '35', '34', '43', '18', '17']
		self.format_names = ['Máxima calidad', 'MP4 4k', 'MP4 1080p', 'MP4 720p', 'WebM 720p', 'FLV 480p', 'FLV 360p', 'WebM 480p', 'MP4 Medium', 'Mobile 3GP']

		self.store = gtk.ListStore(gobject.TYPE_STRING)

		for name in self.format_names:
			self.store.append([name])

		self.c_presets = b.get_object('c_presets')
		self.c_presets.set_model(self.store)
		self.c_presets.set_active(0)

		cell = gtk.CellRendererText()
		self.c_presets.pack_start(cell, True)
		self.c_presets.add_attribute(cell, 'text', 0)

		b.connect_signals(self)

		self.started = False

		self.icon = gtk.StatusIcon()
		self.icon.set_from_stock(gtk.STOCK_GO_DOWN)
		self.icon.set_tooltip('Ocultar %s' % PROGRAM_NAME)
		self.icon.connect("activate", self.visibility_handler)

		self.ventanaprincipal.show()

	def visibility_handler(self, obj):
		window = self.ventanaprincipal
	  	visible = window.get_property('visible')

		if visible:
			window.hide()
			self.icon.set_tooltip('Mostrar %s' % PROGRAM_NAME)
		else:
			window.show()
			self.icon.set_tooltip('Ocultar %s' % PROGRAM_NAME)

	def minimize_handler(self, window, event):
	   if event.changed_mask & gtk.gdk.WINDOW_STATE_ICONIFIED:
		  if event.new_window_state & gtk.gdk.WINDOW_STATE_ICONIFIED:
			window.hide()
			self.icon.set_tooltip('Mostrar %s' % PROGRAM_NAME)

	def on_c_presets_changed(self, widget):
		selected = widget.get_active_text()
		print self.format_ids[self.format_names.index(selected)]

	def on_b_about_clicked(self, widget):
		dialogs.About().about_info()

	def on_b_download_clicked(self, widget):
		yt_url = self.e_youtube_url.get_text()
		save_format = self.format_ids[self.format_names.index(self.c_presets.get_active_text())]
		save_directory = self.f_save_directory.get_filename()

		if not yt_url.startswith('http://www.youtube.com/watch?v='):
			self.msgbox('Dirección de video no válida', True)
			return

		self.hilo = threading.Thread(target=self.run_script, args=(yt_url, save_format, save_directory))
		self.hilo.start()

	def on_ventanaprincipal_destroy(self, widget, data=None):
		try:
			self.child.sendline(chr(3))
			print 'CTR+C'
			#~ self.child.kill(pexpect.signal.SIGINT)
			#~ self.child.close(True)
		except:
			pass
			#~ print "Unexpected error:", sys.exc_info()[0]

		gtk.main_quit()

	def run_script(self, url, format, directory):
		if format != '':
			format = '-f %s' % format
		command = 'python ./youtube-dl/youtube-dl.py -c %s -o "%s/%%(title)s-%%(id)s.%%(ext)s" "%s"' % (format, directory, url)

		#~ print command
		#~ return
		if self.started:
			self.b_download.set_label(gtk.STOCK_GO_DOWN)
			self.child.sendline(chr(3))
			self.started = False
			return
		else:
			self.b_download.set_label(gtk.STOCK_STOP)
			self.started = True

		self.set_progress(0, 'Iniciando...por favor espere...')
		self.child = pexpect.spawn(command)

		while 1:
			try:
				self.child.expect('\[download\]')
			except pexpect.EOF:
				error = re.search('ERROR: (.*)', self.child.before)
				if error:
					self.set_progress(0, error.group(0).strip())
					print 'ERROR / STOPPED'
				else:
					print 'ENDED'
					self.set_progress(1, 'Finalizado')
				self.b_download.set_label(gtk.STOCK_GO_DOWN)
				self.started = False
				return
			except:
				return

			text = self.child.before.strip()
			if text != None and text != '':
				try:
					matches = re.search(r'([0-9.]+)%', text)
					perc = float(matches.group(1)) / 100.00
					self.set_progress(perc, text)
				except:
					#~ print "Unexpected error:", sys.exc_info()[0]
					continue

	def set_progress(self, percent, text):
		self.p_bar.set_text('%s' % text)
		self.p_bar.set_fraction(percent)
		return True

	def msgbox(self, msg, is_error = False):
		dialog = gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_INFO if not is_error else gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK, message_format=msg)
		dialog.run()
		dialog.destroy()

if __name__== '__main__':
	try:
		MainGui()
		gtk.main()
	except KeyboardInterrupt:
		pass