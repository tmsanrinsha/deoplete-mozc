import functools
import os
import re
import sys

from .base import Base
from deoplete.util import debug

sys.path.insert(0, os.path.dirname(__file__))
import mozc


class Source(Base):

    def __init__(self, vim):
        Base.__init__(self, vim)

        self.name = 'mozc'
        self.mark = '[Mozc]'
        # self.filetypes = ['hoge']
        self.matchers = []
        self.sorters = []
        self.min_pattern_length = 1
        self.is_volatile = True
        self.rank = 50

    def on_init(self, context):
        vars = context['vars']

        mozc_emacs_helper_path = vars.get('deoplete#sources#mozc#mozc_emacs_helper_path', 'mozc_emacs_helper')

        self.mozc = mozc.Mozc(mozc_emacs_helper_path, functools.partial(debug, self.vim))
        try:
            pass
        except Exception:
            # Ignore the error
            pass

    def on_event(self, context):
        # ここでCompleteDone?
        if context['event'] == 'BufRead':
            try:
                # vim autocmd event based works
                pass
            except Exception:
                # Ignore the error
                pass

    def get_complete_position(self, context):
        m = re.search(r'[\x21-\x7E]+$', context['input'])
        return m.start() if m else -1

    def gather_candidates(self, context):
        vars = context['vars']

        additional_key = vars.get('deoplete#sources#mozc#additional_key', '')
        res = self.mozc.change_input(context['complete_str'], additional_key)

        candidates = [{'word': c["value"],
                       'abbr': "{0} {1}".format(c["value"], c["annotation"]["description"])}
                      if "annotation" in c and "description" in c["annotation"]
                      else {'word':  c["value"]}
                      for c in res]

        # debug(self.vim, candidates)
        return candidates
