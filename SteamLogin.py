import winreg


def get_login_status():

    active_user_hkey = r'SOFTWARE\Valve\Steam\ActiveProcess'

    a_reg = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)

    active_process_data = winreg.OpenKey(a_reg, active_user_hkey)

    active_user_id = winreg.EnumValue(active_process_data, 4)[1]

    if active_user_id == 0:
        print('No user logged in, get user login')
        return False
    else:
        print('User is logged in, continue')
        return True


def set_open_applications_always():

    disable_popup_app_hkey = r'SOFTWARE\Policies\Google\Chrome'

    a_reg = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)

    active_process_data = winreg.OpenKey(a_reg, disable_popup_app_hkey)

    winreg.SetValueEx()



if __name__ == '__main__':
    get_login_status()