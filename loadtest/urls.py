# -*- coding: UTF-8 -*-
"""learn_models URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""

from django.conf.urls import url, patterns


handler404 = 'loadtest.views.page_not_found'
handler500 = 'loadtest.views.page_error'

'''
urlpatterns = [
    url(r'^$', 'loadtest.views.show_latest', name='index'),
    url(r'^showLatest', 'loadtest.views.show_latest', name='latest'),
    
    url(r'^showAll/(?P<test_type>.*)', 'loadtest.views.show_all_load_test_results', name='showAll'),
    url(r'^showOne/(?P<test_id>.*)', 'loadtest.views.show_one_load_test_result', name='showOne'),
    
    url(r'^getAllByVersion/(?P<test_type>.*)/(?P<test_version>.*)', 'loadtest.views.get_all_load_test_results_by_version', name='allByVersion'),
    url(r'^getAllByModule/(?P<test_type>.*)/(?P<test_version>.*)/(?P<test_module>.*)', 'loadtest.views.get_all_load_test_results_by_module', name='allByModule'),
    
    url(r'^insert', 'loadtest.views.insert_test_result_with_form', name='insert'),
    url(r'^about', 'loadtest.views.about', name='about'),
]
'''

# 提取公共模块出来。如果在不同的view里，那还可以多个urlpatterns连起来
urlpatterns = patterns('loadtest.views',
    url(r'^$', 'show_latest', name='index'),
    url(r'^showLatest', 'show_latest', name='latest'),
    url(r'^showAll/(?P<test_type>.*)', 'show_all_load_test_results', name='showAll'),
    url(r'^showOne/(?P<test_id>.*)', 'show_one_load_test_result', name='showOne'),
    url(r'^getAllByVersion/(?P<test_type>.*)/(?P<test_version>.*)', 'get_all_load_test_results_by_version', name='allByVersion'),
    url(r'^getAllByModule/(?P<test_type>.*)/(?P<test_version>.*)/(?P<test_module>.*)', 'get_all_load_test_results_by_module', name='allByModule'),
    url(r'^insert', 'insert_test_result_with_form', name='insert'),
)

urlpatterns += patterns('loadtest.views',
    url(r'^about', 'about', name='about'),
)
