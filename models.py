from datetime import datetime
from flask import Flask, session, redirect, url_for, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from webapp import db

#Database relationships https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html
from sqlalchemy.orm import declarative_base, relationship

#password encrpytion
from passlib.hash import sha256_crypt

class user(db.Model):
    __tablename__= "user_table"
    _id = db.Column('id', db.Integer, primary_key=True)
    user_name = db.Column("user_name", db.String(100), unique=True, index=True)
    password_hash = db.Column(db.String(100))
    random_salt = db.Column(db.String(16))
    created_date = db.Column(db.String(30)) #year/month/day
    title = db.Column(db.String(69)) #Harrison Leece "The Whispering Shiba"
    status = db.Column(db.String(69))
    email = db.Column(db.String(60), unique=True, index=True) #blahblah@mailmail.com
    points = db.Column(db.Integer)
    owned_tools = relationship("tool", back_populates="owned_by")


    def __init__(self, user_name, password, email):
        now = datetime.now()
        print(password)
        #salt = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        self.user_name = user_name;
        self.password_hash = sha256_crypt.hash(password);

        self.created_date = now.strftime("%Y/%m/%d");
        self.title = "";
        self.status = "New";
        self.email = email;
        self.points = 0;
        self.owned_tools;

    def verify_password_hash(self, password_in):
        if (sha256_crypt.verify(password_in, self.password_hash)):
            return True
        return False

class tool(db.Model):
    __tablename__ = "tool_table"
    _id = db.Column('id', db.Integer, primary_key=True)
    tool_name = db.Column(db.String(100))
    comment = db.Column(db.String(1000))
    parent_id = db.Column(db.Integer, db.ForeignKey("user_table.id"))
    owned_by = relationship("user", back_populates="owned_tools")
    #still need a relationship to accessories
    accessories = relationship("accessory", back_populates="owned_by")

    def __init___(self, name, comment, owner):
        self.tool_name = name; self.comment = comment; self.owned_by = owner;
        self.parent_id;
        self.accessories;

    def add_accessory(self, accessory_id):
        #super important comment
        pass

class accessory(db.Model):
    __tablename__ = "accessory_table"
    _id = db.Column('id', db.Integer, primary_key = True)
    name = db.Column(db.String(60))
    comment = db.Column(db.String(60))
    associated_tools = db.Column(db.String(60))
    parent_id = db.Column(db.Integer, db.ForeignKey("tool_table.id"))
    #relationship to owning tool
    owned_by = relationship("tool", back_populates="accessories")

    def __init__(self, name, comment, tools):
        self.name = name; self.comment = comment; self.associated_tools = tools;
        self.owned_by;
        self.parent_id;
