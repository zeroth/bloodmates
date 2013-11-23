from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include('mainsite.urls')),
    url(r'^emails/', include('mail.urls')),
    # Examples:
    # url(r'^$', 'emailer.views.home', name='home'),
    # url(r'^emailer/', include('emailer.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include(admin.site.urls)),
)
