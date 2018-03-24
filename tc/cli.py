import click

@click.group()
def main():
    pass

@main.command()
def status():
    """Get the build related info from team city server"""
    click.echo('SUCCESS')