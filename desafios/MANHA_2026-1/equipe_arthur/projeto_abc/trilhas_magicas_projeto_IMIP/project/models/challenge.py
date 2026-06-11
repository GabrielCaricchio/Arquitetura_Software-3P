from extensions import db


class Challenge(db.Model):
    """Perguntas geradas a partir da história."""
    __tablename__ = "challenges"

    id = db.Column(db.Integer, primary_key=True)
    story_id = db.Column(db.Integer, db.ForeignKey("stories.id"), nullable=False)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)

    story = db.relationship("Story", back_populates="challenges")
