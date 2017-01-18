#!/usr/bin/env python3

import sh, sys
from utiltools import shellutils
from utiltools.shellutils import file_exists, read_file
from utiltools.shellutils import expand_link, ls
from settings import gen_arg_parser, gen_new_conf, find_conf_path, parse_conf
from helpers import get_path_matches

from utiltools.shellutils import get_abs_path_relative_to
su_get_path = get_abs_path_relative_to

from settings import parse_args, print_help, usage

conf_path = '.vivie.conf'
data_dir = '.vivie/'
avail_cmd_args = ['setup', 'snapshot', 'help', 'status']

vim_view_path = expand_link('~/.vim/view/') + '/'

full_home_path = expand_link('~')

def take_snapshot(file_lst):
   for local_fpath in file_lst:
      print('snapshotting:', local_fpath)
      local_fpath = expand_link(local_fpath).replace(full_home_path, '~')
      print('after cleanup:', local_fpath)

      view_fname = path_to_vim(local_fpath)

      view_fpath = vim_view_path + view_fname
      view_localdest = data_dir + view_fname

      sh.rm('-Rf', view_localdest)
      sh.cp(view_fpath, view_localdest)

def run_setup(file_lst):
   for local_fpath in file_lst:
      print('setting up:', local_fpath)
      local_fpath = expand_link(local_fpath).replace(full_home_path, '~')

      view_fname = path_to_vim(local_fpath)
      #print(view_fname)

      view_dest_path = vim_view_path + view_fname
      view_local_path = data_dir + view_fname
      sh.cp(view_local_path, view_dest_path)


def dispatch_init(conf, conf_path, project_name):
   if project_name is None:
      print('error: no project name. check flags with --help')
      return #TODO: can be sys.exit()

   if file_exists(conf_path):
      print('error: .vivie.conf file already exists..exiting')
      return

   gen_new_conf(project_name, conf_path)
   #TODO: create directories, initialize stuff
   pass


def dispatch_setup(conf, conf_path, project_name):
   print(x)

   return
   to_track_lst = [] #list of paths to track
   run_setup(to_track_lst)



def dispatch_snapshot(conf, conf_path, project_name):
   conf_path = su_get_path(conf_path)
   file_paths = ls(conf_path, rec=True)
   #print(files)

   print(get_path_matches(file_paths, conf['include']))
   print(conf)
   return

   to_track_lst = [] #list of paths to track
   take_snapshot(to_track_lst)

def dispatch_status(conf, project_name):
   pass

def main():

   arg_parser = gen_arg_parser()
   args = arg_parser.parse_args()

   conf_path = args.conf_path
   action = args.action
   project_name = args.project_name

   conf_path = find_conf_path(conf_path)
   print(conf_path)

   conf = None
   if conf_path is not None:
      conf = parse_conf(conf_path)

   if conf is None and action in ['setup', 'snapshot']:
      print("didn't find conf. can't run command..exiting")
      return

   if action == 'init':
      dispatch_init(conf, conf_path, project_name)
   elif action == 'setup':
      dispatch_setup(conf, conf_path, project_name)
   elif action == 'snapshot':
      dispatch_snapshot(conf, conf_path, project_name)
   elif action == 'status':
      dispatch_status(conf, conf_path, project_name)

   return


   to_track_lst = None

   if not file_exists(conf_path):
      err_str = "can't find %s. " % (conf_path, )
      print("doesn't look like .vivie folder:", err_str)
      sys.exit(1)
   else:
      to_track_str = read_file(conf_path)
      to_track_lst = to_track_str.split('\n')[:-1]

   if not file_exists(data_dir):
      sh.mkdir(data_dir)

   cmd = parse_args()

   if cmd == 'help':
      print_help()
   elif cmd == 'setup':
      run_setup(to_track_lst)
   elif cmd == 'snapshot':
      take_snapshot(to_track_lst)
   elif cmd == 'status':
      pass

main()


