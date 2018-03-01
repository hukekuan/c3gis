#-*- coding:utf-8 -*-
#!/usr/bin/env python
from flask import render_template, redirect, url_for
from flask_login import current_user, login_required

from apps import poster_permission
from apps.bussinesApp import bussines
from apps.bussinesApp.models import Post


@bussines.route('/')
def Login():
    return render_template('login.html', **locals())

@bussines.route('/main')
def Main():
    return render_template('index.html', **locals())

@bussines.route('/edit/<string:id>', methods=['GET', 'POST'])
@login_required
@poster_permission.require(http_exception=403)
def edit_post(id):
    post = Post.query.get_or_404(id)
    if not current_user:
        return redirect(url_for('login'))