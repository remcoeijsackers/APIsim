import os
from subprocess import call
import yaml

from unit import config_unit
class Settings:

  def __init__(self, config) -> None:
      self.config = config

  def editconfig(self):
    EDITOR = os.environ.get('EDITOR') if os.environ.get('EDITOR') else 'vim'
    with open(self.config) as tf:
      tf.flush()
      call([EDITOR, tf.name])

  def loadconfig(self) -> config_unit:
    with open(self.config, 'r') as stream:
      try:
        x = yaml.safe_load(stream)
        ps = x.get('auto_printsteps')
        tb = x.get('auto_printtable')
        fb = x.get('auto_fallback')
        cr = x.get('count_repeat')
        cu = config_unit(ps,fb, tb, cr)
      except yaml.YAMLError as exc:
        print(exc)
      return cu 
      
