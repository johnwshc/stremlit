from flask_wtf import FlaskForm
from wtforms import (StringField, TextAreaField, IntegerField, BooleanField,
                     RadioField, SelectField)
from wtforms.validators import InputRequired, Length
import os
from config import Config

class PBPoetryPublishForm(FlaskForm):


    title = StringField('Title', validators=[InputRequired(),
                                             Length(min=10, max=100)])
    dir = Config.WNL_DIR

    fnames = os.listdir(dir)
    poetry_audio_names = [f for f in fnames if f.startswith('poet')]
    choices_tuples = [(f, f) for f in poetry_audio_names]

    filename = SelectField('Audio File', validators=[InputRequired()], choices=choices_tuples)
    description = TextAreaField('Description',
                                validators=[InputRequired(),
                                            Length(max=500)])
    broadcast = StringField('Broadcast Info', validators=[InputRequired(), Length(max=80)])
    rec_date = StringField('Recording Date', validators=[InputRequired(), Length(max=40)])
    image_url = StringField("image url", validators=[InputRequired(), Length(max=160)])
    headline = StringField("headline", validators=[InputRequired(), Length(max=160)])
    hosts = StringField('Add Host(s) csv', validators=[Length(max=80)])
    guests = StringField('Guests (csv)', validators=[Length(max=80)])
    poem_names_dir = os.path.join(Config.basedir, 'show_resources/poetry')
    poem_choices = [(f,f) for f in os.listdir(poem_names_dir) if f.startswith('poem')]
    poem = SelectField('Poem of the Week', validators=[InputRequired()], choices=poem_choices)
    poem_title = StringField('Poem Title', validators=[InputRequired(), Length(max=80)])
    poet = StringField('Poet', validators=[InputRequired(), Length(max=80)], default="Homer")


class PBLaborPublishForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired(),
                                             Length(min=10, max=100)])
    dir = Config.WNL_DIR
    fnames = os.listdir(dir)
    labor_audio_names = [f for f in fnames if f.startswith('labor')]
    choices_tuples = [(f, f) for f in labor_audio_names]

    filename = SelectField('Audio File', validators=[InputRequired()], choices=choices_tuples)
    description = TextAreaField('Description',
                                validators=[InputRequired(),
                                            Length(max=400)])
    broadcast = StringField('Broadcast Info', validators=[InputRequired(), Length(max=80)])
    rec_date = StringField('Recording Date', validators=[InputRequired(), Length(max=40)])
    image_url = StringField("image url", validators=[InputRequired(), Length(max=160)])
    headline = StringField("headline", validators=[InputRequired(), Length(max=160)])
    hosts = StringField('Add Host(s) csv', validators=[Length(max=80)])
    guests = StringField('Guests (csv)', validators=[Length(max=80)])


class PBWNLPublishForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired(),
                                             Length(min=10, max=100)])
    dir = Config.WNL_DIR
    fnames = os.listdir(dir)
    wnl_audio_names = [f for f in fnames if f.startswith('wnl')]
    choices_tuples = [(f, f) for f in wnl_audio_names]

    filename = SelectField('Audio File', validators=[InputRequired()], choices=choices_tuples)
    description = TextAreaField('Description',
                                validators=[InputRequired(),
                                            Length(max=1500)])
    broadcast = StringField('Broadcast Info', validators=[InputRequired(), Length(max=80)])
    rec_date = StringField('Recording Date', validators=[InputRequired(), Length(max=40)])
    image_url = StringField("image url", validators=[InputRequired(), Length(max=360)])
    headline = StringField("headline", validators=[InputRequired(), Length(max=160)])
    hosts = StringField('Add Host(s) csv', validators=[Length(max=80)])
    guests = StringField('Guests (csv)', validators=[Length(max=80)])


class PBSportsPublishForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired(),
                                             Length(min=10, max=100)])
    dir = Config.WNL_DIR
    fnames = os.listdir(dir)
    sports_audio_names = [f for f in fnames if f.startswith('sport')]
    choices_tuples = [(f, f) for f in sports_audio_names]

    filename = SelectField('Audio File', validators=[InputRequired()], choices=choices_tuples)
    description = TextAreaField('Description',
                                validators=[InputRequired(),
                                            Length(max=1000)])
    broadcast = StringField('Broadcast Info', validators=[InputRequired(), Length(max=80)])
    rec_date = StringField('Recording Date', validators=[InputRequired(), Length(max=40)])
    image_url = StringField("image url", validators=[InputRequired(), Length(max=360)])
    headline = StringField("headline", validators=[InputRequired(), Length(max=160)])
    hosts = StringField('Add Host(s) csv', validators=[Length(max=80)])
    guests = StringField('Guests (csv)', validators=[Length(max=80)])


class PBRecoveryPublishForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired(),
                                             Length(min=10, max=100)])
    dir = Config.WNL_DIR
    fnames = os.listdir(dir)
    recovery_audio_names = [f for f in fnames if f.startswith('rec')]
    choices_tuples = [(f, f) for f in recovery_audio_names]

    filename = SelectField('Audio File', validators=[InputRequired()], choices=choices_tuples)
    description = TextAreaField('Description',
                                validators=[InputRequired(),
                                            Length(max=300)])
    broadcast = StringField('Broadcast Info', validators=[InputRequired(), Length(max=80)])
    rec_date = StringField('Recording Date', validators=[InputRequired(), Length(max=40)])
    image_url = StringField("image url", validators=[InputRequired(), Length(max=260)])
    headline = StringField("headline", validators=[InputRequired(), Length(max=160)])
    hosts = StringField('Add Host(s) csv', validators=[Length(max=80)])
    guests = StringField('Guests (csv)', validators=[Length(max=80)])


class PytuberForm(FlaskForm):
     youtube_url = StringField("YouTube URL", validators=[InputRequired(), Length(max=120)])
     fn = StringField("Download File name", validators=[InputRequired(), Length(max=20)])


