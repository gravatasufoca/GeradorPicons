# -*- coding: utf-8 -*-
from Components.ActionMap import ActionMap
from Components.Language import language
from Components.PluginComponent import plugins
from Components.Sources.StaticText import StaticText
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from Tools.Directories import resolveFilename, SCOPE_PLUGINS, SCOPE_SKIN_IMAGE
from Tools.LoadPixmap import LoadPixmap
from enigma import eServiceCenter

import utils
from Picon import Picon
from PiconList import *
from ProgressoGerador import ProgressoGeradorScreen


def languageChanged():
	plugins.clearPluginList()
	plugins.readPluginList(resolveFilename(SCOPE_PLUGINS))


class DuvidasPiconScreen(Screen):
	skin="""
	  <screen name="DuvidasPicon" position="fill" flags="wfNoBorder">
	    <panel name="PigTemplate"/>
	    <panel name="ButtonTemplate_RGS"/>
	    <eLabel text="Plugin browser" position="85,30" size="1085,55" backgroundColor="secondBG" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="left" />
	    <widget name="list" position="590,110" size="630,500" font="Regular;26" scrollbarMode="showOnDemand" selectionPixmap="PLi-HD/buttons/sel.png" />
  </screen>
	"""
	def __init__(self, session,zipFile, gerados={},duvidas={}):
		Screen.__init__(self, session)
		# self.skinName = [ "PluginBrowser" ]

		self.zipFile=zipFile
		self.skin=DuvidasPiconScreen.skin

		self.onLayoutFinish.append(self.updateList)

		self.onFirstExecBegin.append(self.mostraMensagem)

		self["Title"].text=utils._title+" - "+utils._developer

		self.list = []
		self["list"] = PluginList(self.list)
		self.duvidasList = {}
		self.expanded = []

		self["key_red"] = StaticText(_("Cancelar"))
		self["key_green"] = StaticText(_("Salvar"))

		self["actions"] = ActionMap(["OkCancelActions","InputActions","ColorActions", "setupActions"],
        {
            "green": self.enviar,
            "cancel": self.close,
            "ok":self.selecionar,
	        "back": self.close,

        }, -2)
		self.gerados=gerados
		self.prepareList(duvidas)
		utils.addScreen(self)


	def mostraMensagem(self):
		msg="Foram encontrado(s) %d picons!\nPorém eu fiquei em dúvida em alguns.\nVocê pode escolher na lista os que combinam com cada canal."%(len(self.gerados))
		self.session.open(MessageBox, text = msg, type = MessageBox.TYPE_WARNING,close_on_any_key=True, timeout=5)


	def enviar(self):
		for canal in self.duvidasList.keys():
			picon= filter(lambda p: p.selected,self.duvidasList[canal])
			if len(picon)>0:
				self.gerados[canal]=picon[0]

		self.session.open(ProgressoGeradorScreen,zipFile=self.zipFile,gerados=self.gerados)




	def selecionar(self):
		piconSelecionado = self["list"].l.getCurrentSelection()

		if piconSelecionado is None:
			return
		piconSelecionado = piconSelecionado[0]
		if isinstance(piconSelecionado, Picon):
			check=not piconSelecionado.selected

			for picon in self.getCategory(piconSelecionado.categoria):
				picon.selected=False

			piconSelecionado.selected=check

			self.updateList()


	def updateList(self):

		list = []
		expandableIcon = LoadPixmap(resolveFilename(SCOPE_SKIN_IMAGE, "skin_default/expandable-plugins.png"))
		expandedIcon = LoadPixmap(resolveFilename(SCOPE_SKIN_IMAGE, "skin_default/expanded-plugins.png"))
		verticallineIcon = LoadPixmap(resolveFilename(SCOPE_SKIN_IMAGE, "skin_default/verticalline-plugins.png"))

		listsize = self["list"].instance.size()
		self.listWidth = listsize.width()
		self.listHeight = listsize.height()


		for x in self.duvidasList.keys():
			list.append(PluginCategoryComponent(self.getNome(x), expandedIcon, self.listWidth))
			list.extend([PluginDownloadComponent(picon, self.listWidth) for picon in self.duvidasList[x]])

		self.list = list
		self["list"].l.setList(list)

	def prepareList(self,lista={}):
		for canal in lista.keys():
			self.addIntoCategory(canal,[picon for picon in lista[canal]])


	def getNome(self,canal):
		servicehandler = eServiceCenter.getInstance()
		return servicehandler.info(canal).getName(canal)


	def addCategory(self,categoria):
		if not self.duvidasList.has_key(categoria):
			self.duvidasList[categoria]=[]


	def getCategory(self,categoria):
		self.addCategory(categoria)
		return self.duvidasList[categoria]

	def addIntoCategory(self,categoria,item):
		self.getCategory(categoria).extend([Picon(categoria,picon,self.zipFile,duvida=True) for picon in item])



language.addCallback(languageChanged)