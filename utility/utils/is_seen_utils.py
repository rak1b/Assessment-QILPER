def getCurrentUser():
    import inspect
    for frame_record in inspect.stack():
        if frame_record[3] == 'get_response':
            request = frame_record[0].f_locals['request']
            return request.user
            break
    else:
        request = None

def update_dashboard_notification(name, value,created=False,client_user=None):
    from promotions.models import DashboardNotification
    if created:
      update_admin_notification = DashboardNotification.objects.filter(user__is_superuser=True).update(**{name: value})
      if client_user!=None:
        try:
          update_seen_dashboard_notification = DashboardNotification.objects.filter(user=client_user).update(**{name: value})
        except:
           create_user_obj = DashboardNotification.objects.create(user=client_user)
    else:
      update_seen_dashboard_notification = DashboardNotification.objects.filter(user=getCurrentUser()).update(**{name: value})



def update_dashboard_notification_prev(name, value):
    from promotions.models import DashboardNotification
    update_admin_notification = DashboardNotification.objects.filter(user__is_superuser=True).update(**{name: value})
    dashboard_notification = DashboardNotification.objects.filter(user=getCurrentUser()).first()
    
    print("dashboard_notification called")
    if name == 'verification_req':
        if value!=0:
          dashboard_notification.verification_req += value 
        else:
            dashboard_notification.verification_req = 0
    elif name == 'business_req':
        if value!=0:
          dashboard_notification.business_req += value 
        else:
            dashboard_notification.business_req = 0
    elif name == 'client':
        if value!=0:
          dashboard_notification.client += value
        else:
            dashboard_notification.client = 0
    elif name == 'review':
        if value!=0:
          print("dashboard_notification review increased")

          dashboard_notification.review += value
        else:
            dashboard_notification.review = 0
    elif name == 'offers':
        if value!=0:
          dashboard_notification.offers += value
        else:
            dashboard_notification.offers = 0
    elif name == 'advertisement':
        if value!=0:
          dashboard_notification.advertisement += value
        else:
            dashboard_notification.advertisement = 0
    elif name == 'invoice':
        if value!=0:
          dashboard_notification.invoice += value
        else:
            dashboard_notification.invoice = 0
    dashboard_notification.save()
