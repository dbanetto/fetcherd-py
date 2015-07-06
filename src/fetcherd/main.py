"""fetcherd

Usage:
    fetcherd (-h | --help)
    fetcherd --version
    fetcherd (-d | --daemon) [-c <path> | --config=<config>]
    fetcherd [--fetch | --sort] [-c <path> | --config=<config>]

Options:
    -h --help                   Show this screen
    --version                   Show version
    -d --daemon                 Run as daemon
    --fetch                     Run fetch
    --sort                      Run sort
"""
from docopt import docopt

import grp
import signal
import daemon
import lockfile


def init():
    pass


def main():
    pass


def cleanup():
    pass


def reload_config():
    pass


def daemonize(settings):
    pid = settings['pid']
    working_dir = settings['working_directory']

    context = daemon.DaemonContext(
        working_directory=working_dir,
        umask=0o002,
        pidfile=lockfile.FileLock(pid),
        )

    context.signal_map = {
        signal.SIGTERM: cleanup,
        signal.SIGHUP: 'terminate',
        signal.SIGUSR1: reload_config,
        }

    context.gid = grp.getgrnam('nobody').gr_gid

    init()

    with context:
        main()

if __name__ == '__main__':
    args = docopt(__doc__, version='fetcherd 0.1')
    print(args)

    if args['--daemon']:
        daemonize({'pid': '/tmp/fetcher.d', 'working_directory': '/tmp'})
