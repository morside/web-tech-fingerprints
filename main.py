import threading
import itertools
import urllib.parse
# kivy
import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.graphics import Color, Line
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.clock import Clock
# core
from src.scripts.dvalid import user_source_data_valid
from src.scripts.techcore import tech_core_lookup
from src.scripts.wwodd import formatted_data_dict
from src.scripts.history import *


# load .kv file / style 
kv_file = Builder.load_file("TechnologyLookup.kv")
# usage / str
usage_str = """
usage:
accept only URL links - http://; https://

examples:
http://example.com
https://examples.com
"""
# formatted result data / dict
tech_target_dict = {}


# screen / main activity
class MainActivity(Screen):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)


	def button_usage_trigger(self):
		screen_manager            = self.manager
		screen_manager.current    = "usage_activity"
		self.ids.source_data.text = ""


	def button_trigger(self):
		screen_manager   = self.manager
		user_source_data = self.ids.source_data.text
		screen_manager.get_screen("load_activity").user_source_data = user_source_data
		screen_manager.current    = "load_activity"
		self.ids.source_data.text = ""


	def button_history_trigger(self):
		screen_manager            = self.manager
		screen_manager.current    = "history_activity"
		self.ids.source_data.text = ""


# screen / error activity
class ErrorActivity(Screen):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)


	def button_trigger(self):
		screen_manager         = self.manager
		screen_manager.current = "main_activity"


# screen / usage activity
class UsageActivity(Screen):
	# user usage inf / out
	usage_label = StringProperty(usage_str)


	def __init__(self, **kwargs):
		super().__init__(**kwargs)


	def button_trigger(self):
		screen_manager         = self.manager
		screen_manager.current = "main_activity"


# screen / load activity
class LoadActivity(Screen):
	user_source_data = StringProperty()
	load_label       = StringProperty()


	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.load_label = "LOADING"
		self.dots       = itertools.cycle((".", "..", "..."))


	def load_animation(self, load):
		self.load_label = "LOADING" + next(self.dots)

		
	def on_enter(self):
		super().on_enter()
		Clock.schedule_interval(self.load_animation, 1)
		threading.Thread(target=self.source_data_valid).start()


	def source_data_valid(self):
		screen_manager = self.manager
		# 1 - error trigger / 0 - valid trigger
		if user_source_data_valid(self.user_source_data) == 1:
			Clock.schedule_once(lambda _: setattr(screen_manager, "current", "error_activity"))
		elif user_source_data_valid(self.user_source_data) == 0:
			# history / write
			history_write(urllib.parse.urlparse(self.user_source_data).netloc, "source_data")
			threading.Thread(target=self.tech_data_get).start()


	def tech_data_get(self):
		screen_manager       = self.manager
		raw_tech_target_dict = tech_core_lookup(self.user_source_data)
		tech_target_dict     = formatted_data_dict(raw_tech_target_dict)
		# history / write
		history_write(tech_target_dict, "lookup_data")
		screen_manager.get_screen("output_activity").lookup_user_result = eval(str(tech_target_dict))
		Clock.schedule_once(lambda _: setattr(screen_manager, "current", "output_activity"))


# screen / output activity
class OutputActivity(Screen):
	lookup_user_result    = {}
	lookup_target_label   = StringProperty()
	lookup_datetime_label = StringProperty()
	lookup_result_label   = StringProperty()


	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.layout = GridLayout(cols=1, spacing=8, pos_hint={"center_x": 0.5, "center_y": 0.54}, size_hint=(0.7, 0.50))
		self.layout.bind(minimum_height=self.layout.setter("height"))
		self.add_widget(self.layout)


	def on_enter(self):
		super().on_enter()
		lookup_user_result = self.lookup_user_result
		if all(tech_cats is None for tech_cats in lookup_user_result["tech_cats"]):
			self.lookup_result_label = "NO RESULT"
		self.lookup_target_label   = "".join(lookup_user_result["target"])
		self.lookup_datetime_label = "".join(lookup_user_result["datetime"])
		for tech_cats, tech_names, tech_descs, tech_webs, methods, fingerprints in zip(lookup_user_result["tech_cats"], lookup_user_result["tech_name"],
			lookup_user_result["tech_desc"], lookup_user_result["tech_web"], lookup_user_result["method"], lookup_user_result["fingerprint"]):
			if tech_cats != None and tech_names != None and tech_descs != None and tech_webs != None and methods != None and methods != None:
				for tech_cat, tech_name, tech_desc, tech_web, method, fingerprint in zip(tech_cats, tech_names, tech_descs, tech_webs, methods, fingerprints):
					self.add_button(tech_cat, tech_name, tech_desc, tech_web, method, fingerprint)


	def add_button(self, tech_cat, tech_name, tech_desc, tech_web, method, fingerprint):
		button = Button(text=tech_name, on_press=lambda _: self.button_full_trigger(
			tech_cat, tech_name, tech_desc, tech_web, method, fingerprint), background_color=(0, 0, 0, 1), bold="true")
		button.bind(size=self.canvas_button)
		self.layout.add_widget(button)


	def canvas_button(self, instance, value):
		instance.canvas.before.clear()
		with instance.canvas.before:
			Color(1, 1, 1, 1)
			Line(rectangle=(instance.x, instance.y, instance.width, instance.height), width=1)


	def button_full_trigger(self, tech_cat, tech_name, tech_desc, tech_web, method, fingerprint):
		screen_manager                                                             = self.manager
		screen_manager.current                                                     = "output_full_activity"
		screen_manager.get_screen("output_full_activity").lookup_target_label      = self.lookup_target_label
		screen_manager.get_screen("output_full_activity").lookup_datetime_label    = self.lookup_datetime_label
		screen_manager.get_screen("output_full_activity").lookup_tech_cat_label    = ", ".join(tech_cat)
		screen_manager.get_screen("output_full_activity").lookup_tech_name_label   = tech_name
		screen_manager.get_screen("output_full_activity").lookup_tech_desc_label   = f"{tech_desc[:35]} ..."
		screen_manager.get_screen("output_full_activity").lookup_tech_web_label    = tech_web
		screen_manager.get_screen("output_full_activity").lookup_method_label      = method
		screen_manager.get_screen("output_full_activity").lookup_fingerprint_label = f"--> {fingerprint}"
		self.layout.clear_widgets()


	def button_trigger(self):
		screen_manager           = self.manager
		screen_manager.current   = "main_activity"
		self.lookup_result_label = ""
		self.layout.clear_widgets()


# screen / output full activity
class OutputFullActivity(Screen):
	lookup_target_label      = StringProperty()
	lookup_datetime_label    = StringProperty()
	lookup_tech_cat_label    = StringProperty()
	lookup_tech_name_label   = StringProperty()
	lookup_tech_desc_label   = StringProperty()
	lookup_tech_web_label    = StringProperty()
	lookup_method_label      = StringProperty()
	lookup_fingerprint_label = StringProperty()


	def __init__(self, **kwargs):
		super().__init__(**kwargs)


	def on_enter(self):
		super().on_enter()
		self.ids.lookup_image.source = "src/assets/icon.png"


	def button_trigger(self):
		screen_manager                = self.manager
		screen_manager.current        = "output_activity"
		self.lookup_target_label      = ""
		self.lookup_datetime_label    = ""
		self.lookup_tech_cat_label    = ""
		self.lookup_tech_name_label   = ""
		self.lookup_tech_desc_label   = ""
		self.lookup_tech_web_label    = ""
		self.lookup_method_label      = ""
		self.lookup_fingerprint_label = ""
		self.ids.lookup_image.source  = "src/assets/nothing.png"


# screen / history activity
class HistoryActivity(Screen):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.layout = GridLayout(cols=1, spacing=8, pos_hint={"center_x": 0.5, "center_y": 0.57}, size_hint=(0.7, 0.6))
		self.layout.bind(minimum_height=self.layout.setter("height"))
		self.add_widget(self.layout)
		Clock.schedule_interval(self.user_history, 1)


	def user_history(self, call):
		self.layout.clear_widgets()
		# history / read
		user_history        = [history for history in history_read("source_data").split("\n") if history != ""]
		lookup_user_history = [lookup_history for lookup_history in history_read("lookup_data").split("\n") if lookup_history != ""]
		# history / detect empty history
		if not user_history: user_history = ["EMPTY"]
		# history / limit / remove first element of history
		if len(user_history) >= 11: history_remove("source_data")
		if len(lookup_user_history) >= 11: history_remove("lookup_data")
		for count, history in enumerate(user_history):
			# history / empty trigger
			if len(user_history) < 10:
				user_history.append("EMPTY")
			# history / output
			self.add_button(count, history, lookup_user_history)


	def add_button(self, count, history_text, lookup_user_history):
		if history_text == "EMPTY":
			button = Button(text=history_text, on_press=self.button_home_trigger,
				background_color=(0, 0, 0, 1), bold="true")
		if history_text != "EMPTY":
			button = Button(text=history_text, on_press=lambda _: self.button_result_trigger(count, lookup_user_history),
				background_color=(0, 0, 0, 1), bold="true")
		button.bind(size=self.canvas_button)
		self.layout.add_widget(button)


	def canvas_button(self, instance, value):
		instance.canvas.before.clear()
		with instance.canvas.before:
			Color(1, 1, 1, 1)
			Line(rectangle=(instance.x, instance.y, instance.width, instance.height), width=1)


	def button_result_trigger(self, count, lookup_user_history):
		screen_manager     = self.manager
		lookup_user_result = lookup_user_history[count]
		screen_manager.get_screen("output_activity").lookup_user_result = eval(lookup_user_result)
		screen_manager.current = "output_activity"


	def button_clear_trigger(self):
		# history / clear
		history_clear("source_data")
		history_clear("lookup_data")


	def button_home_trigger(self, on_press):
		screen_manager         = self.manager
		screen_manager.current = "main_activity"


	def button_trigger(self):
		screen_manager         = self.manager
		screen_manager.current = "main_activity"


class TechnologyLookupApp(App):
	def build(self):
		screen_manager = ScreenManager()
		# main activity
		screen_manager.add_widget(MainActivity(name="main_activity"))
		# error activity
		screen_manager.add_widget(ErrorActivity(name="error_activity"))
		# usage activity
		screen_manager.add_widget(UsageActivity(name="usage_activity"))
		# load activity
		screen_manager.add_widget(LoadActivity(name="load_activity"))
		# output activity
		screen_manager.add_widget(OutputActivity(name="output_activity"))
		# output full activity
		screen_manager.add_widget(OutputFullActivity(name="output_full_activity"))
		# history activity
		screen_manager.add_widget(HistoryActivity(name="history_activity"))
		return screen_manager


if __name__ == "__main__":
	TechnologyLookupApp().run()