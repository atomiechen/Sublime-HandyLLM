import logging

import sublime
import sublime_plugin


__all__ = [
	'HandyllmNewFileCommand',
]

logger = logging.getLogger(__name__)

hprompt_snippet=r"""---
meta:
  credential_path: ${1:credential.yml}
  var_map_path: ${2:var_map.txt}
model: ${3:gpt-4o}
temperature: ${4:0.3}
---

\$system\$
${5:Define your system message here.}

\$user\$
${6:Define your first user message here.}
$0"""


class HandyllmNewFileCommand(sublime_plugin.WindowCommand):
	"""Create a new file."""

	def run(self, action: str):
		if action != 'hprompt':
			logger.error("Unknown action %r", action)
			return

		# create new file
		v = self.window.new_file()


		# set syntax
		v.assign_syntax('scope:source.hprompt')

		v.run_command('insert_snippet', {'contents': hprompt_snippet})
