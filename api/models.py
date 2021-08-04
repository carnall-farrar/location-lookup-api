from dataclasses import dataclass
from api import db

@dataclass
class Population(db.Model):
    id: int
    ccg_code: str 
    ccg_name: str
    stp_code: str
    stp_name: str 
    file: str
    FID: int
    STP20CD: str
    STP20CDH: str
    STP20NM: str
    NHSER20CD: str
    NHSER20CDH: str
    NHSER20NM: str
     
    __tablename__ = 'population'
    id = db.Column(db.Integer, primary_key=True)
    ccg_code = db.Column(db.String(50), nullable=False)
    ccg_name = db.Column(db.String(500), nullable=False)
    stp_code = db.Column(db.String(50), nullable=False)
    stp_name = db.Column(db.String(500), nullable=False)
    file = db.Column(db.String(50), nullable=False)
    FID = db.Column(db.Integer)
    STP20CD = db.Column(db.String(200), nullable=False)
    STP20CDH = db.Column(db.String(200), nullable=False)
    STP20NM = db.Column(db.String(200), nullable=False)
    NHSER20CD = db.Column(db.String(200), nullable=False)
    NHSER20CDH = db.Column(db.String(200), nullable=False)
    NHSER20NM = db.Column(db.String(200), nullable=False)
    
    def __init__(self, ccg_code=None, ccg_name=None, stp_code=None, stp_name=None, 
                 file=None, FID=None, STP20CD=None, STP20CDH=None, STP20NM=None,
                 NHSER20CD=None, NHSER20CDH=None, NHSER20NM=None):
        self.ccg_code= ccg_code
        self.ccg_name= ccg_name
        self.stp_code= stp_code
        self.stp_name= stp_name
        self.file = file
        self.FID = FID
        self.STP20CD = STP20CD
        self.STP20CDH = STP20CDH
        self.STP20NM = STP20NM
        self.NHSER20CD = NHSER20CD
        self.NHSER20CDH = NHSER20CDH
        self.NHSER20NM = NHSER20NM
    
    def __repr__(self):
        return '<id {}>'.format(self.id)