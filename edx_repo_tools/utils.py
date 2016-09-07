import click


def dry_echo(dry, message, *args, **kwargs):
    """
    Print a command to the console (like :func:`click.echo`), but if ``dry`` is True,
    then prefix the message with a warning message stating that the action was
    skipped. All unknown args and kwargs are passed to :func:`click.echo`

    Example usage:

        dry_echo(dry, "Firing ze missiles!", fg='red')
        if not dry:
            fire_ze_missiles()

    Arguments:
        dry (bool): Whether to prefix the dry-run notification
        message: The message to print
    """
    click.echo("{dry}{message}".format(
        dry=click.style("DRY RUN - SKIPPED: ", fg='yellow', bold=True) if dry else "",
        message=click.style(message, *args, **kwargs)
    ))


def dry(f, help='Enable/disable actions taken by the script'):
    return click.option(
        '--dry/--yes',
        is_flag=True,
        default=True,
        help=help,
    )(f)

