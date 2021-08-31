import sys

from flask.cli import FlaskGroup

from app import create_app, db
from app.api.location.models import CcgToStpLookup


app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command('recreate_db')
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command('add_ccg_lookup')
def add_ccg_lookup():
    """
    ,ccg_code,ccg_name,stp_code,stp_name,file,FID,STP20CD,STP20CDH,STP20NM,NHSER20CD,NHSER20CDH,NHSER20NM

    """
    with open("data/combined_lookup.csv") as fp:
        lines = fp.readlines()

        for line in lines[1:]:
            split = line.split("|")
            row = CcgToStpLookup.create(
                ccg_code=split[1].strip(),
                ccg_name=split[2].strip(),
                stp_code=split[3].strip(),
                stp_cdh=split[8].strip(),
                stp_name=split[4].strip(),
                region_code=split[10].strip(),
                region_cdh=split[11].strip(),
                region_name=split[12].strip(),
                file=split[5].strip()
            )
            print(row)


if __name__ == '__main__':
    cli()
