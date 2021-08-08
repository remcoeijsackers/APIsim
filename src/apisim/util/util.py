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
        s = x.get('auto_store')
        cr = x.get('count_repeat')
        cu = config_unit(ps,fb, tb, s, cr)
      except yaml.YAMLError as exc:
        print(exc)
      return cu 
      
class helpers:
  def __init__(self) -> None:
      pass

  def print_help(self) -> str:
        helpv = """
        APIsim [url] [options]

        Options [Params]:
        --url: [String] Urls to call
        --authurl: [String] Url to login to
        --creds: [String] Credentials to login with 
                * username, password
        --command: [String]
                * visual :Run the cli dashboard
        --repeat/-r: [Int] Times the calls should be repeated
        --mode/-m: [String] Type of request 
                * get
                * post

        --file/-f: [String] Input of output file for the request
        --fallback/-fb: [None] Fallback to the tor network
        --verbose/-v: [None] Print out the results in a table
        --store/-s: [None] Store the results in the db
        --query/-q:  [None] Query the db
        --printsteps/-ps: [None] print each step

        --edit/-e: [None] edit config file
        """
        return helpv