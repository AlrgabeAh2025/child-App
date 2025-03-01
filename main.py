from flet import *
from views.login_screen.login_screen import Login
from views.signup_screen.signup_screen import SignUp
from views.welcome_screen.welcome_screen import Welcome
from views.home_screen.home_screen import Home
from views.profile_screen.profile_screen import (
    Profile,
    PersonalInformation,
    SecurityPasswords,
)
import requests


def main(page: Page):

    page.fonts = {
        "LateefBoldFont": "/fonts/Lateef,Rakkas/Lateef/Lateef-Bold.ttf",
        "LateefNormalFont": "/fonts/Lateef,Rakkas/Lateef/Lateef-Medium.ttf",
        "Rakkas": "/fonts/Lateef,Rakkas/Rakkas/Rakkas-Regular.ttf",
        "ElMessiri": "/fonts/El_Messiri,Lateef,Rakkas/El_Messiri/ElMessiri-VariableFont_wght.ttf",
    }

    page.theme_mode = ThemeMode.LIGHT
    page.rtl = True
    page.client_storage.clear()
    page.theme = Theme(
        font_family="LateefNormalFont",
        color_scheme_seed="#666666",
        text_theme=TextStyle(color="#110b22", font_family="LateefBoldFont"),
        appbar_theme=AppBarTheme(bgcolor="#110b22", color="#ffffff"),
    )

    baseUrl = "http://192.168.244.135:2010"

    def showMessage(text):
        snack_bar = SnackBar(
                    content=Text(
                        f"{text}",
                        style=TextStyle(size=15, font_family="ElMessiri"),
                    ),
                    show_close_icon=True
                )
        page.open(snack_bar)
    
    def route_change(e):
        routes = {
            "/":Welcome,
            "/home":Home,
            "/login":Login,
            "/signup":SignUp,
            "/Profile":Profile,
            "/PersonalInformation":PersonalInformation,
            "/SecurityPasswords":SecurityPasswords,
        }

        # مسح الشاشة الحالية
        page.views.clear()

        # جلب الشاشة المناسبة بناءً على المسار
        page_class = routes.get(page.route, None)
        page_class.baseUrl = baseUrl
        if page_class:
            page.views.append(
                page_class(route=page.route, page=page)
            )  # إضافة الشاشة المناسبة
        else:
            page.views.append(Text("Page not found"))  # إذا لم يكن المسار موجودًا

        page.update()

    def refreshAccessToken():
        if page.client_storage.contains_key("refresh"):
            async def refresh(refresh_token):
                body={"refresh": refresh_token}
                try:
                    response = requests.post(url=f"{baseUrl}/refresh/", data=body)
                    json = response.json()
                    if response.status_code == 200:
                        return [True , json]
                    else:
                        return [False , "الرجاء التحقق من اتصال الانترنت"]
                except requests.exceptions.Timeout:
                    return [False , "الرجاء التحقق من اتصال الانترنت"]
                except requests.exceptions.ConnectionError:
                    return [False , "لم نتمكن من الوصول الى الخادم الرجاء اعادة المحاولة"]
            refresh_token = page.client_storage.get("refresh")
            result = page.run_task(refresh , refresh_token)
            if result.result()[0]:
                page.client_storage.set("access", result.result()[1]['access'])
                page.client_storage.set("refresh",result.result()[1]['refresh'])  
                return [result.result()[0] , result.result()[1]]
            else :return [result.result()[0] , result.result()[1]]
        else:
            return [False , "سجل الدخول او انشئ حساب"]
        
    page.on_route_change = route_change
    result = refreshAccessToken()
    if result[0]:
        page.go("/home")
    else:
        page.go("/")
        showMessage(result[1])
app(main, assets_dir="assets")