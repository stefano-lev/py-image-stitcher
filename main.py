import sys

if len(sys.argv) > 1:

    from cli import run_cli
    run_cli()

else:

    from gui import launch_gui
    launch_gui()