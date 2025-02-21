from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship,declarative_base
from TextPreProcessing import text_processing
from SpeechToText import model
from Speaker import speaker
from Recorder import recorder

Base = declarative_base()

class Mode(Base):
    __tablename__ = 'modes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    commands = relationship('Command', back_populates='mode', cascade='all, delete-orphan')

class Command(Base):
    __tablename__ = 'commands'
    id = Column(Integer, primary_key=True, autoincrement=True)
    mode_id = Column(Integer, ForeignKey('modes.id'))
    command = Column(String, nullable=False)
    mode = relationship('Mode', back_populates='commands')

class ModeDatabase:
    def __init__(self, db_name='sqlite:///modes.db'):
        self.engine = create_engine(db_name)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def add_mode(self, mode_name, commands):
        session = self.Session()
        if session.query(Mode).filter_by(name=mode_name).first():
            session.close()
            raise ValueError(f"Mode with name '{mode_name}' already exists.")
        mode = Mode(name=mode_name, commands=[Command(command=cmd) for cmd in commands])
        session.add(mode)
        session.commit()
        session.close()

    def get_mode_by_name(self, mode_name):
        session = self.Session()
        mode = session.query(Mode).filter_by(name=mode_name).first()
        if mode:
            mode_data = {'id': mode.id, 'name': mode.name, 'commands': [cmd.command for cmd in mode.commands]}
            session.close()
            return mode_data
        else:
            session.close()
            raise ValueError(f"Mode with name '{mode_name}' does not exist.")

    def update_mode_by_name(self, mode_name, commands):
        session = self.Session()
        mode = session.query(Mode).filter_by(name=mode_name).first()
        if not mode:
            session.close()
            raise ValueError(f"Mode with name '{mode_name}' does not exist.")
        mode.commands = [Command(command=cmd) for cmd in commands]
        session.commit()
        session.close()

    def close(self):
        self.engine.dispose()






# Example usage
if __name__ == '__main__':
    db = ModeDatabase()
    try:
        db.add_mode('Study Mode', ['Turn on the lights', 'Set the temperature to 24 degrees', 'Set the fan speed to 3'])
    except ValueError as e:
        print(e)
    try:
        mode = db.get_mode_by_name('Study Mode')
        print(mode['commands'])
    except ValueError as e:
        print(e)
    db.close()

    db.create_mode()
