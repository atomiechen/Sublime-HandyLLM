import sublime
import sublime_plugin

from .utils import settings_on_change


handyllm_settings = sublime.load_settings("HandyLLM.sublime-settings")


class SettingKeys:
	ENABLE_ROLE = "enable_underline_role"
	ENABLE_FM = "enable_decor_frontmatter"
	ROLE_STYLE = "role_underline_style"


class Core:
	setting_enable_key = ""
	region_key = ""
	selector = ""

	def update_view(self, view):
		regions = self.get_target_regions(view)
		if handyllm_settings.get(self.setting_enable_key):
			self.decor(view, regions)
		else:
			self.remove_decor(view, regions)

	def get_target_regions(self, view):
		regions = view.find_by_selector(self.selector)
		return regions

	def decor(self, view, regions):
		pass

	def remove_decor(self, view, regions):
		view.add_regions(
			key=self.region_key,
			regions=regions,
			scope="",
		)


class CoreDecorRole(Core):
	setting_enable_key = SettingKeys.ENABLE_ROLE
	region_key = "role"
	selector = "meta.block.role"

	def decor(self, view, regions):
		underline_style = handyllm_settings.get(SettingKeys.ROLE_STYLE)
		underline_style = underline_style.lower()
		if underline_style == "solid":
			style_flag = sublime.DRAW_SOLID_UNDERLINE
		elif underline_style == "stippled":
			style_flag = sublime.DRAW_STIPPLED_UNDERLINE
		elif underline_style == "squiggly":
			style_flag = sublime.DRAW_SQUIGGLY_UNDERLINE
		view.add_regions(
			key=self.region_key,
			regions=regions,
			scope="markup.heading",
			flags=style_flag | sublime.DRAW_NO_FILL | sublime.DRAW_NO_OUTLINE,
		)


class CoreDecorFrontmatter(Core):
	setting_enable_key = SettingKeys.ENABLE_FM
	region_key = "frontmatter"
	selector = "meta.frontmatter.block"

	def decor(self, view, regions):
		if self.has_valid_frontmatter(view):
			self.remove_decor(view, regions)
		else:
			view.add_regions(
				key=self.region_key,
				regions=regions,
				scope="invalid",
			)

	@staticmethod
	def has_valid_frontmatter(view):
		region = view.find(
			pattern=r'^---[^\S\r\n]*\n([\s\S]*?)\n---',
			start_pt=0,
		)
		if region.a == 0:
			return True
		else:
			return False


class HandyllmBaseListener(sublime_plugin.ViewEventListener):
	core = Core()

	@classmethod
	def is_applicable(cls, settings):
		return settings.get('syntax') == 'Packages/HandyLLM/Hprompt.sublime-syntax'

	@classmethod
	def applies_to_primary_view_only(cls):
		return False

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.update_view()

	def update_view(self):
		self.core.update_view(self.view)


class HandyllmUnderlineRoleListener(HandyllmBaseListener):
	"""Decorating block heads."""

	core = CoreDecorRole()

	def on_modified_async(self):
		self.update_view()


class HandyllmDecorFrontmatterListener(HandyllmBaseListener):
	"""Decorating frontmatter invalid area."""

	core = CoreDecorFrontmatter()

	def on_modified_async(self):
		self.update_view()


listen_setting_keys = [
	SettingKeys.ENABLE_ROLE,
	SettingKeys.ENABLE_FM,
	SettingKeys.ROLE_STYLE,
]

def update_all_views():
	core_bh = CoreDecorRole()
	core_fm = CoreDecorFrontmatter()
	for window in sublime.windows():
		for view in window.views():
			core_bh.update_view(view)
			core_fm.update_view(view)

def plugin_loaded():
    settings = sublime.load_settings("HandyLLM.sublime-settings")
    settings_on_change(settings, listen_setting_keys)(
        lambda _: update_all_views()
    )

def plugin_unloaded():
    settings = sublime.load_settings("HandyLLM.sublime-settings")
    settings_on_change(settings, listen_setting_keys, clear=True)
