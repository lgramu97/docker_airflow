import click

@click.command()
@click.option(
    '--date',
    required=True,
    help='Execution date format yyyy-mm-dd'
)
def main(date):
    print(date)
    
if __name__ == '__main__':
    main()