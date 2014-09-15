import wx
import wx.grid
import wx.aui
import images
import settings_pannel
import cStringIO
import wx.lib.agw.ribbon as Ribbon
import resources

# --------------------------------------------------- #
# Some constants for ribbon buttons
ID_CIRCLE = wx.ID_HIGHEST + 1
ID_CROSS = ID_CIRCLE + 1
ID_TRIANGLE = ID_CIRCLE + 2
ID_SQUARE = ID_CIRCLE + 3
ID_POLYGON = ID_CIRCLE + 4
ID_SELECTION_EXPAND_H = ID_CIRCLE + 5
ID_SELECTION_EXPAND_V = ID_CIRCLE + 6
ID_SELECTION_CONTRACT = ID_CIRCLE + 7
ID_PRIMARY_COLOUR = ID_CIRCLE + 8
ID_SECONDARY_COLOUR = ID_CIRCLE + 9
ID_DEFAULT_PROVIDER = ID_CIRCLE + 10
ID_AUI_PROVIDER = ID_CIRCLE + 11
ID_MSW_PROVIDER = ID_CIRCLE + 12
ID_MAIN_TOOLBAR = ID_CIRCLE + 13
ID_POSITION_TOP = ID_CIRCLE + 14
ID_POSITION_TOP_ICONS = ID_CIRCLE + 15
ID_POSITION_TOP_BOTH = ID_CIRCLE + 16
ID_POSITION_LEFT = ID_CIRCLE + 17
ID_POSITION_LEFT_LABELS = ID_CIRCLE + 18
ID_POSITION_LEFT_BOTH = ID_CIRCLE + 19
ID_TOGGLE_PANELS = ID_CIRCLE + 20

align_center = resources.align_center
align_left = resources.align_left
align_right = resources.align_right
aui_style = resources.aui_style
auto_crop_selection = resources.auto_crop_selection
auto_crop_selection_small = resources.auto_crop_selection_small
circle = resources.circle
circle_small = resources.circle_small
colours = resources.colours
cross = resources.cross
empty = resources.empty
expand_selection_h = resources.expand_selection_h
expand_selection_v = resources.expand_selection_v
eye = resources.eye
hexagon = resources.hexagon
msw_style = resources.msw_style
position_left = resources.position_left
position_top = resources.position_top
ribbon = resources.ribbon
powerPanel = resources.powerPanel
square = resources.square
triangle = resources.triangle
icon_power = resources.power
icon_tune = resources.tune
icon_seek_prev = resources.seek_prev
icon_seek_next = resources.seek_next
icon_scan = resources.scan
icon_intro_scan = resources.intro_scan
icon_cancel = resources.cancel
icon_reload_ensemble = resources.reload_ensemble

ID_BT_POW = wx.ID_HIGHEST+100
ID_BT_TUNE = wx.ID_HIGHEST+101
ID_BT_SEEK_PREV = wx.ID_HIGHEST+102
ID_BT_SEEK_NEXT = wx.ID_HIGHEST+103
ID_BT_SCAN = wx.ID_HIGHEST+104
ID_BT_INTRO_SCAN = wx.ID_HIGHEST+105
ID_BT_CANCEL = wx.ID_HIGHEST+106
ID_BT_RELOAD_ENS = wx.ID_HIGHEST+107
# --------------------------------------------------- #

def CreateBitmap(xpm):
	bmp = eval(xpm).Bitmap
	return bmp


# --------------------------------------------------- #


class ColourClientData(object):

	def __init__(self, name, colour):
		self._name = name
		self._colour = colour


	def GetName(self):
		return self._name


	def GetColour(self):
		return self._colour
# --------------------------------------------------- #
def GetMondrianData():
	return \
'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00 \x00\x00\x00 \x08\x06\x00\
\x00\x00szz\xf4\x00\x00\x00\x04sBIT\x08\x08\x08\x08|\x08d\x88\x00\x00\x00qID\
ATX\x85\xed\xd6;\n\x800\x10E\xd1{\xc5\x8d\xb9r\x97\x16\x0b\xad$\x8a\x82:\x16\
o\xda\x84pB2\x1f\x81Fa\x8c\x9c\x08\x04Z{\xcf\xa72\xbcv\xfa\xc5\x08 \x80r\x80\
\xfc\xa2\x0e\x1c\xe4\xba\xfaX\x1d\xd0\xde]S\x07\x02\xd8>\xe1wa-`\x9fQ\xe9\
\x86\x01\x04\x10\x00\\(Dk\x1b-\x04\xdc\x1d\x07\x14\x98;\x0bS\x7f\x7f\xf9\x13\
\x04\x10@\xf9X\xbe\x00\xc9 \x14K\xc1<={\x00\x00\x00\x00IEND\xaeB`\x82' 


def GetMondrianBitmap():
    return wx.BitmapFromImage(GetMondrianImage())


def GetMondrianImage():
	stream = cStringIO.StringIO(GetMondrianData())
	return wx.ImageFromStream(stream)


def GetMondrianIcon():
    icon = wx.EmptyIcon()
    icon.CopyFromBitmap(GetMondrianBitmap())
    return icon

class TcFrame(wx.Frame):
	def __init__(self, parent, id=-1, title="", pos=wx.DefaultPosition,
		size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE|wx.SUNKEN_BORDER|wx.CLIP_CHILDREN
		):
		super(TcFrame, self).__init__(parent, id, title, pos, size, style)

		panel = wx.Panel(self)

		# tell FrameManager to manage this frame
		self._mgr = wx.aui.AuiManager()
		self._mgr.SetManagedWindow(self)
		self._perspectives = []
		self.n = 0
		self.x = 0

		self.SetIcon(GetMondrianIcon())

		#create ribbon bar
		self._ribbon = Ribbon.RibbonBar(panel, wx.ID_ANY,
			agwStyle=Ribbon.RIBBON_BAR_DEFAULT_STYLE|Ribbon.RIBBON_BAR_SHOW_PANEL_EXT_BUTTONS)
		self._bitmap_creation_dc = wx.MemoryDC()
		self._colour_data = wx.ColourData()
		home = Ribbon.RibbonPage(self._ribbon, wx.ID_ANY, "DAB")

		powerPanel = Ribbon.RibbonPanel(home, wx.ID_ANY, "Power")
		powerBar = Ribbon.RibbonButtonBar(powerPanel)
		powerBar.AddSimpleButton(ID_BT_POW, "On/Off", CreateBitmap("icon_power"),
			"Reset application setting")

		dabPanel = Ribbon.RibbonPanel(home, wx.ID_ANY, "DAB")
		dabBar = Ribbon.RibbonButtonBar(dabPanel)
		dabBar.AddSimpleButton(ID_BT_TUNE, "Tune", CreateBitmap("icon_tune"), 
			"Tune the frequency")
		dabBar.AddSimpleButton(ID_BT_SEEK_PREV, "Seek Prev", CreateBitmap("icon_seek_prev"),
			"Seek previous service component")
		dabBar.AddSimpleButton(ID_BT_SEEK_NEXT, "Seek Next", CreateBitmap("icon_seek_next"), 
			"Seek next service component")

		label_font = wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_LIGHT)
		self._bitmap_creation_dc.SetFont(label_font)

		scheme = Ribbon.RibbonPage(self._ribbon, wx.ID_ANY, "UI")
		self._default_primary, self._default_secondary, self._default_tertiary = self._ribbon.GetArtProvider().GetColourScheme(1, 1, 1)

		provider_panel = Ribbon.RibbonPanel(scheme, wx.ID_ANY, "Art", wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize,
			agwStyle=Ribbon.RIBBON_PANEL_NO_AUTO_MINIMISE)
		provider_bar = Ribbon.RibbonButtonBar(provider_panel, wx.ID_ANY)
		provider_bar.AddSimpleButton(ID_DEFAULT_PROVIDER, "Default Provider",
		wx.ArtProvider.GetBitmap(wx.ART_QUESTION, wx.ART_OTHER, wx.Size(32, 32)), "")
		provider_bar.AddSimpleButton(ID_AUI_PROVIDER, "AUI Provider", CreateBitmap("aui_style"), "")
		provider_bar.AddSimpleButton(ID_MSW_PROVIDER, "MSW Provider", CreateBitmap("msw_style"), "")

		primary_panel = Ribbon.RibbonPanel(scheme, wx.ID_ANY, "Primary Colour", CreateBitmap("colours"))
		self._primary_gallery = self.PopulateColoursPanel(primary_panel, self._default_primary, ID_PRIMARY_COLOUR)

		secondary_panel = Ribbon.RibbonPanel(scheme, wx.ID_ANY, "Secondary Colour", CreateBitmap("colours"))
		self._secondary_gallery = self.PopulateColoursPanel(secondary_panel, self._default_secondary, ID_SECONDARY_COLOUR)

		self._ribbon.Realize()

		self._logwindow = wx.TextCtrl(panel, wx.ID_ANY, "", wx.DefaultPosition, wx.DefaultSize,
		wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_LEFT | wx.TE_BESTWRAP | wx.BORDER_NONE)

		s = wx.BoxSizer(wx.VERTICAL)

		s.Add(self._ribbon, 0, wx.EXPAND)
		s.Add(self._logwindow, 1, wx.EXPAND)

		panel.SetSizer(s)
		self.panel = panel

		self.BindEvents([powerBar, dabBar, provider_bar])

		self.SetIcon(GetMondrianIcon())
		self.CenterOnScreen()
		self.Show()

	def BindEvents(self, bars):
		powerBar, dabBar, provider_bar = bars

		provider_bar.Bind(Ribbon.EVT_RIBBONBUTTONBAR_CLICKED, self.OnDefaultProvider, id=ID_DEFAULT_PROVIDER)
		provider_bar.Bind(Ribbon.EVT_RIBBONBUTTONBAR_CLICKED, self.OnAUIProvider, id=ID_AUI_PROVIDER)
		provider_bar.Bind(Ribbon.EVT_RIBBONBUTTONBAR_CLICKED, self.OnMSWProvider, id=ID_MSW_PROVIDER)
		powerBar.Bind(Ribbon.EVT_RIBBONBUTTONBAR_CLICKED, self.OnSelectionExpandHButton, id=ID_SELECTION_EXPAND_H)
		powerBar.Bind(Ribbon.EVT_RIBBONBUTTONBAR_CLICKED, self.OnSelectionExpandVButton, id=ID_SELECTION_EXPAND_V)
		powerBar.Bind(Ribbon.EVT_RIBBONBUTTONBAR_CLICKED, self.OnSelectionContractButton, id=ID_SELECTION_CONTRACT)
		dabBar.Bind(Ribbon.EVT_RIBBONBUTTONBAR_CLICKED, self.OnCircleButton, id=ID_CIRCLE)
		dabBar.Bind(Ribbon.EVT_RIBBONBUTTONBAR_CLICKED, self.OnCrossButton, id=ID_CROSS)
		dabBar.Bind(Ribbon.EVT_RIBBONBUTTONBAR_CLICKED, self.OnTriangleButton, id=ID_TRIANGLE)
		dabBar.Bind(Ribbon.EVT_RIBBONBUTTONBAR_CLICKED, self.OnSquareButton, id=ID_SQUARE)
		dabBar.Bind(Ribbon.EVT_RIBBONBUTTONBAR_DROPDOWN_CLICKED, self.OnTriangleDropdown, id=ID_TRIANGLE)
		dabBar.Bind(Ribbon.EVT_RIBBONBUTTONBAR_DROPDOWN_CLICKED, self.OnPolygonDropdown, id=ID_POLYGON)

		self.Bind(Ribbon.EVT_RIBBONGALLERY_HOVER_CHANGED, self.OnHoveredColourChange, id=ID_PRIMARY_COLOUR)
		self.Bind(Ribbon.EVT_RIBBONGALLERY_HOVER_CHANGED, self.OnHoveredColourChange, id=ID_SECONDARY_COLOUR)
		self.Bind(Ribbon.EVT_RIBBONGALLERY_SELECTED, self.OnPrimaryColourSelect, id=ID_PRIMARY_COLOUR)
		self.Bind(Ribbon.EVT_RIBBONGALLERY_SELECTED, self.OnSecondaryColourSelect, id=ID_SECONDARY_COLOUR)
		self.Bind(Ribbon.EVT_RIBBONTOOLBAR_CLICKED, self.OnNew, id=wx.ID_NEW)
		self.Bind(Ribbon.EVT_RIBBONTOOLBAR_DROPDOWN_CLICKED, self.OnNewDropdown, id=wx.ID_NEW)
		self.Bind(Ribbon.EVT_RIBBONTOOLBAR_CLICKED, self.OnPrint, id=wx.ID_PRINT)
		self.Bind(Ribbon.EVT_RIBBONTOOLBAR_DROPDOWN_CLICKED, self.OnPrintDropdown, id=wx.ID_PRINT)
		self.Bind(Ribbon.EVT_RIBBONTOOLBAR_DROPDOWN_CLICKED, self.OnRedoDropdown, id=wx.ID_REDO)
		self.Bind(Ribbon.EVT_RIBBONTOOLBAR_DROPDOWN_CLICKED, self.OnUndoDropdown, id=wx.ID_UNDO)
		self.Bind(Ribbon.EVT_RIBBONTOOLBAR_CLICKED, self.OnPositionLeft, id=ID_POSITION_LEFT)
		self.Bind(Ribbon.EVT_RIBBONTOOLBAR_DROPDOWN_CLICKED, self.OnPositionLeftDropdown, id=ID_POSITION_LEFT)
		self.Bind(Ribbon.EVT_RIBBONTOOLBAR_CLICKED, self.OnPositionTop, id=ID_POSITION_TOP)
		self.Bind(Ribbon.EVT_RIBBONTOOLBAR_DROPDOWN_CLICKED, self.OnPositionTopDropdown, id=ID_POSITION_TOP)
		self.Bind(wx.EVT_BUTTON, self.OnColourGalleryButton, id=ID_PRIMARY_COLOUR)
		self.Bind(wx.EVT_BUTTON, self.OnColourGalleryButton, id=ID_SECONDARY_COLOUR)
		self.Bind(wx.EVT_MENU, self.OnPositionLeftIcons, id=ID_POSITION_LEFT)
		self.Bind(wx.EVT_MENU, self.OnPositionLeftLabels, id=ID_POSITION_LEFT_LABELS)
		self.Bind(wx.EVT_MENU, self.OnPositionLeftBoth, id=ID_POSITION_LEFT_BOTH)
		self.Bind(wx.EVT_MENU, self.OnPositionTopLabels, id=ID_POSITION_TOP)
		self.Bind(wx.EVT_MENU, self.OnPositionTopIcons, id=ID_POSITION_TOP_ICONS)
		self.Bind(wx.EVT_MENU, self.OnPositionTopBoth, id=ID_POSITION_TOP_BOTH)


	def SetBarStyle(self, agwStyle):
		self._ribbon.Freeze()
		self._ribbon.SetAGWWindowStyleFlag(agwStyle)

		pTopSize = self.panel.GetSizer()
		pToolbar = wx.FindWindowById(ID_MAIN_TOOLBAR)

		if agwStyle & Ribbon.RIBBON_BAR_FLOW_VERTICAL:
			self._ribbon.SetTabCtrlMargins(10, 10)
			pTopSize.SetOrientation(wx.HORIZONTAL)
			if pToolbar:
				pToolbar.SetRows(3, 5)

		else:
			self._ribbon.SetTabCtrlMargins(50, 20)
			pTopSize.SetOrientation(wx.VERTICAL)
			if pToolbar:
				pToolbar.SetRows(2, 3)

		self._ribbon.Realize()
		self._ribbon.Thaw()
		self.panel.Layout()


	def PopulateColoursPanel(self, panel, defc, gallery_id):
		gallery = wx.FindWindowById(gallery_id, panel)

		if gallery:
			gallery.Clear()
		else:
			gallery = Ribbon.RibbonGallery(panel, gallery_id)

		dc = self._bitmap_creation_dc
		def_item = self.AddColourToGallery(gallery, "Default", dc, defc)
		gallery.SetSelection(def_item)

		self.AddColourToGallery(gallery, "BLUE", dc)
		self.AddColourToGallery(gallery, "BLUE VIOLET", dc)
		self.AddColourToGallery(gallery, "BROWN", dc)
		self.AddColourToGallery(gallery, "CADET BLUE", dc)
		self.AddColourToGallery(gallery, "CORAL", dc)
		self.AddColourToGallery(gallery, "CYAN", dc)
		self.AddColourToGallery(gallery, "DARK GREEN", dc)
		self.AddColourToGallery(gallery, "DARK ORCHID", dc)
		self.AddColourToGallery(gallery, "FIREBRICK", dc)
		self.AddColourToGallery(gallery, "GOLD", dc)
		self.AddColourToGallery(gallery, "GOLDENROD", dc)
		self.AddColourToGallery(gallery, "GREEN", dc)
		self.AddColourToGallery(gallery, "INDIAN RED", dc)
		self.AddColourToGallery(gallery, "KHAKI", dc)
		self.AddColourToGallery(gallery, "LIGHT BLUE", dc)
		self.AddColourToGallery(gallery, "LIME GREEN", dc)
		self.AddColourToGallery(gallery, "MAGENTA", dc)
		self.AddColourToGallery(gallery, "MAROON", dc)
		self.AddColourToGallery(gallery, "NAVY", dc)
		self.AddColourToGallery(gallery, "ORANGE", dc)
		self.AddColourToGallery(gallery, "ORCHID", dc)
		self.AddColourToGallery(gallery, "PINK", dc)
		self.AddColourToGallery(gallery, "PLUM", dc)
		self.AddColourToGallery(gallery, "PURPLE", dc)
		self.AddColourToGallery(gallery, "RED", dc)
		self.AddColourToGallery(gallery, "SALMON", dc)
		self.AddColourToGallery(gallery, "SEA GREEN", dc)
		self.AddColourToGallery(gallery, "SIENNA", dc)
		self.AddColourToGallery(gallery, "SKY BLUE", dc)
		self.AddColourToGallery(gallery, "TAN", dc)
		self.AddColourToGallery(gallery, "THISTLE", dc)
		self.AddColourToGallery(gallery, "TURQUOISE", dc)
		self.AddColourToGallery(gallery, "VIOLET", dc)
		self.AddColourToGallery(gallery, "VIOLET RED", dc)
		self.AddColourToGallery(gallery, "WHEAT", dc)
		self.AddColourToGallery(gallery, "WHITE", dc)
		self.AddColourToGallery(gallery, "YELLOW", dc)

		return gallery


	def GetGalleryColour(self, gallery, item, name=None):
		data = gallery.GetItemClientData(item)

		if name != None:
			name = data.GetName()

		return data.GetColour(), name


	def OnHoveredColourChange(self, event):

		# Set the background of the gallery to the hovered colour, or back to the
		# default if there is no longer a hovered item.

		gallery = event.GetGallery()
		provider = gallery.GetArtProvider()

		if event.GetGalleryItem() != None:        
			if provider == self._ribbon.GetArtProvider():
				provider = provider.Clone()
				gallery.SetArtProvider(provider)

			provider.SetColour(Ribbon.RIBBON_ART_GALLERY_HOVER_BACKGROUND_COLOUR,
				self.GetGalleryColour(event.GetGallery(), event.GetGalleryItem(), None)[0])

		else:        
			if provider != self._ribbon.GetArtProvider():            
				gallery.SetArtProvider(self._ribbon.GetArtProvider())
				del provider


	def OnPrimaryColourSelect(self, event):
		colour, name = self.GetGalleryColour(event.GetGallery(), event.GetGalleryItem(), "")
		self.AddText("Colour %s selected as primary."%name)

		dummy, secondary, tertiary = self._ribbon.GetArtProvider().GetColourScheme(None, 1, 1)
		self._ribbon.GetArtProvider().SetColourScheme(colour, secondary, tertiary)
		self.ResetGalleryArtProviders()
		self._ribbon.Refresh()


	def OnSecondaryColourSelect(self, event):
		colour, name = self.GetGalleryColour(event.GetGallery(), event.GetGalleryItem(), "")
		self.AddText("Colour %s selected as secondary."%name)

		primary, dummy, tertiary = self._ribbon.GetArtProvider().GetColourScheme(1, None, 1)
		self._ribbon.GetArtProvider().SetColourScheme(primary, colour, tertiary)
		self.ResetGalleryArtProviders()
		self._ribbon.Refresh()


	def ResetGalleryArtProviders(self):
		if self._primary_gallery.GetArtProvider() != self._ribbon.GetArtProvider():
			self._primary_gallery.SetArtProvider(self._ribbon.GetArtProvider())

		if self._secondary_gallery.GetArtProvider() != self._ribbon.GetArtProvider():        
			self._secondary_gallery.SetArtProvider(self._ribbon.GetArtProvider())


	def OnSelectionExpandHButton(self, event):

		self.AddText("Expand powerBar horizontally button clicked.")


	def OnSelectionExpandVButton(self, event):

		self.AddText("Expand powerBar vertically button clicked.")


	def OnSelectionContractButton(self, event):

		self.AddText("Contract powerBar button clicked.")


	def OnCircleButton(self, event):

		self.AddText("Circle button clicked.")


	def OnCrossButton(self, event):

		self.AddText("Cross button clicked.")


	def OnTriangleButton(self, event):

		self.AddText("Triangle button clicked.")


	def OnTriangleDropdown(self, event):

		menu = wx.Menu()
		menu.Append(wx.ID_ANY, "Equilateral")
		menu.Append(wx.ID_ANY, "Isosceles")
		menu.Append(wx.ID_ANY, "Scalene")

		event.PopupMenu(menu)


	def OnSquareButton(self, event):

		self.AddText("Square button clicked.")


	def OnPolygonDropdown(self, event):

		menu = wx.Menu()
		menu.Append(wx.ID_ANY, "Pentagon (5 sided)")
		menu.Append(wx.ID_ANY, "Hexagon (6 sided)")
		menu.Append(wx.ID_ANY, "Heptagon (7 sided)")
		menu.Append(wx.ID_ANY, "Octogon (8 sided)")
		menu.Append(wx.ID_ANY, "Nonagon (9 sided)")
		menu.Append(wx.ID_ANY, "Decagon (10 sided)")

		event.PopupMenu(menu)


	def OnNew(self, event):

		self.AddText("New button clicked.")


	def OnNewDropdown(self, event):

		menu = wx.Menu()
		menu.Append(wx.ID_ANY, "New Document")
		menu.Append(wx.ID_ANY, "New Template")
		menu.Append(wx.ID_ANY, "New Mail")

		event.PopupMenu(menu)


	def OnPrint(self, event):

		self.AddText("Print button clicked.")


	def OnPrintDropdown(self, event):

		menu = wx.Menu()
		menu.Append(wx.ID_ANY, "Print")
		menu.Append(wx.ID_ANY, "Preview")
		menu.Append(wx.ID_ANY, "Options")

		event.PopupMenu(menu)


	def OnRedoDropdown(self, event):

		menu = wx.Menu()
		menu.Append(wx.ID_ANY, "Redo E")
		menu.Append(wx.ID_ANY, "Redo F")
		menu.Append(wx.ID_ANY, "Redo G")

		event.PopupMenu(menu)


	def OnUndoDropdown(self, event):

		menu = wx.Menu()
		menu.Append(wx.ID_ANY, "Undo C")
		menu.Append(wx.ID_ANY, "Undo B")
		menu.Append(wx.ID_ANY, "Undo A")

		event.PopupMenu(menu)


	def OnPositionTopLabels(self, event):

		self.SetBarStyle(Ribbon.RIBBON_BAR_DEFAULT_STYLE)


	def OnPositionTopIcons(self, event):

		self.SetBarStyle((Ribbon.RIBBON_BAR_DEFAULT_STYLE &~Ribbon.RIBBON_BAR_SHOW_PAGE_LABELS)
			| Ribbon.RIBBON_BAR_SHOW_PAGE_ICONS)


	def OnPositionTopBoth(self, event):

		self.SetBarStyle(Ribbon.RIBBON_BAR_DEFAULT_STYLE | Ribbon.RIBBON_BAR_SHOW_PAGE_ICONS)


	def OnPositionLeftLabels(self, event):

		self.SetBarStyle(Ribbon.RIBBON_BAR_DEFAULT_STYLE | Ribbon.RIBBON_BAR_FLOW_VERTICAL)


	def OnPositionLeftIcons(self, event):

		self.SetBarStyle((Ribbon.RIBBON_BAR_DEFAULT_STYLE &~Ribbon.RIBBON_BAR_SHOW_PAGE_LABELS) |
			Ribbon.RIBBON_BAR_SHOW_PAGE_ICONS | Ribbon.RIBBON_BAR_FLOW_VERTICAL)


	def OnPositionLeftBoth(self, event):

		self.SetBarStyle(Ribbon.RIBBON_BAR_DEFAULT_STYLE | Ribbon.RIBBON_BAR_SHOW_PAGE_ICONS |
			Ribbon.RIBBON_BAR_FLOW_VERTICAL)


	def OnPositionTop(self, event):

		self.OnPositionTopLabels(event)


	def OnPositionTopDropdown(self, event):

		menu = wx.Menu()
		menu.Append(ID_POSITION_TOP, "Top with Labels")
		menu.Append(ID_POSITION_TOP_ICONS, "Top with Icons")
		menu.Append(ID_POSITION_TOP_BOTH, "Top with Both")
		event.PopupMenu(menu)


	def OnPositionLeft(self, event):

		self.OnPositionLeftIcons(event)


	def OnPositionLeftDropdown(self, event):

		menu = wx.Menu()
		menu.Append(ID_POSITION_LEFT, "Left with Icons")
		menu.Append(ID_POSITION_LEFT_LABELS, "Left with Labels")
		menu.Append(ID_POSITION_LEFT_BOTH, "Left with Both")
		event.PopupMenu(menu)


	def OnTogglePanels(self, event):
		pass


	def OnExtButton(self, event):

		wx.MessageBox("Extended button activated")


	def AddText(self, msg):

		self._logwindow.AppendText(msg)
		self._logwindow.AppendText("\n")
		self._ribbon.DismissExpandedPanel()


	def AddColourToGallery(self, gallery, colour, dc, value=None):

		item = None

		if colour != "Default":
			c = wx.NamedColour(colour)

		if value is not None:
			c = value

		if c.IsOk():

			iWidth = 64
			iHeight = 40

			bitmap = wx.EmptyBitmap(iWidth, iHeight)
			dc.SelectObject(bitmap)
			b = wx.Brush(c)
			dc.SetPen(wx.BLACK_PEN)
			dc.SetBrush(b)
			dc.DrawRectangle(0, 0, iWidth, iHeight)

			colour = colour[0] + colour[1:].lower()
			size = wx.Size(*dc.GetTextExtent(colour))
			notcred = min(abs(~c.Red()), 255)
			notcgreen = min(abs(~c.Green()), 255)
			notcblue = min(abs(~c.Blue()), 255)

			foreground = wx.Colour(notcred, notcgreen, notcblue)

			if abs(foreground.Red() - c.Red()) + abs(foreground.Blue() - c.Blue()) + abs(foreground.Green() - c.Green()) < 64:
				# Foreground too similar to background - use a different
				# strategy to find a contrasting colour
				foreground = wx.Colour((c.Red() + 64) % 256, 255 - c.Green(),
					(c.Blue() + 192) % 256)

			dc.SetTextForeground(foreground)
			dc.DrawText(colour, (iWidth - size.GetWidth() + 1) / 2, (iHeight - size.GetHeight()) / 2)
			dc.SelectObjectAsSource(wx.NullBitmap)

			item = gallery.Append(bitmap, wx.ID_ANY)
			gallery.SetItemClientData(item, ColourClientData(colour, c))

		return item


	def OnColourGalleryButton(self, event):
		gallery = event.GetEventObject()
		if gallery is None:
			return

		self._ribbon.DismissExpandedPanel()
		if gallery.GetSelection():
			self._colour_data.SetColour(self.GetGalleryColour(gallery, gallery.GetSelection(), None)[0])

		dlg = wx.ColourDialog(self, self._colour_data)

		if dlg.ShowModal() == wx.ID_OK:

			self._colour_data = dlg.GetColourData()
			clr = self._colour_data.GetColour()

			# Try to find colour in gallery
			item = None
			for i in xrange(gallery.GetCount()):
				item = gallery.GetItem(i)
				if self.GetGalleryColour(gallery, item, None)[0] == clr:
					break
				else:
					item = None

			# Colour not in gallery - add it
			if item == None:            
				item = self.AddColourToGallery(gallery, clr.GetAsString(wx.C2S_HTML_SYNTAX), 
					self._bitmap_creation_dc, clr)
				gallery.Realize()

			# Set powerBar
			gallery.EnsureVisible(item)
			gallery.SetSelection(item)

			# Send an event to respond to the powerBar change
			dummy = Ribbon.RibbonGalleryEvent(Ribbon.wxEVT_COMMAND_RIBBONGALLERY_SELECTED, gallery.GetId())
			dummy.SetEventObject(gallery)
			dummy.SetGallery(gallery)
			dummy.SetGalleryItem(item)
			self.GetEventHandler().ProcessEvent(dummy)


	def OnDefaultProvider(self, event):
		self._ribbon.DismissExpandedPanel()
		self.SetArtProvider(Ribbon.RibbonDefaultArtProvider())


	def OnAUIProvider(self, event):
		self._ribbon.DismissExpandedPanel()
		self.SetArtProvider(Ribbon.RibbonAUIArtProvider())


	def OnMSWProvider(self, event):
		self._ribbon.DismissExpandedPanel()
		self.SetArtProvider(Ribbon.RibbonMSWArtProvider())


	def SetArtProvider(self, prov):
		self._ribbon.Freeze()
		self._ribbon.SetArtProvider(prov)

		self._default_primary, self._default_secondary, self._default_tertiary = \
		prov.GetColourScheme(self._default_primary, self._default_secondary, self._default_tertiary)
		self.PopulateColoursPanel(self._primary_gallery.GetParent(), self._default_primary,
		ID_PRIMARY_COLOUR)
		self.PopulateColoursPanel(self._secondary_gallery.GetParent(), self._default_secondary,
		ID_SECONDARY_COLOUR)

		self._ribbon.Thaw()
		self.panel.GetSizer().Layout()
		self._ribbon.Realize()

class TcApp(wx.App):
	def OnInit(self):
		self.frame = TcFrame(None, title="Telechips DAB GUI")
		self.SetTopWindow(self.frame)
		self.frame.Show()
		return True

if __name__ == "__main__":
	app = TcApp(False)
	app.MainLoop()
