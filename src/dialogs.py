# -*- coding: utf-8 -*-
import gtk
import ytdown

class About:
	def __init__(self):
		self.name = ytdown.PROGRAM_NAME
		self.version = ytdown.PROGRAM_VERSION
		self.copyright = 'Copyright © 2010 Cristian Ferreyra.'
		self.authors = ['Cristian Ferreyra <snake [@] 8d2media com>', 'Para http://lazonalinux.com.ar']
		self.website = 'http://snake.8d2media.com'
		self.description = 'GUI simple para youtube-dl usando PyGTK'
		self.license = 'This program is free software; you can redistribute it and/or \
modify it under the terms of the GNU General Public License as published by \
the Free Software Foundation; either version 2 of the License, or (at your \
option) any later version. \n\nThis program is distributed in the hope that \
it will be useful, but WITHOUT ANY WARRANTY; without even the implied \
warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. \
See the GNU General Public License for more details. \n\nYou should have \
received a copy of the GNU General Public License along with this program; \
if not, write to the Free Software Foundation, Inc., 51 Franklin Street, \
Fifth Floor, Boston, MA 02110-1301, USA.'

	# Ventana About (conocida como Acerca de).
	def about_info(self, data=None):
		about = gtk.AboutDialog()
		about.set_name(self.name)
		about.set_version(self.version)
		about.set_comments(self.description)
		about.set_copyright(self.copyright)

		def openHomePage(widget,url,url2): # Para abrir el sitio
			import webbrowser
			webbrowser.open_new(url)

		gtk.about_dialog_set_url_hook(openHomePage,self.website)
		about.set_website(self.website)
		about.set_authors(self.authors)
		about.set_license(self.license)
		about.set_wrap_license(True) # Adapta el texto a la ventana
		about.run()
		about.destroy()