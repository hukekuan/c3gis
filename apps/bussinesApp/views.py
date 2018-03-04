#-*- coding:utf-8 -*-
#!/usr/bin/env python
from flask import render_template, redirect, url_for, jsonify
from flask_login import current_user, login_required
from flask_principal import UserNeed, Permission

# from apps import poster_permission, admin_permission
from apps.bussinesApp import bussines
from apps.bussinesApp.models import Post
from apps.mainApp.sys.permission import admin_authority


@bussines.route('/')
def Login():
    return render_template('login.html', **locals())

@bussines.route('/main')
def Main():
    return render_template('index.html', **locals())

@bussines.route('/post/<string:id>', methods=['GET', 'POST'])
@login_required
# @poster_permission.require(http_exception=403)
@admin_authority
def edit_post(id):
    post = Post.query.get_or_404(id)
    if not current_user:
        return redirect(url_for('login'))
    if current_user != post.user:
        return jsonify({'info': 'user has not post permession'})
    permission = Permission(UserNeed(post.user.userid))
    if permission.can() or admin_permission.can():
        return jsonify({'info': 'user has post and admin permession'})