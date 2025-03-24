import sublime
import sublime_plugin


__all__ = [
	'HandyllmDecorBlockHeadListener',
	'HandyllmDecorFrontmatterListener',
]

handyllm_settings = sublime.load_settings("HandyLLM.sublime-settings")



class HandyllmBaseListener(sublime_plugin.ViewEventListener):

	setting_enable_key = ""
	region_key = ""
	selector = ""

	removed = True  # mark if the decoration has removed after disable

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
		regions = self.get_target_regions()
		if handyllm_settings.get(self.setting_enable_key):
			self.removed = False
			self.decor(regions)
		else:
			if not self.removed:
				self.remove_decor(regions)
				self.removed = True

	def get_target_regions(self):
		regions = self.view.find_by_selector(self.selector)
		return regions

	def decor(self, regions):
		pass

	def remove_decor(self, regions):
		self.view.add_regions(
			key=self.region_key,
			regions=regions,
			scope="",
		)


class HandyllmDecorBlockHeadListener(HandyllmBaseListener):
	"""Decorating block heads."""

	setting_enable_key = "enable_decor_block_head"
	region_key = "block_head"
	selector = "meta.block.head"

	def on_modified_async(self):
		self.update_view()

	def decor(self, regions):
		self.view.add_regions(
			key=self.region_key,
			regions=regions,
			scope="meta.block.head",
			flags=sublime.HIDDEN,
			annotations=['————————']*len(regions),
			annotation_color='#fff0',
		)


class HandyllmDecorFrontmatterListener(HandyllmBaseListener):
	"""Decorating frontmatter invalid area."""

	setting_enable_key = "enable_decor_frontmatter"
	region_key = "frontmatter"
	selector = "meta.frontmatter.block"

	def on_modified_async(self):
		self.update_view()

	def decor(self, regions):
		if self.has_valid_frontmatter():
			self.remove_decor(regions)
		else:
			self.view.add_regions(
				key=self.region_key,
				regions=regions,
				scope="invalid",
			)

	def has_valid_frontmatter(self):
		region = self.view.find(
			pattern=r'^---[^\S\r\n]*\n([\s\S]*?)\n---',
			start_pt=0,
		)
		if region.a == 0:
			return True
		else:
			return False
