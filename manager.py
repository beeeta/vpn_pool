import click
from vpn_pool import engine,Base

@click.command()
@click.argument('name')
def db(name):
    if(name=='init_db'):
        Base.metadata.create_all(engine)

if __name__ == '__main__':
    db()