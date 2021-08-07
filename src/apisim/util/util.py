import os
from subprocess import call

class settings:

  def __init__(self, config) -> None:
      self.config = config

  def editconfig(self):
    EDITOR = os.environ.get('EDITOR') if os.environ.get('EDITOR') else 'vim'
    with open(self.config) as tf:
      tf.flush()
      call([EDITOR, tf.name])
